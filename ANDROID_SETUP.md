# Android Setup

The easiest Android version is a PWA.

A PWA is a website that Android Chrome can install to the phone home screen like an app.

## Why This Route

The calculator uses Python and Swiss Ephemeris. Android cannot directly run the same local Windows Python app as a normal APK.

So the simplest reliable setup is:

1. Put this project on GitHub.
2. Deploy the app online.
3. Open the deployed link on Android Chrome.
4. Tap **Add to Home screen** or **Install app**.

## Step 1: Upload Updated Files To GitHub

Upload these updated files to your new repository:

- `app.py`
- `requirements.txt`
- `README.md`
- `ANDROID_SETUP.md`
- `ANDROID_PLAN.md`
- `.gitignore`
- `start_app_windows.bat`

Repository:

```text
https://github.com/sureshaniyer-boop/Ugra-Mahalakshmy-Astrology-App
```

## Step 2: Deploy Online

One beginner-friendly option is Render.

1. Go to https://render.com
2. Sign in using GitHub.
3. Click **New**.
4. Choose **Web Service**.
5. Select `Ugra-Mahalakshmy-Astrology-App`.
6. Use these settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
```

7. Click **Create Web Service**.
8. Wait for Render to finish deploying.

Render will give you a public link, for example:

```text
https://your-app-name.onrender.com
```

## Step 3: Install On Android

1. Open the deployed link in Android Chrome.
2. Tap the three-dot menu.
3. Tap **Add to Home screen** or **Install app**.
4. Open the app from your phone home screen.

## Important Note

If the app is deployed online, your phone needs internet to calculate charts.

Fully offline Android is possible later, but it needs a separate native Android calculation engine or an Android-compatible Swiss Ephemeris setup.
