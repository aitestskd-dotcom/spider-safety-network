# Spider Safety Network — MVP Prototype

A working product prototype for a **remote-area emergency-response network** in India. It combines:

- Women’s safety and SOS escalation
- First-aid emergency coordination
- A “spider network” of drone/first-aid response nodes
- Travel-area and enterprise subscriptions
- Insurance-ready incident and claims workflows

> This is a software prototype. It does **not** operate real drones, replace 112, police, ambulance, or medical services, or provide insurance underwriting.

## Live prototype

The repository contains:

- **Backend:** FastAPI REST API with an in-memory demo database
- **Frontend:** React + Vite web application
- **Tests:** Pytest API tests
- **CI:** GitHub Actions test workflow
- **Deployment:** Docker Compose for local/cloud deployment

## Core user journey

1. A user registers and adds emergency contacts.
2. The user buys a **Travel Safety Pass** for a route, trek, campsite, industrial site, or remote district.
3. The user activates an SOS.
4. The platform identifies the nearest available spider node.
5. The platform creates an incident, notifies trusted contacts, and records the escalation workflow.
6. A response coordinator can mark the incident as acknowledged, drone dispatched, kit delivered, resolved, or escalated.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/api/nodes` | List spider-network response nodes |
| POST | `/api/users` | Register a demo user |
| POST | `/api/trips` | Create a travel-area safety pass |
| POST | `/api/sos` | Trigger an SOS and create an incident |
| GET | `/api/incidents/{incident_id}` | View incident status and response timeline |
| PATCH | `/api/incidents/{incident_id}/status` | Update incident response status |
| POST | `/api/subscriptions` | Create a subscription record |

## Local development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API documentation: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

### Run with Docker

```bash
docker compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

## Repository structure

```text
backend/                 FastAPI backend and tests
frontend/                React web application
docs/                    Product requirements and architecture
.github/workflows/       CI pipeline
docker-compose.yml       Local deployment
```

## Important product boundaries

- SOS alerts must always be capable of escalating to India’s **112 ERSS** and local emergency services.
- Drone dispatch is a **coordinator workflow**, not an autonomous rescue promise.
- Drone operations require appropriate DGCA authorisation, airspace approval, trained remote pilots, and local emergency-service coordination.
- Insurance must be underwritten by a licensed insurer; this platform only records coverage and supports claims workflow.
- Location data must be consent-based, minimised, encrypted in transit, and retained only according to a defined privacy policy.
