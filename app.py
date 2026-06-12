from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel

try:
    import swisseph as swe
except Exception as exc:  # pragma: no cover
    swe = None
    SWISSEPH_IMPORT_ERROR = str(exc)
else:
    SWISSEPH_IMPORT_ERROR = ""


app = FastAPI(title="Ugra Mahalakshmy Astrology App", version="1.0.0")

RASI = [
    ("Mesha", "Aries"),
    ("Rishaba", "Taurus"),
    ("Mithuna", "Gemini"),
    ("Kadagam", "Cancer"),
    ("Simha", "Leo"),
    ("Kanni", "Virgo"),
    ("Thula", "Libra"),
    ("Vrichigam", "Scorpio"),
    ("Dhanusu", "Sagittarius"),
    ("Makara", "Capricorn"),
    ("Kumbam", "Aquarius"),
    ("Meenam", "Pisces"),
]

NAKSHATRAS = [
    ("Ashwini", "Ketu"),
    ("Bharani", "Venus"),
    ("Krittika", "Sun"),
    ("Rohini", "Moon"),
    ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"),
    ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"),
    ("Purva Phalguni", "Venus"),
    ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"),
    ("Chitra", "Mars"),
    ("Swati", "Rahu"),
    ("Vishaka", "Jupiter"),
    ("Anuradha", "Saturn"),
    ("Jyeshta", "Mercury"),
    ("Mula", "Ketu"),
    ("Purvashada", "Venus"),
    ("Uttarashada", "Sun"),
    ("Shravana", "Moon"),
    ("Dhanishta", "Mars"),
    ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"),
    ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury"),
]

ASPECT_RULES = {
    "Sun": [("7th", 180, "Classical Parashari")],
    "Moon": [("7th", 180, "Classical Parashari")],
    "Mars": [
        ("4th", 90, "Special aspect"),
        ("7th", 180, "Classical aspect"),
        ("8th", 210, "Special aspect"),
    ],
    "Mercury": [("7th", 180, "Classical Parashari")],
    "Jupiter": [
        ("5th", 120, "Special aspect"),
        ("7th", 180, "Classical aspect"),
        ("9th", 240, "Special aspect"),
    ],
    "Venus": [("7th", 180, "Classical Parashari")],
    "Saturn": [
        ("3rd", 60, "Special aspect"),
        ("7th", 180, "Classical aspect"),
        ("10th", 270, "Special aspect"),
    ],
    "Rahu": [
        ("5th", 120, "Research/tradition-dependent"),
        ("7th", 180, "Research/tradition-dependent"),
        ("9th", 240, "Research/tradition-dependent"),
    ],
    "Ketu": [
        ("5th", 120, "Research/tradition-dependent"),
        ("7th", 180, "Research/tradition-dependent"),
        ("9th", 240, "Research/tradition-dependent"),
    ],
}

HOUSE_MEANINGS = {
    1: "Body, identity, life direction",
    2: "Family, speech, savings",
    3: "Courage, effort, siblings, communication",
    4: "Home, mother, property, inner peace",
    5: "Children, intelligence, purva punya",
    6: "Debt, disease, enemies, service",
    7: "Marriage, partners, public dealings",
    8: "Longevity, transformation, hidden karma",
    9: "Dharma, fortune, guru, father",
    10: "Career, karma, status, authority",
    11: "Gains, network, fulfilment",
    12: "Loss, sleep, moksha, foreign matters",
}

