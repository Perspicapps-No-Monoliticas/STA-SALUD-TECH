# Medical Image Anonymizer - DDD with FastAPI

This project is a Domain-Driven Design (DDD) implementation of a medical image anonymization service using FastAPI.

## Architecture

The project follows a DDD architecture with these main components:

- **Application Layer**: Contains the application services and orchestrates the domain.
  - Pipeline: Handles the anonymization workflow
  - Events: Application-level events

- **Domain Layer**: Contains the business logic, entities, and domain events.
  - Entities: Medical images and metadata
  - Events: Domain events that capture important business occurrences

- **Infrastructure Layer**: Provides implementations for external services.
  - Tokenizer: Generates secure tokens for anonymized images
  - Script Anonymizer: Traditional rule-based anonymization
  - AI Model Anonymizer: Machine learning-based anonymization
  - Broker Adapter: Interface to message brokers

- **Dispatcher**: Mediator pattern implementation for event handling.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The application will be available at http://localhost:8000.

## API Endpoints

- `POST /anonymize/`: Upload and anonymize a medical image
  - Parameters:
    - `file`: The image file to anonymize
    - `use_ai`: Boolean to indicate whether to use AI-based anonymization (default: false)

- `GET /health`: Health check endpoint

## Development

To run tests:
```bash
pytest
```

## Integration with Other Systems

This system uses a mediator pattern to coordinate events across the application. External systems can be integrated through the broker adapter in the infrastructure layer.