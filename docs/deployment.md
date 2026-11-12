# Spider Safety Network — Deployment

## Local deployment

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API documentation: http://localhost:8000/docs

## Backend-only deployment

```bash
cd backend
docker build -t spider-safety-backend .
docker run -p 8000:8000 spider-safety-backend
```

## Frontend-only deployment

```bash
cd frontend
npm install
npm run build
npm run preview
```

## Recommended production deployment

- Deploy the backend container to Render, Railway, Fly.io, AWS ECS, Azure Container Apps, or Google Cloud Run.
- Deploy the frontend build to Vercel, Netlify, Cloudflare Pages, or a CDN-backed static hosting service.
- Replace the in-memory store with PostgreSQL and Redis.
- Add authentication, audit logging, monitoring, and backup policies before public launch.

## Environment variables

| Variable | Service | Purpose |
|---|---|---|
| `VITE_API_BASE_URL` | Frontend | Backend API base URL |
| `DATABASE_URL` | Backend, future | PostgreSQL connection string |
| `REDIS_URL` | Backend, future | Redis connection string |
| `JWT_SECRET` | Backend, future | Authentication signing key |
| `DRONE_OPERATOR_API_KEY` | Backend, future | Licensed drone partner integration |
| `INSURER_API_KEY` | Backend, future | Licensed insurance partner integration |