PLACES = [
    {"place": "Kuala Lumpur, Malaysia", "lat": 3.139003, "lon": 101.686855, "tz": 8, "country": "Malaysia"},
    {"place": "Batu Caves, Malaysia", "lat": 3.2379, "lon": 101.684, "tz": 8, "country": "Malaysia"},
    {"place": "Petaling Jaya, Malaysia", "lat": 3.1073, "lon": 101.6067, "tz": 8, "country": "Malaysia"},
    {"place": "Shah Alam, Malaysia", "lat": 3.0738, "lon": 101.5183, "tz": 8, "country": "Malaysia"},
    {"place": "Klang, Malaysia", "lat": 3.0449, "lon": 101.4456, "tz": 8, "country": "Malaysia"},
    {"place": "Penang, Malaysia", "lat": 5.4141, "lon": 100.3288, "tz": 8, "country": "Malaysia"},
    {"place": "Ipoh, Malaysia", "lat": 4.5975, "lon": 101.0901, "tz": 8, "country": "Malaysia"},
    {"place": "Johor Bahru, Malaysia", "lat": 1.4927, "lon": 103.7414, "tz": 8, "country": "Malaysia"},
    {"place": "Singapore", "lat": 1.3521, "lon": 103.8198, "tz": 8, "country": "Singapore"},
    {"place": "Chennai, India", "lat": 13.0827, "lon": 80.2707, "tz": 5.5, "country": "India"},
    {"place": "Madurai, India", "lat": 9.9252, "lon": 78.1198, "tz": 5.5, "country": "India"},
    {"place": "Bengaluru, India", "lat": 12.9716, "lon": 77.5946, "tz": 5.5, "country": "India"},
    {"place": "Mumbai, India", "lat": 19.076, "lon": 72.8777, "tz": 5.5, "country": "India"},
    {"place": "Delhi, India", "lat": 28.6139, "lon": 77.209, "tz": 5.5, "country": "India"},
    {"place": "Colombo, Sri Lanka", "lat": 6.9271, "lon": 79.8612, "tz": 5.5, "country": "Sri Lanka"},
]


class ChartRequest(BaseModel):
    name: str = "Sample Client"
    date: str
    time: str
    place: str = "Kuala Lumpur, Malaysia"
    lat: float
    lon: float
    tz: float
    ayanamsa: str = "Lahiri"
    node: str = "Mean Node"


def normalize(deg: float) -> float:
    return float(deg % 360.0)


