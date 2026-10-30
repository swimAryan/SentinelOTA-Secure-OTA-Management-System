# 🚗 SentinelOTA
### Secure Over-the-Air (OTA) Software Update Management System for Software-Defined Vehicles

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📌 Project Overview

**SentinelOTA** is a simulation-based Secure Over-the-Air (OTA) Software Update Management System designed for Software-Defined Vehicles (SDVs).

The project demonstrates how vehicle software updates can be managed remotely through a centralized web-based dashboard without requiring physical automotive hardware.

The system provides vehicle monitoring, software release management, OTA deployment simulation, installation failure handling, and backend database integration.

This project is being developed as part of a **B.Tech Computer Science and Engineering Major Project**.

---

## 🎯 Project Objectives

- Develop a centralized OTA software update management platform.
- Manage registered vehicles and their software versions.
- Simulate remote software installation on virtual vehicles.
- Validate software version compatibility before deployment.
- Demonstrate installation failure and basic rollback behavior.
- Store vehicle information using PostgreSQL.
- Provide a user-friendly dashboard for monitoring OTA operations.
- Explore secure software update mechanisms for connected vehicles.

---

## ✨ Features

### 🚘 Vehicle Management
- View registered vehicles.
- Monitor vehicle software versions.
- Identify online and offline vehicles.
- Register vehicles through REST APIs.

### 📦 Software Update Management
- Create simulated software releases.
- Specify software versions.
- Configure compatible vehicle models.
- Select releases for OTA deployment.

### 🚀 OTA Deployment Simulation
- Deploy simulated software updates to virtual vehicles.
- Validate software version requirements.
- Check vehicle availability.
- Simulate downloading and installing updates.
- Display deployment progress and results.

### 🔄 Failure Simulation and Rollback
- Simulate software installation failures.
- Preserve the previous software version when installation fails.
- Demonstrate basic rollback behavior.

### 🔐 Security Monitoring
- Demonstration interface for tampered software detection.
- Demonstration interface for invalid digital signatures.
- Planned integration of SHA-256 hashing and Ed25519 digital signatures.

**Note:** Cryptographic security checks are not yet implemented. Current security demonstrations are simulation-only.

### 🗄️ Database Integration
- PostgreSQL database connectivity.
- Vehicle information storage.
- Database-backed vehicle retrieval.
- Deployment history database schema and API development.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Database Connectivity | Psycopg |
| API Documentation | Swagger UI |
| Development Environment | Visual Studio Code |
| Database Management | pgAdmin 4 |
| Version Control | Git and GitHub |

---

## 🏗️ System Architecture

```text
                +-----------------------+
                |     Web Dashboard     |
                | HTML / CSS / JS       |
                +-----------+-----------+
                            |
                            | HTTP REST API
                            |
                +-----------v-----------+
                |     FastAPI Backend   |
                |        Python         |
                +-----------+-----------+
                            |
              +-------------+-------------+
              |                           |
    +---------v----------+      +---------v----------+
    | Vehicle Simulator  |      | PostgreSQL Database|
    | Python             |      | Vehicle Records     |
    | Update Simulation  |      | Deployment History  |
    +--------------------+      +--------------------+
```

---

## 📂 Project Structure

```text
SentinelOTA/
│
├── index.html
├── main.py
├── vehicle_simulator.py
├── database.py
├── .env.example
├── .gitignore
├── README.md
└── sql.sql
```

**Important:** `.env.example` should contain placeholder database credentials only. Never upload your actual `.env` file.

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd SentinelOTA-Secure-OTA-Management-System
```

### 2. Install Dependencies

Ensure Python and PostgreSQL are installed.

```bash
pip install fastapi uvicorn psycopg[binary] python-dotenv
```

### 3. Configure PostgreSQL

Create a PostgreSQL database named:

```sql
CREATE DATABASE secure_ota_db;
```

Connect to `secure_ota_db` using pgAdmin and execute the SQL statements in `sql.sql` to create the required tables.

### 4. Configure Environment Variables

Create a `.env` file in the project directory:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=secure_ota_db
DB_USER=postgres
DB_PASSWORD=your_database_password
```

Replace `your_database_password` with your local PostgreSQL password.

### 5. Start the Backend Server

```bash
python -m uvicorn main:app --reload
```

### 6. Open the Dashboard

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

### 7. Access API Documentation

```text
http://127.0.0.1:8000/docs
```

---

## 🔗 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Open the web dashboard |
| GET | `/api/vehicles` | Retrieve registered vehicles |
| POST | `/api/vehicles` | Register a new vehicle |
| POST | `/api/deploy` | Initiate simulated OTA deployment |
| GET | `/api/deployments` | Retrieve stored deployment records |

---

## 🧪 Example: Vehicle Registration

A vehicle can be registered through the FastAPI Swagger UI.

**Endpoint:**

```http
POST /api/vehicles
```

**Example request:**

```json
{
  "vehicle_id": "VEH004",
  "model": "Demo EV D",
  "version": "1.0",
  "status": "Online"
}
```

After successful database-backed registration, the vehicle should appear in the vehicle retrieval API and dashboard.

---

## 🔄 OTA Update Workflow

```text
Select Vehicle
      |
      v
Select Software Release
      |
      v
Check Vehicle Availability
      |
      v
Validate Software Version
      |
      v
Simulate Download
      |
      v
Simulate Verification
      |
      v
Simulate Installation
      |
      +------------------+
      |                  |
      v                  v
   Success             Failure
      |                  |
      v                  v
Update Version      Retain Old Version
      |                  |
      +---------+--------+
                |
                v
        Deployment Result
```

The current prototype simulates OTA installation rather than transferring or installing real automotive firmware.

---

## 🧪 Testing and Validation

Initial testing has been conducted using FastAPI Swagger UI, the web dashboard, and PostgreSQL.

### Observed Results

- The vehicle retrieval API successfully returned registered vehicle records.
- The vehicle registration API returned HTTP 201 for a valid registration request.
- PostgreSQL connectivity was successfully established.
- The deployment interface displayed validation errors for incompatible vehicle models.
- Deployment requests using non-incremental software versions were rejected.

### Testing in Progress

- End-to-end vehicle registration persistence.
- Successful database-backed OTA deployment.
- Persistent deployment history verification.
- Installation failure and rollback validation.
- Cryptographic security verification.

---

## 🚧 Current Development Status

**Status: Functional Prototype — Development in Progress**

The current implementation includes a web dashboard, FastAPI backend, Python vehicle simulator, and PostgreSQL integration.

The project is not yet a production-ready automotive OTA solution.

### Planned Enhancements

- SHA-256 software package integrity verification.
- Ed25519 digital signature verification.
- Secure firmware package management.
- Authentication and role-based access control.
- Improved deployment history synchronization.
- Enhanced rollback and recovery mechanisms.
- Comprehensive automated testing.

---

## 🎓 Academic Information

**Project Title:** Secure Over-the-Air (OTA) Software Update Management System for Software-Defined Vehicles

**Project Name:** SentinelOTA

**Program:** Bachelor of Technology in Computer Science and Engineering

**University:** IILM University

**Project Type:** B.Tech CSE Major Project

---

## ⚠️ Disclaimer

SentinelOTA is an academic simulation prototype intended for educational and research purposes.

It does not currently implement real automotive ECU firmware installation, production-grade cryptographic verification, or safety-critical vehicle update mechanisms.

---

## 📄 License

No license has currently been specified for this repository.
