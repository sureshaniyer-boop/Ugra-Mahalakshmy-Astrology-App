import os
import re
import tempfile
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from openai import OpenAI


def extract_youtube_video_id(url: str) -> str | None:
    if not url:
        return None
    try:
        parsed = urlparse(url.strip())
        host = parsed.netloc.lower().replace("www.", "")
        if host == "youtu.be":
            return parsed.path.strip("/").split("/")[0] or None
        if host in {"youtube.com", "m.youtube.com"}:
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [None])[0]
            parts = [p for p in parsed.path.split("/") if p]
            if len(parts) >= 2 and parts[0] in {"shorts", "live", "embed"}:
                return parts[1]
    except Exception:
        return None
    return None


def is_youtube_url(url: str) -> bool:
    return extract_youtube_video_id(url) is not None


def timestamp_link(url: str, seconds: int) -> str:
    video_id = extract_youtube_video_id(url)
    if not video_id:
        return url
    return f"https://youtu.be/{video_id}?t={max(0, int(seconds))}"


def transcribe_uploaded_media(uploaded_file) -> str:
    """Transcribe a user-provided audio/video file through the OpenAI Audio API."""
    model = os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-transcribe")
    client = OpenAI()

    suffix = Path(uploaded_file.name).suffix or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = Path(tmp.name)

    try:
        with temp_path.open("rb") as f:
            result = client.audio.transcriptions.create(
                model=model,
                file=f,
            )
        return getattr(result, "text", str(result))
    finally:
        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass


def read_transcript_upload(uploaded_file) -> str:
    data = uploaded_file.getvalue()
    for encoding in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")
