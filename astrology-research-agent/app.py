import asyncio
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
from database import init_db, save_note, search_notes, list_notes
from agent import analyze_transcript
from media import is_youtube_url, extract_youtube_video_id, transcribe_uploaded_media, read_transcript_upload

st.set_page_config(
    page_title="Shri Kashi Astrology Research AI",
    page_icon="🪷",
    layout="wide",
)

init_db()

st.title("🪷 Shri Kashi Astrology Research AI")
st.caption("Turn astrology videos, transcripts, and lectures into structured, searchable professional research notes.")

if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY is not configured. Create a .env file beside app.py and add your key there.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Analyse Video / Transcript", "Search Library", "All Notes"])

with tab1:
    st.subheader("1. Source")
    c1, c2 = st.columns(2)
    with c1:
        title = st.text_input("Video / Lecture title")
        teacher = st.text_input("Teacher / Astrologer")
    with c2:
        source_url = st.text_input("YouTube / Source URL (optional)")
        language = st.selectbox(
            "Language",
            ["Tamil / English / Mixed", "Tamil", "English", "Sanskrit / Mixed", "Other"],
        )

    if source_url and is_youtube_url(source_url):
        video_id = extract_youtube_video_id(source_url)
        st.success(f"YouTube video recognised. Video ID: {video_id}")
        st.info(
            "For arbitrary public YouTube videos, this app does not bypass YouTube caption permissions or download the video. "
            "Use a transcript you are permitted to access, or upload media you are authorised to process."
        )

    st.subheader("2. Choose Input Method")
    mode = st.radio(
        "Input",
        ["Paste transcript", "Upload transcript file", "Upload audio / video"],
        horizontal=True,
    )

    transcript = ""

    if mode == "Paste transcript":
        transcript = st.text_area(
            "Paste transcript here",
            height=420,
            placeholder="Paste the full transcript. Timestamps such as [00:17:10] are strongly recommended...",
        )

    elif mode == "Upload transcript file":
        transcript_file = st.file_uploader(
            "Upload TXT, SRT or VTT transcript",
            type=["txt", "srt", "vtt"],
        )
        if transcript_file is not None:
            transcript = read_transcript_upload(transcript_file)
            st.success(f"Loaded transcript: {transcript_file.name}")
            with st.expander("Preview transcript"):
                st.text(transcript[:10000])

    else:
        media_file = st.file_uploader(
            "Upload audio or video you are authorised to process",
            type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
        )
        if media_file is not None:
            st.write(f"Selected: {media_file.name}")
            if st.button("Transcribe Uploaded Media", use_container_width=True):
                with st.spinner("Transcribing lecture audio..."):
                    try:
                        st.session_state["phase2_transcript"] = transcribe_uploaded_media(media_file)
                        st.success("Transcription completed.")
                    except Exception as e:
                        st.exception(e)

        transcript = st.session_state.get("phase2_transcript", "")
        if transcript:
            transcript = st.text_area(
                "Review / correct transcription before analysis",
                value=transcript,
                height=420,
            )
            st.session_state["phase2_transcript"] = transcript

    st.subheader("3. Astrology Research Analysis")
    if st.button("Analyse & Save to Astrology Library", type="primary", use_container_width=True):
        if len(transcript.strip()) < 100:
            st.warning("Please provide or transcribe a meaningful transcript before analysing.")
        else:
            with st.spinner("Extracting astrology teachings, rules, pariharam and case studies..."):
                try:
                    analysis = asyncio.run(
                        analyze_transcript(
                            transcript=transcript,
                            title=title,
                            teacher=teacher,
                            source_url=source_url,
                            language=language,
                        )
                    )
                    note_id = save_note(
                        title=title or "Untitled Astrology Lecture",
                        teacher=teacher,
                        source_url=source_url,
                        language=language,
                        transcript=transcript,
                        analysis=analysis,
                    )
                    st.success(f"Saved to your Astrology Library as Note #{note_id}.")
                    st.markdown(analysis)
                    st.download_button(
                        "Download Note as Markdown",
                        data=analysis,
                        file_name=f"astrology_note_{note_id}.md",
                        mime="text/markdown",
                    )
                except Exception as e:
                    st.exception(e)

with tab2:
    query = st.text_input(
        "Search your astrology library",
        placeholder="e.g. Mudakku Dosham, Revathi 4th pada, Saturn retrograde, Ayilyam pariharam",
    )
    if query:
        results = search_notes(query)
        st.write(f"Found {len(results)} note(s).")
        for row in results:
            with st.expander(f"#{row['id']} — {row['title']} — {row['teacher'] or 'Unknown teacher'}"):
                if row["source_url"]:
                    st.write(row["source_url"])
                st.markdown(row["analysis"])

with tab3:
    rows = list_notes()
    if not rows:
        st.info("Your library is empty.")
    for row in rows:
        with st.expander(f"#{row['id']} — {row['title']} — {row['created_at']}"):
            st.write(f"Teacher: {row['teacher'] or 'Unknown'}")
            if row["source_url"]:
                st.write(f"Source: {row['source_url']}")
            st.markdown(row["analysis"])
