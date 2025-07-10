# Game Analytics Dashboard

A full-stack game analytics dashboard that tracks and visualizes player behavior using simulated (dummy) data. It processes events like session starts, purchases, and level completions — just like real-world telemetry in live games — and presents the insights through dynamic APIs and optional frontend dashboards.

Built with **Flask**, **PostgreSQL**, and **React**, and fully orchestrated using **Docker Compose**.

---
<p align="center">
  <img src="./analyticsdashboard.gif" alt="Dashboard Demo" width="80%">
</p>
<p align="center"><i>A quick preview of the dashboard in action — visualizing player sessions, purchases, and level completions using simulated game data. (Although the gif is very low in quality)</i></p>


## Key Features

- **Interactive Analytics Endpoints**:
  - Active users in the past 24 hours  
  - Average session lengths  
  - Daily revenue reports  
  - Popular completed levels  
  - Total purchase volume

- **Dynamic Filtering**:
  - Filter by device (`Tablet`, `Mobile`, etc.)
  - Filter by date range
  - Filter by game level

- **Tech Highlights**:
  - Modular Flask backend (`src/app`)
  - DRY query building with reusable filter logic (`utils/query_filters.py`)
  - PostgreSQL for relational data querying
  - Dockerized with Compose for isolated services
  - Optional React frontend served via NGINX

---

## Tech Stack

| Layer     | Tech                        |
|-----------|-----------------------------|
| Backend   | Python, Flask, psycopg2     |
| Database  | PostgreSQL                  |
| Frontend  | React, NGINX (optional)     |
| DevOps    | Docker, Docker Compose      |

---

## 📁 Project Structure

```
game-analytics-dashboard/
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── .env
│   └── src/
│       ├── app/
│       │   └── app.py
│       ├── utils/
│       │   └── query_filters.py
│       └── init/
│           └── schema.sql
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── src/
│   │   └── App.js
├── docker-compose.yml
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sinemdonmez/game-analytics-dashboard.git
cd game-analytics-dashboard
```

### 2. Set up environment variables

Create a `.env` file inside `backend/`:

```env
DB_URL=postgresql://postgres:postgres@db:5432/game_analytics
```

### 3. Launch the project

```bash
docker-compose up --build
```

- Backend API: [http://localhost:5000/api](http://localhost:5000/api)
- Frontend UI: [http://localhost:3000](http://localhost:3000)

---

## 🧪 API Examples

```http
GET /api/active-users
GET /api/total-purchases?device=ios&start=2024-01-01&end=2024-02-01
GET /api/popular-levels?level=3
GET /api/daily-revenue?device=android
```

---

## 🧪 Running Tests

To run backend tests:

```bash
docker-compose exec backend bash
# Inside container:
pytest src/tests/
```

Make sure `pytest` is installed in the backend Dockerfile or manually inside the container.

---

## 📄 License

MIT License.

---

## 🙋‍♀️ Author

Built with care by Sinem Dönmez. Focused on backend data engineering and scalable game analytics.

