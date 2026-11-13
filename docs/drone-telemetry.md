# Opt-in drone telemetry integration

## Scope

This module uses the real MAVSDK Python interface to connect to a MAVLink-compatible vehicle or simulator and retrieve one position sample. It is not a simulator implementation and has not been validated against your hardware. It is not yet wired into the web dashboard or SOS workflow. No flight, arming, landing, payload-release, mission-upload, or actuator commands are implemented. MAVSDK still establishes a protocol connection; this is not a passive radio sniffer.

## Setup

Use a separate development environment and follow the MAVSDK Python installation instructions for your operating system and processor: https://mavsdk.mavlink.io/main/en/python/quickstart.html . Install the optional dependency with `pip install mavsdk`. This change deliberately does not modify the application's existing requirements. Pin an appropriately tested MAVSDK version before deployment.

From the backend directory, with a locally configured PX4/ArduPilot simulator exposing the corresponding endpoint:

```bash
python -m app.drone_telemetry --address udpin://0.0.0.0:14540 --timeout 20
```

Select the actual serial, UDP, or TCP endpoint using the documentation for your installed MAVSDK version and vehicle. Do not expose MAVLink ports to the public internet. Use only authorised equipment and isolated networks. A successful position sample does not establish GPS fix quality, battery health, airworthiness, flight authorisation, or response availability. Output timestamps indicate receipt time, not sensor measurement time. Telemetry coordinates may be sensitive; do not publish them.

## Verification checklist

1. Verify coordinate validation with valid, invalid, and non-finite values.
2. Verify timeout behaviour with an unavailable endpoint.
3. Connect to software-in-the-loop and compare output with the simulator ground station.
4. With a qualified operator, verify telemetry on a secured, propeller-removed test vehicle.
5. Add automated adapter tests and integration tests before enabling dashboard access.

No automated tests or physical hardware tests are claimed by this change.

## Next integration decisions

Identify manufacturer, aircraft model, flight controller, firmware, docking station, telemetry link, and desired deployment environment. DJI Cloud API is a different integration and is intentionally not represented by a placeholder here. Its supported hardware, authentication, MQTT schemas and command permissions must be verified against the selected hardware and official DJI documentation.

Flight control, dispatch automation, payments, real notifications, 112 connectivity and insurance activation remain outside this adapter. They require separate implementation, testing, approval and partner arrangements. Do not display simulated notifications, insurance eligibility, or response-time estimates as verified services.
