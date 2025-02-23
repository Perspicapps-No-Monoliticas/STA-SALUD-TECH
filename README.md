# SaludTech de Los Alpes

## General Description

SaludTech de Los Alpes is a microservices-based project designed to handle data ingestion, cleaning, anonimizaitiona and tagging from various data sources. The project leverages Apache Pulsar for messaging and FastAPI for building the API. The project also includes a PostgreSQL database for storing ingested data and uses Docker Compose for container orchestration.

## Instructions for Running the Current Docker Compose

To run the project using Docker Compose, follow these steps:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/your-repo/STA-SALUD-TECH.git
    cd STA-SALUD-TECH
    ```

2. **Create Necessary Directories**:
Only if running unbut
    ```sh
    sudo mkdir -p ./data/zookeeper ./data/bookkeeper
    sudo chown -R 10000 data
    ```

3. **Start Docker Compose**:
    ```sh
    docker-compose up -d
    ```

4. **Check the Status of the Services**:
    ```sh
    docker-compose ps
    ```

5. **Access the API**:
    The API will be available at `http://localhost:8000`.

## API Documentation

### Ingestion

#### Create Data Source

- **Endpoint**: `POST /ingestion/data-sources`
- **Request Body**:
    ```json
    {
        "name": "who",
        "description": "testing",
        "type": "POSTGRES",
        "credentials": {
            "payload": {
                "DB_USER": "DB_USER",
                "DB_PASSWORD": "DB_PASSWORD",
                "DB_HOST": "DB_HOST",
                "DB_PORT": "DB_PORT",
                "DB_NAME": "DB_NAME"
            },
            "type": "PASSWORD"
        },
        "provider_id": "afd19370-3387-4b24-9604-1ffe43afe91f"
    }
    ```

#### List All Data Sources

- **Endpoint**: `GET /ingestion/data-sources`
- **Query Parameters**:
    - `limit` (optional): Number of results to return (default: 100)
    - `page` (optional): Page number to return (default: 1)

#### Get Data Source Detail

- **Endpoint**: `GET /ingestion/data-sources/:id`
- **Path Parameters**:
    - `id`: UUID of the data source

### Health

#### Check Health

- **Endpoint**: `GET /health`
- **Response**:
    ```json
    {
        "status": "healthy"
    }
    ```

## Postman Collection

You can import the provided Postman collection `salutech.postman_collection.json` to test the API endpoints. The collection includes the following requests:

- **Create Data Source**: `POST /ingestion/data-sources`
- **List All Data Sources**: `GET /ingestion/data-sources`
- **Get Data Source Detail**: `GET /ingestion/data-sources/:id`
- **Check Health**: `GET /ingestion/health`

To import the collection:

1. Open Postman.
2. Click on `Import` in the top left corner.
3. Select the `salutech.postman_collection.json` file.
4. The collection will be imported and available for use.

## Additional Information

- **Docker Compose File**: The `docker-compose.yml` file sets up the necessary services including Zookeeper, Pulsar, PostgreSQL, and the FastAPI application.
- **Environment Variables**: Ensure that the environment variables in the `docker-compose.yml` file are correctly set for your environment.

For more detailed information, please refer to the project documentation or contact the project maintainers.
