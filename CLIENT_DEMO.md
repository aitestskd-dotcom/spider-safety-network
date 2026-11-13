# Spider Safety Network — Client Demo Guide

## Purpose

Use this guide to run a live client demonstration from the GitHub-hosted prototype.

The demo shows the SOS, nearest-node selection, incident timeline, and coordinator acknowledgement workflow. It does not dispatch a real drone, replace 112, police, ambulance, or medical services, or provide insurance underwriting.

## Deployment architecture

```text
GitHub repository
      |
      +--> Render: FastAPI backend
      |
      +--> Vercel: React frontend
                  |
                  +--> Client browser
```

## Render backend setup

1. Connect the GitHub repository to Render.
2. Create a new Web Service.
3. Select the repository: `spider-safety-network`.
4. Set Root Directory to `backend`.
5. Set Runtime to Python 3.
6. Set Build Command to `pip install -r requirements.txt`.
7. Set Start Command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
8. Add environment variable `ALLOWED_ORIGINS` with your Vercel URL, for example `https://spider-safety-network.vercel.app`.
9. Deploy the service.
10. Test `https://your-render-service-url/health`.

Alternatively, Render can use the included `render.yaml` blueprint.

## Vercel frontend setup

1. Connect the GitHub repository to Vercel.
2. Create a new project.
3. Set Root Directory to `frontend`.
4. Set Framework Preset to Vite.
5. Add environment variable `VITE_API_BASE_URL` with the Render backend URL, for example `https://your-render-service-url`.
6. Deploy the project.
7. Open the Vercel URL and confirm the spider nodes load.

## Client demo script

### 1. Opening

Say:

> “This is the Spider Safety Network prototype. It demonstrates how a traveller, worker, or resident in a remote area can raise an SOS and how the platform identifies the nearest response node and coordinates the emergency workflow.”

### 2. Show the network

Open the application and show the spider-network node list.

Explain that nodes can represent:

- Fixed drone and first-aid stations
- Mobile response vehicles
- Community health centres
- Resorts, camps, or trekking bases
- Industrial sites
- Highway checkpoints

### 3. Register a user

Click **Register demo user**.

Explain:

- Emergency-contact capture
- Consent-based location sharing
- Safety profile creation
- Family notification capability

### 4. Trigger SOS

Click **Trigger demo SOS**.

Show:

- Incident ID
- Assigned nearest node
- Estimated response time
- Trusted contacts notified
- 112 escalation record
- Incident timeline

Say:

> “In production, the platform would escalate to 112 and coordinate with local emergency responders. A licensed drone operator would handle any authorised drone dispatch.”

### 5. Coordinator workflow

Click **Acknowledge incident**.

Show the status change and timeline entry.

Say:

> “A trained coordinator remains responsible for the response. The platform provides visibility, escalation records, and an audit trail.”

### 6. Close

Say:

> “The free layer builds safety adoption. The subscription funds first-aid readiness and response coordination. Insurance adds financial protection. The spider network allows one node to serve many users across a route, camp, village, or industrial site.”

## Demo disclaimer

Display this during the demonstration:

> **Live prototype demonstration. This does not dispatch a real drone, replace 112, police, ambulance, or medical services, or provide insurance underwriting.**

## Demo checklist

- Backend health endpoint returns `status: ok`.
- Frontend loads spider nodes.
- Demo user registration succeeds.
- SOS creates an incident.
- Nearest node is assigned.
- Incident timeline is visible.
- Coordinator acknowledgement works.
- API documentation is available at `/docs`.
- Client can access the frontend URL from a phone or laptop.
