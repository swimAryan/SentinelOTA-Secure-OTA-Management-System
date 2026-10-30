
CREATE TABLE vehicles (
    vehicle_id VARCHAR(50) PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    version VARCHAR(30) NOT NULL,
    status VARCHAR(20) DEFAULT 'Online'
);

CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    old_version VARCHAR(30) NOT NULL,
    new_version VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id)
);


INSERT INTO vehicles (vehicle_id, model, version, status)
VALUES
    ('VEH001', 'Demo EV A', '1.0', 'Online'),
    ('VEH002', 'Demo EV B', '1.1', 'Online'),
    ('VEH003', 'Demo EV C', '1.0', 'Offline')
ON CONFLICT (vehicle_id) DO NOTHING;

SELECT * FROM vehicles;