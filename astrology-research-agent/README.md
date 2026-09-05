# Shri Kashi Astrology Research AI — Phase 2

A local astrology research assistant that converts lectures, transcripts, and authorised media uploads into structured, searchable professional notes.

## Phase 2 features

- Paste a transcript directly
- Upload TXT, SRT or VTT transcript files
- Upload authorised MP3, MP4, MPEG, MPGA, M4A, WAV or WEBM media and transcribe it with OpenAI speech-to-text
- Recognise YouTube URLs and preserve the source link/video ID
- Tamil / English / mixed-language support
- Extract core astrology teachings
- Build an astrology rule database
- Extract Pariharam/remedy instructions
- Extract case studies
- Preserve Nakshatra/Pada/Graha terminology
- Separate teacher statements from AI interpretation
- Flag contradictions and items requiring verification
- Store every analysis in a local SQLite library
- Search previous notes
- Export an analysis as Markdown

## Important YouTube limitation

The official YouTube Data API does not provide unrestricted caption downloading for arbitrary public videos. Caption listing/downloading requires appropriate authorisation and permissions.

For that reason, this app does not bypass YouTube controls or silently download arbitrary videos. Use one of these routes:

1. Paste a transcript you are permitted to access.
2. Upload a TXT/SRT/VTT transcript.
3. Upload audio/video that you are authorised to process.
4. Later, OAuth support can be added for caption access to YouTube content you own/manage.

## Run from GitHub on Windows

```powershell
git clone https://github.com/sureshaniyer-boop/Ugra-Mahalakshmy-Astrology-App.git
cd Ugra-Mahalakshmy-Astrology-App\astrology-research-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `your_key_here` with your OpenAI API key.

Do not commit `.env` to GitHub.

Then run:

```powershell
streamlit run app.py
```

Open the local address Streamlit shows, normally:

```text
http://localhost:8501
```

## Best workflow for astrology videos

For the strongest research output, use a timestamped transcript whenever available:

```text
[00:01:20] Today we are discussing Mudakku Dosham...
[00:08:42] If Saturn occupies...
[00:17:10] For this condition the pariharam is...
```

The AI will preserve those timestamps in the research note whenever the transcript contains them.

## Data privacy

Your local notes are stored in:

`astrology_library.db`

The database and `.env` are ignored by GitHub, so your private research library and API key are not uploaded accidentally.

## Next roadmap

1. Ask My Astrology Library semantic research assistant
2. Cross-video contradiction comparison
3. Master Pariharam database
4. Master Nakshatra/Pada rule database
5. PDF/book ingestion
6. Source-level timestamp deep links
7. Optional OAuth for captions on YouTube content you own/manage
8. Optional private cloud deployment
