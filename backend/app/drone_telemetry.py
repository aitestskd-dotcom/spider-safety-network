"""Opt-in MAVSDK telemetry reader. No flight or actuator commands."""
import argparse
import asyncio
import json
import math
from datetime import datetime, timezone


def validate_position(latitude, longitude, altitude):
    values = (latitude, longitude, altitude)
    if not all(math.isfinite(value) for value in values):
        raise ValueError('Non-finite telemetry')
    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        raise ValueError('Coordinates out of bounds')
    return {'latitude': latitude, 'longitude': longitude, 'absolute_altitude_m': altitude}


async def read_position(address, timeout_seconds=20.0):
    if not address or timeout_seconds <= 0:
        raise ValueError('Address and positive timeout required')
    from mavsdk import System

    drone = System()

    async def collect():
        await drone.connect(system_address=address)
        async for state in drone.core.connection_state():
            if state.is_connected:
                break
        else:
            raise ConnectionError('Connection stream ended')
        async for position in drone.telemetry.position():
            result = validate_position(position.latitude_deg, position.longitude_deg, position.absolute_altitude_m)
            result['received_at'] = datetime.now(timezone.utc).isoformat()
            result['source'] = 'mavsdk'
            result['position_validity'] = 'bounds_checked_only'
            return result
        raise ConnectionError('Position stream ended')

    return await asyncio.wait_for(collect(), timeout=timeout_seconds)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--address', required=True, help='Explicit MAVSDK system address; use a simulator first')
    parser.add_argument('--timeout', type=float, default=20.0)
    args = parser.parse_args()
    try:
        result = asyncio.run(read_position(args.address, args.timeout))
    except (TimeoutError, ConnectionError, ValueError, ImportError) as error:
        parser.exit(1, f'Telemetry unavailable: {error}\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
