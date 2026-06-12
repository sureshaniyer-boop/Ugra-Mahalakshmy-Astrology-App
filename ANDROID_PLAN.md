# Android Plan

## Best First Android Version

Build the Android app as a mobile shell around the existing calculator backend.

This keeps the astrology calculation accurate and avoids rewriting Swiss Ephemeris calculations in Android/Kotlin immediately.

## Phase 1: GitHub Project

- Keep `app.py` as the calculator backend.
- Keep the browser UI as the first working app interface.
- Add a clean README and `.gitignore`.
- Push to `sureshaniyer-boop/Nakshatra-finder`.

## Phase 2: Online Backend

Deploy the FastAPI app to a cloud host such as Render, Railway, Fly.io, or a small VPS.

The deployed backend should expose:

- `/`
- `/health`
- `/api/places`
- `/api/calculate`

## Phase 3: Mobile App

Use one of these:

### Option A: PWA

Make the website installable on Android from Chrome.

Pros:
- Fastest
- No Play Store required
- Uses the same UI

Cons:
- Needs internet if the backend is online

### Option B: Capacitor Android App

Wrap the mobile web interface into an Android APK.

Pros:
- Feels like a normal Android app
- Can later be published to Play Store

Cons:
- Needs Android Studio setup
- Still needs a backend unless we rewrite calculations natively

### Option C: Fully Offline Native Android

Rebuild the calculation layer using Android-compatible Swiss Ephemeris code.

Pros:
- Works without internet

Cons:
- More development work
- Needs careful validation against the existing Python results

## Recommendation

Start with Option A or B, then consider offline native Android only after the app logic and screens are finalized.
