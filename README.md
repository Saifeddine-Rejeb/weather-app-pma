# Weather App — Full Stack

**Built by Saifeddine Rejeb**

**Live Demo:** [here](https://weather-app-frontend-sigma-six.vercel.app)

**Technical Assessment:** Full Stack (Tech Assessment #1 + #2)

![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)
![Backend](https://img.shields.io/badge/Backend-Flask%203.1-black?logo=flask)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-React%2019-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Build-Vite-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38BDF8?logo=tailwindcss&logoColor=white)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)
![ORM](https://img.shields.io/badge/ORM-SQLAlchemy-red?logo=sqlalchemy)
![Tests](https://img.shields.io/badge/Tests-37%20passing-brightgreen?logo=pytest)
![License](https://img.shields.io/badge/License-MIT-green)

## PM Accelerator Mission

> _By making industry-leading tools and education available to individuals from all backgrounds, we level the playing field for future PM leaders. This is the PM Accelerator motto, as we grant aspiring and experienced PMs what they need most – Access. We introduce you to industry leaders, surround you with the right PM ecosystem, and discover the new world of AI product management skills._

## What This App Does

A full-stack weather application that lets users:

- Search weather by **city, zip code, GPS coordinates, or landmark**
- View **current weather** with temperature, humidity, wind, and visibility
- View a **5-day forecast** with daily min/max temperatures
- Check the **Air Quality Index (AQI)** for any location
- Watch **YouTube travel videos** for a location
- View **Google Maps** place data for a location
- **Save weather records** for a location and date range (up to 5 days from today, powered by the forecast API)
- **Read, update, and delete** saved records
- **Export** all records in JSON, CSV, or XML format
- Use their **current GPS location** for instant weather lookup

## Tech Stack

### Frontend

- **React 19** + **Vite**
- **Tailwind CSS** + **Radix UI** primitives
- **Lucide** icons

### Backend

- **Flask** — REST API server
- **PostgreSQL** (Neon) + **SQLAlchemy** — persistent database
- **OpenWeather API** — weather, forecast, air quality, geocoding
- **YouTube Data API v3** — location videos
- **Google Places API** — map data
- **pytest** — test suite (37 tests)

## Project Structure

```text
weather-app/
├── backend/
│   ├── .env
│   ├── requirements.txt
│   ├── run.py
│   ├── vercel.json
│   ├── api/
│   │   └── index.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── exceptions.py
│   │   ├── clients/
│   │   │   ├── __init__.py
│   │   │   ├── maps_client.py
│   │   │   ├── weather_client.py
│   │   │   └── youtube_client.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── weather_record.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── enrichment_routes.py
│   │   │   ├── records_routes.py
│   │   │   └── weather_routes.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── export_service.py
│   │       ├── geocoding_service.py
│   │       ├── records_service.py
│   │       └── weather_service.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_geocoding.py
│       ├── test_records_service.py
│       ├── test_routes.py
│       └── test_weather.py
├── frontend/
│   ├── .env
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vercel.json
│   ├── vite.config.js
│   ├── public/
│   │   └── cloud.svg
│   └── src/
│       ├── App.css
│       ├── App.jsx
│       ├── index.css
│       ├── main.jsx
│       ├── assets/
│       │   └── pma.png
│       ├── components/
│       │   ├── ErrorAlert.jsx
│       │   ├── ExploreTab.jsx
│       │   ├── LocationSearch.jsx
│       │   ├── RecordForm.jsx
│       │   ├── RecordsTab.jsx
│       │   ├── WeatherTab.jsx
│       │   └── ui/
│       │       ├── badge.jsx
│       │       ├── button.jsx
│       │       ├── card.jsx
│       │       ├── dialog.jsx
│       │       ├── input.jsx
│       │       ├── label.jsx
│       │       ├── select.jsx
│       │       ├── separator.jsx
│       │       └── tabs.jsx
│       └── lib/
│           ├── api.js
│           └── utils.js
└── README.md
```

---

### Backend Focus Areas

- `backend/app/routes/*`: API endpoints
- `backend/app/services/*`: business logic and integrations
- `backend/app/models/*`: database models
- `backend/api/index.py`: Vercel serverless entrypoint

---

### Frontend Focus Areas

- `frontend/src/App.jsx`: app shell + tab/state orchestration
- `frontend/src/components/*Tab.jsx`: feature-level UI
- `frontend/src/components/RecordForm.jsx`: create/edit modal
- `frontend/src/lib/api.js`: backend API client

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements-dev.txt
cp .env.example .env
# Fill in your API keys in .env
python run.py
```

Backend runs at `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

Create a `frontend/.env` file:

```
VITE_API_URL=http://localhost:5000
```

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

## Environment Variables

### Backend `.env`

```
WEATHER_API_KEY=        # openweathermap.org
YOUTUBE_API_KEY=        # console.cloud.google.com → YouTube Data API v3
GOOGLE_MAPS_API_KEY=    # console.cloud.google.com → Places API
DATABASE_URL=           # PostgreSQL connection string (Neon or other)
                        # If not set, falls back to SQLite locally
```

### Frontend `.env`

```
VITE_API_URL=           # Backend base URL (e.g. https://your-backend.vercel.app)
                        # If not set, falls back to http://localhost:5000
```

## API Endpoints

### Weather

| Method | Endpoint                    | Description       |
| ------ | --------------------------- | ----------------- |
| GET    | `/weather?q=<location>`     | Current weather   |
| GET    | `/forecast?q=<location>`    | 5-day forecast    |
| GET    | `/air-quality?q=<location>` | Air Quality Index |

`location` accepts: city name, zip/postal code, GPS coordinates (`lat,lon`), or landmark.

### Enrichment

| Method | Endpoint                | Description            |
| ------ | ----------------------- | ---------------------- |
| GET    | `/youtube?q=<location>` | YouTube travel videos  |
| GET    | `/maps?q=<location>`    | Google Maps place data |

### Records (CRUD)

| Method | Endpoint                                | Description             |
| ------ | --------------------------------------- | ----------------------- |
| POST   | `/records`                              | Create a weather record |
| GET    | `/records`                              | List all records        |
| GET    | `/records/<id>`                         | Get a single record     |
| PUT    | `/records/<id>`                         | Update a record         |
| DELETE | `/records/<id>`                         | Delete a record         |
| GET    | `/records/export?format=json\|csv\|xml` | Export all records      |

**POST /records body:**

```json
{
  "location": "Paris",
  "start_date": "2025-04-27",
  "end_date": "2025-05-01"
}
```

Date range must start from today, max 5 days (aligned with forecast API window).

### Error Responses

| Status | Meaning                                          |
| ------ | ------------------------------------------------ |
| 400    | Missing fields or invalid date range             |
| 404    | Record not found                                 |
| 422    | Location could not be geocoded                   |
| 502    | External API failed (OpenWeather, YouTube, Maps) |
| 500    | Unexpected server error                          |

## Deployment

Both services are deployed on **Vercel**:

- **Frontend** — Vercel static deployment, Root Directory: `frontend`
- **Backend** — Vercel serverless Python, Root Directory: `backend`
- **Database** — [Neon](https://neon.tech) free tier PostgreSQL

Each has its own Vercel project pointed at the same GitHub repo. Push to `main` triggers automatic redeploy for both.