def position_parts(longitude: float) -> Dict[str, object]:
    lon = normalize(longitude)
    rasi_index = int(lon // 30.0)
    deg_in_rasi = lon % 30.0
    nak_len = 40.0 / 3.0
    pada_len = 10.0 / 3.0
    nak_index = int(lon // nak_len)
    pada = int((lon % nak_len) // pada_len) + 1
    return {
        "longitude": round(lon, 8),
        "rasi_index": rasi_index + 1,
        "rasi": RASI[rasi_index][0],
        "sign": RASI[rasi_index][1],
        "degree_in_rasi": round(deg_in_rasi, 8),
        "nakshatra_index": nak_index + 1,
        "nakshatra": NAKSHATRAS[nak_index][0],
        "nakshatra_lord": NAKSHATRAS[nak_index][1],
        "pada": pada,
    }


def house_from_lagna(target_longitude: float, lagna_longitude: float) -> int:
    target_rasi = int(normalize(target_longitude) // 30.0)
    lagna_rasi = int(normalize(lagna_longitude) // 30.0)
    return ((target_rasi - lagna_rasi) % 12) + 1


def configure_swisseph(ayanamsa: str) -> None:
    if swe is None:
        raise RuntimeError(f"pyswisseph is not installed or failed to import: {SWISSEPH_IMPORT_ERROR}")

    try:
        swe.set_ephe_path(os.environ.get("SWEPH_EPHE_PATH", "./ephe"))
    except Exception:
        pass

    ay = (ayanamsa or "Lahiri").strip().lower()
    if ay.startswith("lahiri"):
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    else:
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)


def julian_day_ut(date_str: str, time_str: str, tz: float) -> float:
    local_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    utc_dt = local_dt - timedelta(hours=float(tz))
    hour_ut = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_ut)


def calc_planet(jd_ut: float, body_id: int, flags: int) -> Tuple[float, float]:
    result = swe.calc_ut(jd_ut, body_id, flags)
    values = result[0]
    return normalize(float(values[0])), float(values[3]) if len(values) > 3 else 0.0


def calc_lagna(jd_ut: float, lat: float, lon: float) -> float:
    try:
        _cusps, ascmc = swe.houses_ex(jd_ut, float(lat), float(lon), b"P", swe.FLG_SIDEREAL)
    except TypeError:
        try:
            _cusps, ascmc = swe.houses_ex(jd_ut, float(lat), float(lon), b"P")
        except TypeError:
            _cusps, ascmc = swe.houses(jd_ut, float(lat), float(lon), b"P")
    return normalize(float(ascmc[0]))


def build_chart(data: ChartRequest) -> Dict[str, object]:
    configure_swisseph(data.ayanamsa)
    jd_ut = julian_day_ut(data.date, data.time, data.tz)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    lagna_lon = calc_lagna(jd_ut, data.lat, data.lon)
    lagna = position_parts(lagna_lon)
    lagna["speed"] = 0
    lagna["source"] = "Swiss Ephemeris ascendant"

    planet_ids = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("Mars", swe.MARS),
        ("Mercury", swe.MERCURY),
        ("Jupiter", swe.JUPITER),
        ("Venus", swe.VENUS),
        ("Saturn", swe.SATURN),
    ]
    node_id = swe.TRUE_NODE if data.node.lower().startswith("true") else swe.MEAN_NODE
    planet_ids.append(("Rahu", node_id))

    planets: List[Dict[str, object]] = []
    for name, body_id in planet_ids:
        p_lon, speed = calc_planet(jd_ut, body_id, flags)
        item = position_parts(p_lon)
        item["name"] = name
        item["speed"] = round(speed, 8)
        item["source"] = "Swiss Ephemeris sidereal"
        planets.append(item)

    rahu_lon = next(float(p["longitude"]) for p in planets if p["name"] == "Rahu")
    ketu = position_parts(rahu_lon + 180.0)
    ketu["name"] = "Ketu"
    ketu["speed"] = next(p["speed"] for p in planets if p["name"] == "Rahu")
    ketu["source"] = "Rahu + 180 degrees"
    planets.append(ketu)

    aspects: List[Dict[str, object]] = []
    for planet in planets:
        name = str(planet["name"])
        for aspect_name, offset, note in ASPECT_RULES.get(name, []):
            target_lon = normalize(float(planet["longitude"]) + float(offset))
            target = position_parts(target_lon)
            house = house_from_lagna(target_lon, lagna_lon)
            aspects.append(
                {
                    "planet": name,
                    "aspect": aspect_name,
                    "offset": offset,
                    "tradition_note": note,
                    "source_longitude": planet["longitude"],
                    "source_rasi": planet["rasi"],
                    "target_longitude": target["longitude"],
                    "target_rasi": target["rasi"],
                    "target_degree": target["degree_in_rasi"],
                    "target_nakshatra": target["nakshatra"],
                    "target_pada": target["pada"],
                    "house_from_lagna": house,
                    "house_meaning": HOUSE_MEANINGS[house],
                }
            )

    house_counts = []
    for house in range(1, 13):
        count = sum(1 for aspect in aspects if aspect["house_from_lagna"] == house)
        house_counts.append(
            {
                "house": house,
                "meaning": HOUSE_MEANINGS[house],
                "aspect_count": count,
                "reading": "No direct aspect landing"
                if count == 0
                else f"{count} aspect landing(s)",
            }
        )

    return {
        "input": data.dict(),
        "julian_day_ut": jd_ut,
        "lagna": lagna,
        "planets": planets,
        "aspects": aspects,
        "house_counts": house_counts,
    }


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return HTML


@app.get("/manifest.webmanifest")
def manifest() -> JSONResponse:
    return JSONResponse(
        {
            "name": "Ugra Mahalakshmy Astrology App",
            "short_name": "Ugra Astrology",
            "description": "Sidereal 9-graha astrology calculator with nakshatra, pada, aspects, and bhava summary.",
            "start_url": "/",
            "scope": "/",
            "display": "standalone",
            "background_color": "#eef4ef",
            "theme_color": "#0a4d38",
            "orientation": "portrait",
            "icons": [
                {
                    "src": "/icon.svg",
                    "sizes": "any",
                    "type": "image/svg+xml",
                    "purpose": "any maskable",
                }
            ],
        }
    )


@app.get("/service-worker.js")
def service_worker() -> Response:
    return Response(SERVICE_WORKER, media_type="application/javascript")


@app.get("/icon.svg")
def icon() -> Response:
    return Response(APP_ICON, media_type="image/svg+xml")


@app.get("/api/places")
def places() -> List[Dict[str, object]]:
    return PLACES


@app.get("/health")
def health() -> Dict[str, object]:
    return {
        "status": "ok" if swe is not None else "pyswisseph import failed",
        "pyswisseph_loaded": swe is not None,
        "error": SWISSEPH_IMPORT_ERROR,
    }


@app.post("/api/calculate")
def calculate(data: ChartRequest):
    try:
        return build_chart(data)
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})


HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0a4d38">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
  <title>Ugra Mahalakshmy Astrology App</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #17211c;
      --muted: #5b6761;
      --line: #d9e2dc;
      --panel: #ffffff;
      --soft: #f4f7f1;
      --mark: #0f6b4e;
      --mark-2: #ad5f1d;
      --wash: #fff3cf;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: #eef4ef;
      color: var(--ink);
    }
    header {
      background: #0a4d38;
      color: white;
      padding: 18px 24px;
      border-bottom: 5px solid #d69b35;
    }
    h1 {
      margin: 0;
      font-size: 24px;
      letter-spacing: 0;
    }
    main {
      display: grid;
      grid-template-columns: 360px minmax(0, 1fr);
      gap: 18px;
      padding: 18px;
      max-width: 1360px;
      margin: 0 auto;
    }
    section, aside {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(20, 40, 30, 0.06);
    }
    aside {
      padding: 16px;
      align-self: start;
      position: sticky;
      top: 12px;
    }
    .results { padding: 16px; min-width: 0; }
    h2 {
      margin: 0 0 12px;
      font-size: 18px;
    }
    label {
      display: block;
      font-size: 13px;
      font-weight: 700;
      color: #25332c;
      margin: 12px 0 6px;
    }
    input, select, button {
      width: 100%;
      font: inherit;
      border-radius: 6px;
    }
    input, select {
      border: 1px solid #cbd8d0;
      padding: 9px 10px;
      background: white;
      color: var(--ink);
    }
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    button {
      border: 0;
      margin-top: 16px;
      padding: 11px 14px;
      background: var(--mark);
      color: white;
      font-weight: 700;
      cursor: pointer;
    }
    button:hover { background: #09563e; }
    .status {
      margin-top: 12px;
      padding: 10px;
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--muted);
      font-size: 13px;
      min-height: 39px;
    }
    .summary {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }
    .metric {
      background: var(--soft);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      min-height: 78px;
    }
    .metric span {
      display: block;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
    }
    .metric strong {
      display: block;
      font-size: 18px;
      overflow-wrap: anywhere;
    }
    .tabs {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--line);
      margin-bottom: 12px;
      overflow-x: auto;
    }
    .tab {
      width: auto;
      margin: 0;
      background: transparent;
      color: var(--muted);
      border-radius: 6px 6px 0 0;
      padding: 9px 11px;
      white-space: nowrap;
    }
    .tab.active {
      background: var(--wash);
      color: var(--ink);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th, td {
      border-bottom: 1px solid #e4ebe6;
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background: #e7f4ec;
      color: #19362b;
      position: sticky;
      top: 0;
      z-index: 1;
    }
    .table-wrap {
      max-height: 560px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    .hidden { display: none; }
    .manual {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      padding: 10px;
      margin-top: 10px;
      background: #fbfcfa;
      border: 1px solid var(--line);
      border-radius: 6px;
    }
    @media (max-width: 900px) {
      main { grid-template-columns: 1fr; }
      aside { position: static; }
      .summary { grid-template-columns: 1fr 1fr; }
      .manual { grid-template-columns: 1fr; }
    }
    @media (max-width: 560px) {
      main { padding: 10px; }
      .summary, .row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Ugra Mahalakshmy Astrology App</h1>
  </header>
  <main>
    <aside>
      <h2>Birth Details</h2>
      <form id="chartForm">
        <label for="name">Client Name</label>
        <input id="name" value="Sample Client">

        <div class="row">
          <div>
            <label for="date">Date of Birth</label>
            <input id="date" type="date" value="1985-04-12" required>
          </div>
          <div>
            <label for="time">Time of Birth</label>
            <input id="time" type="time" value="03:39:00" step="1" required>
          </div>
        </div>

        <label for="place">Place of Birth</label>
        <select id="place"></select>

        <div class="manual">
          <div>
            <label for="lat">Latitude</label>
            <input id="lat" type="number" value="3.139003" step="0.000001">
          </div>
          <div>
            <label for="lon">Longitude</label>
            <input id="lon" type="number" value="101.686855" step="0.000001">
          </div>
          <div>
            <label for="tz">Timezone</label>
            <input id="tz" type="number" value="8" step="0.5">
          </div>
        </div>

        <div class="row">
          <div>
            <label for="ayanamsa">Ayanamsa</label>
            <select id="ayanamsa">
              <option>Lahiri</option>
            </select>
          </div>
          <div>
            <label for="node">Node Mode</label>
            <select id="node">
              <option>Mean Node</option>
              <option>True Node</option>
            </select>
          </div>
        </div>

        <button type="submit">Calculate</button>
      </form>
      <div id="status" class="status">Ready.</div>
    </aside>

    <section class="results">
      <div class="summary">
        <div class="metric"><span>Client</span><strong id="mClient">-</strong></div>
        <div class="metric"><span>Lagna</span><strong id="mLagna">-</strong></div>
        <div class="metric"><span>Nakshatra</span><strong id="mNak">-</strong></div>
        <div class="metric"><span>Active Aspects</span><strong id="mAspects">-</strong></div>
      </div>

      <div class="tabs">
        <button class="tab active" type="button" data-tab="planets">Graha Positions</button>
        <button class="tab" type="button" data-tab="aspects">Aspect Output</button>
        <button class="tab" type="button" data-tab="houses">Bhava Summary</button>
      </div>

      <div id="planets" class="panel">
        <div class="table-wrap"><table id="planetTable"></table></div>
      </div>
      <div id="aspects" class="panel hidden">
        <div class="table-wrap"><table id="aspectTable"></table></div>
      </div>
      <div id="houses" class="panel hidden">
        <div class="table-wrap"><table id="houseTable"></table></div>
      </div>
    </section>
  </main>

  <script>
    let places = [];

    const $ = (id) => document.getElementById(id);
    const status = $("status");

    function setStatus(message, isError = false) {
      status.textContent = message;
      status.style.color = isError ? "#a32816" : "#5b6761";
    }

    function cell(value) {
      return value === undefined || value === null || value === "" ? "-" : value;
    }

    function degrees(value) {
      if (value === undefined || value === null || value === "") return "-";
      return Number(value).toFixed(4);
    }

    function renderTable(table, headers, rows) {
      table.innerHTML = "";
      const thead = document.createElement("thead");
      const headerRow = document.createElement("tr");
      headers.forEach((header) => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      table.appendChild(thead);

      const tbody = document.createElement("tbody");
      rows.forEach((row) => {
        const tr = document.createElement("tr");
        row.forEach((value) => {
          const td = document.createElement("td");
          td.textContent = cell(value);
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
    }

    async function loadPlaces() {
      const response = await fetch("/api/places");
      places = await response.json();
      const select = $("place");
      select.innerHTML = "";
      places.forEach((item, index) => {
        const option = document.createElement("option");
        option.value = String(index);
        option.textContent = item.place;
        select.appendChild(option);
      });
      applyPlace(0);
    }

    function applyPlace(index) {
      const item = places[index];
      if (!item) return;
      $("lat").value = item.lat;
      $("lon").value = item.lon;
      $("tz").value = item.tz;
    }

    async function calculate() {
      const place = places[Number($("place").value)] || {};
      const payload = {
        name: $("name").value || "Client",
        date: $("date").value,
        time: $("time").value,
        place: place.place || "Manual",
        lat: Number($("lat").value),
        lon: Number($("lon").value),
        tz: Number($("tz").value),
        ayanamsa: $("ayanamsa").value,
        node: $("node").value,
      };

      setStatus("Calculating...");
      const response = await fetch("/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Calculation failed");
      }
      renderResults(data);
      setStatus("Calculation complete.");
    }

    function renderResults(data) {
      $("mClient").textContent = data.input.name;
      $("mLagna").textContent = `${data.lagna.rasi} (${data.lagna.sign})`;
      $("mNak").textContent = `${data.lagna.nakshatra} Pada ${data.lagna.pada}`;
      $("mAspects").textContent = String(data.aspects.length);

      const planetRows = [
        ["Lagna", data.lagna.longitude, data.lagna.rasi, data.lagna.sign, data.lagna.degree_in_rasi, data.lagna.nakshatra, data.lagna.pada, data.lagna.source],
        ...data.planets.map((p) => [p.name, p.longitude, p.rasi, p.sign, p.degree_in_rasi, p.nakshatra, p.pada, p.source]),
      ].map((row) => [row[0], degrees(row[1]), row[2], row[3], degrees(row[4]), row[5], row[6], row[7]]);
      renderTable($("planetTable"), ["Body", "Longitude", "Rasi", "Sign", "Degree", "Nakshatra", "Pada", "Source"], planetRows);

      const aspectRows = data.aspects.map((a) => [
        a.planet,
        a.aspect,
        a.offset,
        a.tradition_note,
        degrees(a.source_longitude),
        a.source_rasi,
        degrees(a.target_longitude),
        a.target_rasi,
        degrees(a.target_degree),
        a.target_nakshatra,
        a.target_pada,
        a.house_from_lagna,
        a.house_meaning,
      ]);
      renderTable($("aspectTable"), ["Planet", "Aspect", "Offset", "Tradition", "Source Lon", "Source Rasi", "Target Lon", "Target Rasi", "Target Degree", "Target Nakshatra", "Pada", "House", "Meaning"], aspectRows);

      const houseRows = data.house_counts.map((h) => [h.house, h.meaning, h.aspect_count, h.reading]);
      renderTable($("houseTable"), ["House", "Meaning", "Aspect Count", "Reading"], houseRows);
    }

    $("place").addEventListener("change", (event) => applyPlace(Number(event.target.value)));
    $("chartForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        await calculate();
      } catch (error) {
        setStatus(error.message, true);
      }
    });
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
        document.querySelectorAll(".panel").forEach((panel) => panel.classList.add("hidden"));
        tab.classList.add("active");
        document.getElementById(tab.dataset.tab).classList.remove("hidden");
      });
    });

    loadPlaces().then(calculate).catch((error) => setStatus(error.message, true));
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("/service-worker.js").catch(() => {});
      });
    }
  </script>
</body>
</html>
"""

SERVICE_WORKER = r"""
const CACHE_NAME = "ugra-astrology-v1";
const APP_SHELL = ["/", "/manifest.webmanifest", "/icon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (response.ok && new URL(request.url).origin === self.location.origin) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        }
        return response;
      });
    })
  );
});
"""

APP_ICON = r"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="104" fill="#0a4d38"/>
  <circle cx="256" cy="256" r="174" fill="#fff3cf"/>
  <circle cx="256" cy="256" r="118" fill="none" stroke="#ad5f1d" stroke-width="18"/>
  <path d="M256 92l28 96 96-28-68 74 68 74-96-28-28 96-28-96-96 28 68-74-68-74 96 28z" fill="#0f6b4e"/>
  <circle cx="256" cy="256" r="34" fill="#ad5f1d"/>
</svg>
"""
