"""FastAPI application for the Spider Safety Network MVP."""

from __future__ import annotations

import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .models import (
    InMemoryStore,
    IncidentStatus,
    IncidentType,
    NodeCapability,
    PlanType,
    SpiderNode,
    Subscription,
)
from .services import NetworkService

app = FastAPI(
    title="Spider Safety Network API",
    description="MVP API for remote-area women’s safety, first-aid response, and drone-node coordination.",
    version="0.1.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

store = InMemoryStore()
network = NetworkService(store)


def seed_nodes() -> None:
    demo_nodes = [
        SpiderNode(
            id="node_rishikesh_01",
            name="Rishikesh Trek Base Node",
            node_type="fixed_drone_node",
            latitude=30.0869,
            longitude=78.2676,
            coverage_radius_km=25,
            capabilities=[
                NodeCapability.FIRST_AID_KIT,
                NodeCapability.AED,
                NodeCapability.DRONE,
                NodeCapability.COMMUNICATION_RELAY,
            ],
        ),
        SpiderNode(
            id="node_dehradun_01",
            name="Dehradun Highway Response Node",
            node_type="mobile_response_node",
            latitude=30.3165,
            longitude=78.0322,
            coverage_radius_km=40,
            capabilities=[
                NodeCapability.FIRST_AID_KIT,
                NodeCapability.AMBULANCE_COORDINATION,
                NodeCapability.COMMUNICATION_RELAY,
            ],
        ),
        SpiderNode(
            id="node_gangtok_01",
            name="Gangtok Remote Health Node",
            node_type="fixed_drone_node",
            latitude=27.3389,
            longitude=88.6065,
            coverage_radius_km=35,
            capabilities=[
                NodeCapability.FIRST_AID_KIT,
                NodeCapability.AED,
                NodeCapability.DRONE,
            ],
        ),
    ]
    for node in demo_nodes:
        store.nodes[node.id] = node


seed_nodes()


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=8, max_length=20)
    emergency_contacts: List[dict] = Field(default_factory=list)


class TravelPassRequest(BaseModel):
    user_id: str
    area_name: str
    start_latitude: float
    start_longitude: float
    end_latitude: float
    end_longitude: float
    valid_from: datetime
    valid_to: datetime
    plan: PlanType = PlanType.TRAVEL_PASS


class SosRequest(BaseModel):
    user_id: str
    incident_type: IncidentType
    latitude: float
    longitude: float
    description: str = ""
    travel_pass_id: Optional[str] = None


class IncidentStatusRequest(BaseModel):
    status: IncidentStatus
    note: str = Field(min_length=3, max_length=500)


class SubscriptionRequest(BaseModel):
    user_id: str
    plan: PlanType
    duration_days: int = Field(default=30, ge=1, le=365)


@app.get("/health")
def health():
    return {"status": "ok", "service": "spider-safety-network", "version": "0.1.0"}


@app.get("/api/nodes")
def list_nodes():
    return {
        "count": len(store.nodes),
        "nodes": list(store.nodes.values()),
    }


@app.post("/api/users", status_code=201)
def create_user(payload: CreateUserRequest):
    try:
        user = network.create_user(
            name=payload.name,
            phone=payload.phone,
            emergency_contacts=payload.emergency_contacts,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return user


@app.post("/api/trips", status_code=201)
def create_travel_pass(payload: TravelPassRequest):
    try:
        travel_pass = network.create_travel_pass(
            user_id=payload.user_id,
            area_name=payload.area_name,
            start_latitude=payload.start_latitude,
            start_longitude=payload.start_longitude,
            end_latitude=payload.end_latitude,
            end_longitude=payload.end_longitude,
            valid_from=payload.valid_from,
            valid_to=payload.valid_to,
            plan=payload.plan,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return travel_pass


@app.post("/api/sos", status_code=201)
def trigger_sos(payload: SosRequest):
    try:
        incident = network.trigger_sos(
            user_id=payload.user_id,
            incident_type=payload.incident_type,
            latitude=payload.latitude,
            longitude=payload.longitude,
            description=payload.description,
            travel_pass_id=payload.travel_pass_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "incident_id": incident.id,
        "status": incident.status,
        "assigned_node": incident.assigned_node_id,
        "estimated_response_minutes": incident.estimated_response_minutes,
        "trusted_contacts_notified": incident.trusted_contacts_notified,
        "escalation": {
            "emergency_number": "112",
            "message": "SOS recorded. Use 112 immediately if there is an immediate threat to life.",
        },
        "timeline": incident.timeline,
    }


@app.get("/api/incidents/{incident_id}")
def get_incident(incident_id: str):
    incident = store.incidents.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.patch("/api/incidents/{incident_id}/status")
def update_incident_status(incident_id: str, payload: IncidentStatusRequest):
    try:
        incident = network.update_status(
            incident_id=incident_id,
            status=payload.status,
            note=payload.note,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return incident


@app.post("/api/subscriptions", status_code=201)
def create_subscription(payload: SubscriptionRequest):
    if payload.user_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")

    subscription_id = f"sub_{payload.user_id[-6:]}_{len(store.subscriptions) + 1}"
    subscription = Subscription(
        id=subscription_id,
        user_id=payload.user_id,
        plan=payload.plan,
    )
    store.subscriptions[subscription_id] = subscription
    return subscription
