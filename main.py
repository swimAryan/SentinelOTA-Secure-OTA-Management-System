
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from vehicle_simulator import Vehicle
from database import get_connection
from psycopg.rows import dict_row


app = FastAPI(title="Secure OTA Management System")

BASE_DIR = Path(__file__).resolve().parent

vehicles = {
    "VEH001": Vehicle("VEH001", "Demo EV A", "1.0"),
    "VEH002": Vehicle("VEH002", "Demo EV B", "1.1"),
    "VEH003": Vehicle("VEH003", "Demo EV C", "1.0")
}


class UpdateRequest(BaseModel):
    vehicle_id: str
    new_version: str
    simulate_failure: bool = False

class VehicleRegistration(BaseModel):
    vehicle_id: str
    model: str
    version: str
    status: str = "Online"

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")



@app.get("/api/vehicles")
def get_vehicles():

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT vehicle_id, model, version, status
                FROM vehicles
                ORDER BY vehicle_id
            """)

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "model": row[1],
            "version": row[2],
            "status": row[3]
        }
        for row in rows
    ]




@app.post("/api/deploy")
def deploy_update(request: UpdateRequest):

    # Step 1: Connect to PostgreSQL
    with get_connection() as conn:

        with conn.cursor(row_factory=dict_row) as cursor:

            # Step 2: Find vehicle in database
            cursor.execute("""
                SELECT vehicle_id, model, version, status
                FROM vehicles
                WHERE vehicle_id = %s
                FOR UPDATE
            """, (request.vehicle_id,))

            vehicle_data = cursor.fetchone()

            if vehicle_data is None:
                raise HTTPException(
                    status_code=404,
                    detail="Vehicle not found"
                )

            # Step 3: Check vehicle status
            if vehicle_data["status"] != "Online":
                raise HTTPException(
                    status_code=400,
                    detail="Vehicle is offline"
                )

            # Step 4: Validate software version
            def parse_version(version):
                try:
                    parts = version.split(".")

                    if not parts or not all(
                        part.isascii() and part.isdecimal()
                        for part in parts
                    ):
                        raise ValueError()

                    return tuple(int(part) for part in parts)

                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid software version"
                    )

            from itertools import zip_longest

            new_parts = parse_version(request.new_version)
            old_parts = parse_version(vehicle_data["version"])

            comparison = next(
                (
                    1 if new > old else -1
                    for new, old in zip_longest(
                        new_parts,
                        old_parts,
                        fillvalue=0
                    )
                    if new != old
                ),
                0
            )

            if comparison <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="New version must be higher than current version"
                )

            # Step 5: Create simulated vehicle
            vehicle = Vehicle(
                vehicle_id=vehicle_data["vehicle_id"],
                model=vehicle_data["model"],
                version=vehicle_data["version"]
            )

            # Step 6: Run Python simulation
            result = vehicle.install_update(
                new_version=request.new_version,
                simulate_failure=request.simulate_failure
            )

            # Step 7: Save updated version if successful
            if result["status"] == "Successful":

                cursor.execute("""
                    UPDATE vehicles
                    SET version = %s
                    WHERE vehicle_id = %s
                """, (
                    result["new_version"],
                    request.vehicle_id
                ))

            # Step 8: Save deployment history
            cursor.execute("""
                INSERT INTO deployments
                    (vehicle_id, old_version, new_version, status)
                VALUES (%s, %s, %s, %s)
            """, (
                request.vehicle_id,
                result["old_version"],
                request.new_version,
                result["status"]
            ))

        # Step 9: Save changes permanently
        conn.commit()

    return result



@app.get("/api/deployments")
def get_deployments():

    with get_connection() as conn:

        with conn.cursor(row_factory=dict_row) as cursor:

            cursor.execute("""
                SELECT
                    id,
                    vehicle_id,
                    old_version,
                    new_version,
                    status,
                    created_at
                FROM deployments
                ORDER BY id DESC
            """)

            rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "vehicle_id": row["vehicle_id"],
            "old_version": row["old_version"],
            "new_version": row["new_version"],
            "status": row["status"],
            "created_at": row["created_at"].isoformat()
                if row["created_at"] else None
        }
        for row in rows
    ]


@app.post("/api/vehicles", status_code=201)
def register_vehicle(vehicle: VehicleRegistration):

    if not all([
        vehicle.vehicle_id.strip(),
        vehicle.model.strip(),
        vehicle.version.strip()
    ]):
        raise HTTPException(
            status_code=400,
            detail="Vehicle ID, model and version are required"
        )

    if vehicle.status not in ("Online", "Offline"):
        raise HTTPException(
            status_code=400,
            detail="Status must be Online or Offline"
        )

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO vehicles
                        (vehicle_id, model, version, status)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (vehicle_id) DO NOTHING
                    RETURNING vehicle_id
                """, (
                    vehicle.vehicle_id.strip(),
                    vehicle.model.strip(),
                    vehicle.version.strip(),
                    vehicle.status
                ))

                inserted = cursor.fetchone()

                if inserted is None:
                    raise HTTPException(
                        status_code=409,
                        detail="Vehicle ID already exists"
                    )

    except HTTPException:
        raise

    return {
        "message": "Vehicle registered successfully",
        "vehicle_id": vehicle.vehicle_id
    }