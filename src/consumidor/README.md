# README.md

# STA-SALUD-TECH

## Overview
STA-SALUD-TECH is a Python application that subscribes to Pulsar topics and processes incoming messages related to health events. This project is designed to run in a Docker container for easy deployment and management.

## Project Structure
```
sta-salud-tech
├── src
│   └── consumidor
│       ├── __init__.py
│       ├── consumidores.py
│       └── v1
│           ├── __init__.py
│           └── eventos.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Requirements
- Docker
- Docker Compose

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sta-salud-tech
   ```

2. Build the Docker image:
   ```bash
   docker-compose build
   ```

3. Run the application:
   ```bash
   docker-compose up
   ```

## Usage
The application will subscribe to the `eventos-reserva` topic and process incoming messages. Ensure that the Pulsar broker is running and accessible.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.