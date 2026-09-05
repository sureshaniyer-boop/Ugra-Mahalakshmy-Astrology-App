# Shri Kashi Astrology Research AI — Phase 1

A local research assistant that converts astrology lecture transcripts into structured, searchable professional notes.

## Phase 1 features

- Paste a YouTube/lecture transcript
- Tamil / English / mixed-language support
- Extract core teachings
- Build an astrology rule database
- Extract Pariharam/remedy instructions
- Extract case studies
- Preserve Nakshatra/Pada/Graha terminology
- Separate teacher statements from AI interpretation
- Flag contradictions and items requiring verification
- Store every analysis in a local SQLite library
- Search previous notes
- Export an analysis as Markdown

## Run from this GitHub repository on Windows

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

Open the local address Streamlit shows, normally `http://localhost:8501`.

## Recommended transcript format

```text
[00:01:20] Today we are discussing Mudakku Dosham...
[00:08:42] If Saturn occupies...
[00:17:10] For this condition the pariharam is...
```

## Data

Your local notes are stored in `astrology_library.db`. It is ignored by GitHub so your private research library is not uploaded accidentally.

## Phase 2 roadmap

1. Video/audio transcription through permitted input routes
2. Semantic search across all notes
3. Ask My Astrology Library
4. Cross-video contradiction comparison
5. Master Pariharam database
6. Master Nakshatra/Pada rule database
7. PDF/book ingestion
8. Source-level citations and timestamp deep links
9. Optional private cloud deployment
