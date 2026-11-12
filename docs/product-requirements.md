# Spider Safety Network — Product Requirements

## 1. Product vision

Provide affordable, location-aware emergency protection for people travelling through or living in remote, low-connectivity, or delayed-response areas of India.

The product combines a free personal-safety layer with paid travel, community, and enterprise coverage. It coordinates first aid, trusted contacts, local responders, drone-enabled medical logistics where authorised, and insurance support.

## 2. Target users

### Consumers

- Women travelling alone or at night
- Trekkers, campers, pilgrims, and adventure travellers
- Rural residents in low-connectivity areas
- Delivery riders and field workers
- Families travelling through remote routes

### Business customers

- Mining, construction, utilities, and logistics companies
- Remote industrial camps
- Tourism operators, resorts, and trekking companies
- State tourism, health, police, and disaster-management departments
- Insurers and corporate wellness providers

## 3. MVP scope

### Included

- User registration and emergency-contact management
- Travel Safety Pass creation
- Spider-node registry and availability status
- SOS activation and incident creation
- Nearest-node selection
- Trusted-contact notification records
- Incident status workflow
- Subscription records
- Basic web dashboard
- API tests and CI

### Excluded from MVP

- Real drone flight control
- Live video streaming
- Payment gateway integration
- Real insurer underwriting
- Aadhaar/KYC verification
- Offline satellite communication
- Production-grade dispatch optimisation

## 4. Key user stories

### As a traveller

- I can register emergency contacts so that help can be alerted quickly.
- I can buy coverage for a specific route and travel period.
- I can trigger an SOS with one action.
- I can see which response node will support my area.

### As a family member

- I can receive an incident alert with the user’s last known location.
- I can view the incident status and response timeline.

### As a response coordinator

- I can see open incidents.
- I can acknowledge an incident.
- I can record drone dispatch or first-aid kit delivery.
- I can escalate or resolve an incident.

### As an enterprise HSE manager

- I can enrol workers in a coverage plan.
- I can view coverage and incident reports.
- I can demonstrate emergency-response readiness.

## 5. Incident workflow

```text
SOS triggered
    → Incident created
    → Nearest available node selected
    → Trusted contacts notified
    → 112/local responder escalation recorded
    → Response coordinator acknowledges
    → Drone dispatch / kit delivery recorded
    → Incident resolved or escalated
```

## 6. Success metrics

| Metric | MVP target |
|---|---:|
| SOS API response time | Under 500 ms in demo environment |
| Test coverage | At least core API happy paths |
| User activation rate | 60% in pilot |
| Emergency-contact completion | 80% in pilot |
| Incident record completeness | 100% of SOS events |
| Coordinator acknowledgement time | Under 2 minutes in pilot |

## 7. Compliance principles

- The platform must never claim to replace 112, police, ambulance, or medical services.
- Drone operations must be performed by authorised operators under applicable Indian regulations.
- Insurance must be provided by a licensed insurer.
- Location sharing must require explicit user consent.
- Incident data must be access-controlled and audit-ready.
