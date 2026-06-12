# Nakshatra Finder

A local astrology calculator app for sidereal 9-graha positions, nakshatra, pada, graha aspects, and bhava summary.

The app is based on Swiss Ephemeris through `pyswisseph` and currently uses Lahiri ayanamsa by default.

## What It Calculates

- Lagna longitude, rasi, nakshatra, and pada
- Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu positions
- Graha aspect landing points by rasi, nakshatra, pada, and house from lagna
- A 12-bhava aspect count summary

## How To Run On Windows

1. Install Python 3.11.
   Recommended installer: https://www.python.org/downloads/release/python-3119/
2. During Python setup, tick **Add python.exe to PATH**.
3. Double-click `start_app_windows.bat`.
4. Wait for the first-time setup to finish.
5. Open this link in your browser:

   ```text
   http://127.0.0.1:8000
   ```

6. Keep the command window open while using the app.

## Important Python Note

Use Python 3.11 or Python 3.10 on Windows.

Python 3.14 is currently too new for the Windows Swiss Ephemeris package and may require Microsoft C++ Build Tools.

## Developer Run

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000
```

## Android Direction

The current app is a local Python web app. Android cannot directly run this exact Windows/Python setup as a normal APK.

Recommended path:

1. Publish this project to GitHub.
2. Deploy the Python calculator backend to a cloud service.
3. Convert the browser interface into a mobile-friendly PWA or Capacitor Android app.
4. The Android app sends birth details to the backend and displays the same graha/aspect results.

Offline Android is possible later, but it requires a native Android build using an Android-compatible Swiss Ephemeris library or a calculation engine port.

## License Notice

This project uses Swiss Ephemeris through `pyswisseph`. Review Swiss Ephemeris licensing carefully before public or commercial use.
