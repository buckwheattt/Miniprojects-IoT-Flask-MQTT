# IoT Miniprojects – Flask Web Application with MQTT, SQLite, and Docker
This repository contains a series of interconnected IoT miniprojects developed as part of a university course. The goal was to iteratively build a full-featured IoT web application using Flask, with features like real-time data monitoring, REST API, database integration, MQTT communication, deployment, and containerization.
###All core and bonus tasks were implemented.

## 🚀 Project Overview
Each miniproject expands the functionality of the application:

### 🔹 MP01 – Flask App with Simulated Sensor Data
Built with Flask + Bootstrap

Pages: Dashboard, Login, Registration

Dashboard features:

Display of latest temperature value with timestamp

Table of last N measurements (parameterized)

Delete oldest measurement button

Graph of measured data (BONUS)

Handled edge cases (empty data, invalid parameters, etc.)

### 🔹 MP02 – SQLite + REST API Integration
Replaced simulated data with SQLite database (tables: Data, Users)

Implemented secure registration & login

Added REST API with endpoints:

Add new temperature

Get latest / by ID

Delete oldest / by ID (auth required)

Get all values with optional sorting (BONUS)

API endpoints organized in separate file (api_routes.py)

### 🔹 MP03 – Raspberry Pi Pico W + MQTT (One-Way)
Programmed Pico W to send temperature via MQTT

Server receives data and stores it in SQLite

Dashboard shows:

Measured timestamp

Sent timestamp

Received timestamp

Implemented MQTT QoS level 1 (BONUS)

### 🔹 MP04 – Two-Way MQTT Communication
Bi-directional MQTT added

Web interface controls:

Start/stop measuring

Turn LED on/off

Live status indicators

User can set custom measurement period (BONUS)

### 🔹 MP05 – Production Deployment
Deployed Flask app using WSGI (e.g., Gunicorn / Waitress)

Configured HTTPS using self-signed certificate

Implemented structured logging (DEBUG to CRITICAL)

Created /health endpoint with status info (JSON)

Added API rate-limiting with proper headers (BONUS)

### 🔹 MP06 – Docker Virtualization
Multi-stage Dockerfile for secure production build

docker-compose setup:

Flask app

InfluxDB

MQTT broker

Healthchecks for containers

Persistent data storage using Docker volumes (BONUS)

## 🛠 Technologies Used
Python (Flask, SQLite, MQTT, Requests)

Bootstrap (Frontend)

Raspberry Pi Pico W + MicroPython

Mosquitto MQTT Broker

Docker & Docker Compose

InfluxDB (used in Docker stage)

WSGI (Gunicorn / Waitress)

TLS/SSL (self-signed certificate)

## 📎 Notes
All virtual environments and unnecessary files are excluded via .gitignore

Dependencies are listed in requirements.txt

MQTT credentials and certificates are stored securely and ignored from Git

Tested on Linux (WSL) and Windows
