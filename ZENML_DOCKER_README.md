# Running ZenML with Docker Compose

This setup allows you to run ZenML with MySQL as the backend database and local artifact storage using Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. **Start the services**

   ```bash
   docker-compose up -d
   ```

2. **Verify the services are running**

   ```bash
   docker-compose ps
   ```

3. **Connect to ZenML**

   ```bash
   zenml connect --url http://localhost:8237
   ```

4. **Verify the connection**
   ```bash
   zenml status
   ```

## Accessing the ZenML Dashboard

Open your web browser and navigate to:

```
http://localhost:8237
```

Default credentials:

- Username: default
- Password: zenml

## Stopping the Services

To stop the services:

```bash
docker-compose down
```

## Data Persistence

- Database data is stored in a Docker volume named `mysql_data`
- Artifacts are stored in a Docker volume named `zenml_artifacts`

## Configuration

You can modify the following environment variables in `docker-compose.yml`:

- `ZENML_DEFAULT_USER_NAME`: Default admin username
- `ZENML_DEFAULT_USER_PASSWORD`: Default admin password
- `MYSQL_ROOT_PASSWORD`: MySQL root password
- `MYSQL_PASSWORD`: MySQL user password
