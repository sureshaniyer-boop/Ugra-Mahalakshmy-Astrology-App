import asyncio
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
from database import init_db, save_note, search_notes, list_notes
from agent import analyze_transcript

st.set_page_config(
    page_title="Shri Kashi Astrology Research AI",
    page_icon="🪷",
    layout="wide",
)

init_db()

st.title("🪷 Shri Kashi Astrology Research AI")
st.caption("Convert astrology lectures into structured, searchable professional research notes.")

if not os.getenv("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY is not configured. Create a .env file beside app.py and add your key there."
    )
    st.stop()

tab1, tab2, tab3 = st.tabs(["Analyse Transcript", "Search Library", "All Notes"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        title = st.text_input("Video / Lecture title")
        teacher = st.text_input("Teacher / Astrologer")
    with c2:
        source_url = st.text_input("Source URL (optional)")
        language = st.selectbox(
            "Language",
            ["Tamil / English / Mixed", "Tamil", "English", "Sanskrit / Mixed", "Other"],
        )

    transcript = st.text_area(
        "Paste transcript here",
        height=420,
        placeholder="Paste the full transcript, preferably with timestamps...",
    )

    if st.button("Analyse & Save", type="primary", use_container_width=True):
        if len(transcript.strip()) < 100:
            st.warning("Please paste a meaningful transcript before analysing.")
        else:
            with st.spinner("Analysing astrology teachings..."):
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
