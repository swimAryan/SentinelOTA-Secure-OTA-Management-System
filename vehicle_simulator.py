
import time


class Vehicle:

    def __init__(self, vehicle_id, model, version):
        self.vehicle_id = vehicle_id
        self.model = model
        self.version = version

    def install_update(self, new_version, simulate_failure=False):

        old_version = self.version

        print(f"\nVehicle: {self.vehicle_id}")
        print(f"Current Version: {old_version}")
        print(f"Target Version: {new_version}")

        print("Downloading update (simulation)...")
        time.sleep(1)

        print("Security verification (simulation)...")
        time.sleep(1)

        print("Installing update (simulation)...")
        time.sleep(1)

        if simulate_failure:
            print("Installation failed!")
            print("Rollback successful!")

            return {
                "vehicle_id": self.vehicle_id,
                "old_version": old_version,
                "new_version": old_version,
                "status": "Failed",
                "message": "Installation failed. Rollback successful."
            }

        self.version = new_version

        print("Update successful!")

        return {
            "vehicle_id": self.vehicle_id,
            "old_version": old_version,
            "new_version": self.version,
            "status": "Successful",
            "message": "Software updated successfully."
        }
