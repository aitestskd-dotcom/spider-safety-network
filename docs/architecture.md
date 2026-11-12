# Spider Safety Network — Architecture

## 1. System context

```text
+----------------+       +----------------------+       +---------------------+
| Mobile / Web   | <---> | Spider Safety API    | <---> | Command Centre UI   |
| User App       |       | FastAPI              |       | Coordinator Console |
+----------------+       +----------------------+       +---------------------+
        |                         |
        |                         +--> PostgreSQL / PostGIS (production)
        |                         +--> Redis (queues, rate limits)
        |                         +--> Notification service
        |                         +--> Payment service
        |                         +--> Insurance partner API
        |                         +--> Drone operator / fleet API
        |                         +--> 112 ERSS / state emergency integration
        |
        +--> Satellite / offline SOS device integration (future)
```

## 2. Spider network model

A **spider network** is a hub-and-spoke topology with mesh-relay capability.

```text
                 Command Centre
                       |
      -------------------------------------
      |             |             |       |
   Node A       Node B       Node C   Node D
   /    \       /    \       /    \     /    \
 User  User   User  User   User  User User  User
```

### Node types

| Node type | Description |
|---|---|
| Fixed drone node | Secure drone nest at a PHC, police post, resort, camp, or industrial site |
| Mobile response node | Vehicle carrying drones, first-aid kits, and trained personnel |
| Community node | Panchayat, women’s help centre, or local partner location with emergency supplies |
| Relay node | Drone or fixed communications node that extends connectivity in weak-network areas |

## 3. Backend architecture

### MVP

- **FastAPI** provides the REST API.
- **Pydantic** validates request and response schemas.
- **In-memory repositories** enable a runnable prototype without external infrastructure.
- **Service layer** contains business rules for node selection, incident creation, and escalation.
- **Pytest** validates API behaviour.

### Production target

| Layer | Technology |
|---|---|
| API | FastAPI, Python 3.11+ |
| Database | PostgreSQL with PostGIS for geospatial queries |
| Cache/queue | Redis |
| Async workers | Celery or ARQ |
| Notifications | SMS, WhatsApp Business API, push notifications |
| Payments | Razorpay, UPI, or enterprise invoicing |
| Maps | MapmyIndia, Google Maps, or OpenStreetMap |
| Drone integration | Licensed drone-operator fleet API |
| Emergency integration | 112 ERSS / state emergency response centre integration |
| Insurance | Licensed insurer API or TPA integration |
| Observability | OpenTelemetry, Prometheus, Grafana, Sentry |

## 4. Data model

### User

- `id`
- `name`
- `phone`
- `emergency_contacts`
- `created_at`

### SpiderNode

- `id`
- `name`
- `node_type`
- `latitude`
- `longitude`
- `coverage_radius_km`
- `capabilities`
- `status`

### TravelPass

- `id`
- `user_id`
- `area_name`
- `start_latitude` / `start_longitude`
- `end_latitude` / `end_longitude`
- `valid_from`
- `valid_to`
- `plan`
- `status`

### Incident

- `id`
- `user_id`
- `travel_pass_id`
- `incident_type`
- `latitude` / `longitude`
- `description`
- `assigned_node_id`
- `status`
- `timeline`
- `insurance_flag`

### Subscription

- `id`
- `user_id`
- `plan`
- `status`
- `started_at`
- `expires_at`

## 5. API design

### SOS flow

```http
POST /api/sos
{
  "user_id": "usr_123",
  "incident_type": "medical",
  "latitude": 30.7333,
  "longitude": 79.0669,
  "description": "Trekking injury, need first aid"
}
```

Response:

```json
{
  "incident_id": "inc_456",
  "status": "open",
  "assigned_node": "node_trek_01",
  "estimated_response_minutes": 12,
  "escalation": {
    "emergency_number": "112",
    "trusted_contacts_notified": 2
  }
}
```

## 6. Security and privacy

- JWT-based authentication for production.
- Role-based access for users, coordinators, enterprise admins, and insurers.
- Location sharing only after explicit consent.
- Incident location retained only for the operational and legal retention period.
- Audit log for every incident-status change.
- Rate limiting and anomaly detection for SOS endpoints.
- Encryption in transit using TLS and at rest for sensitive fields.

## 7. Deployment

### MVP

- Docker Compose: backend, frontend, PostgreSQL, Redis.
- GitHub Actions runs linting and tests.
- Container images can be deployed to Render, Railway, Fly.io, AWS ECS, Azure Container Apps, or GCP Cloud Run.

### Production

- Managed PostgreSQL with automated backups.
- Horizontal API scaling behind a load balancer.
- Private networking for database and internal services.
- Secrets stored in a managed secret manager.
- Blue-green or rolling deployments.
- Disaster-recovery backups and incident-response runbooks.
