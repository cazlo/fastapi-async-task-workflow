# Local Deployment Workflow

## Dev Profile

Intended for local testing activities.
Has local dev only features like 
- file watching and reload of the server
- pytest installed
- linting and formating tools installed


=== "C4 PlantUml"

      ``` plantuml
      @startuml Development Environment
      !include <C4/C4_Container>
      !include <tupadr3/devicons/python>
      !include <tupadr3/devicons/postgresql>
      !include <tupadr3/devicons/redis>
      !include <tupadr3/devicons2/rabbitmq_original>
      !include <tupadr3/font-awesome/server>
      !include <tupadr3/font-awesome/cogs>
      !include <tupadr3/font-awesome/database>
      !include <tupadr3/font-awesome-6/clock>
      !include <tupadr3/font-awesome/book>
      !include <tupadr3/material/storage>
      
      LAYOUT_WITH_LEGEND()
      
      Person(user, "User", "System user")
      
      Boundary(docker_compose, "Docker Compose Environment - Development Profile") {
          Container(caddy, "Caddy Reverse Proxy", "Caddy:alpine", "Handles HTTP/HTTPS requests, routes to appropriate services", $sprite="server")
          
          Container(fastapi_dev, "FastAPI Server (Dev)", "Python, Uvicorn", "API server with hot reload for development", $sprite="python")
          
          Container(celery_beat, "Celery Beat", "Python, Celery", "Schedules periodic tasks", $sprite="clock")
          
          ContainerDb(postgres, "PostgreSQL", "Postgres 17", "Stores application data and Celery results", $sprite="postgresql")
          ContainerDb(valkey, "Valkey", "Valkey 8.1", "In-memory cache (Redis API compatible)", $sprite="redis")
          ContainerDb(rabbitmq, "RabbitMQ", "RabbitMQ 3.13", "Message broker for task queue", $sprite="rabbitmq_original")
          ContainerDb(minio, "MinIO", "MinIO", "Object storage for files", $sprite="storage")
          
          Container(db_migrator, "DB Migrator", "Python, Alembic", "Handles database migrations", $sprite="cogs")
          Container(docs, "Documentation Server", "MkDocs", "Serves project documentation", $sprite="book")
      }
      
      Rel(user, caddy, "Uses", "HTTP/HTTPS")
      Rel(caddy, fastapi_dev, "Routes requests to", "HTTP")
      Rel(caddy, minio, "Routes storage requests to", "HTTP")
      
      Rel(fastapi_dev, postgres, "Reads/writes data", "SQL/asyncpg")
      Rel(fastapi_dev, valkey, "Caches data", "Redis protocol")
      Rel(fastapi_dev, rabbitmq, "Publishes tasks", "AMQP")
      Rel(fastapi_dev, minio, "Stores/retrieves files", "S3 API")
      
      Rel(celery_beat, postgres, "Schedules tasks in", "SQL/asyncpg")
      Rel(celery_beat, rabbitmq, "Publishes scheduled tasks", "AMQP")
      
      Rel(db_migrator, postgres, "Migrates schema", "SQL/alembic")
      
      Lay_D(caddy, fastapi_dev)
      Lay_R(fastapi_dev, postgres)
      Lay_R(postgres, valkey)
      Lay_R(valkey, rabbitmq)
      Lay_R(rabbitmq, minio)
      Lay_D(fastapi_dev, celery_beat)
      Lay_D(postgres, db_migrator)
      Lay_R(db_migrator, docs)
      
      @enduml
      ```

=== "Mermaid"

    ``` mermaid
    flowchart LR
        subgraph "Development Environment"
            direction TB
            
            User((User))
            
            subgraph "Web Interface"
                CaddyProxy["`Caddy Reverse Proxy
      (caddy_reverse_proxy)`"]
            end
            
            subgraph "API Layer"
                FastAPI["`FastAPI Server
      (fastapi_server_dev)
      Uvicorn with hot reload`"]
            end
            
            subgraph "Task Processing"
                CeleryBeat["`Celery Beat
      (celery_beat)
      Schedules tasks`"]
                %% Note: celery_worker is excluded from dev profile
            end
            
            subgraph "Data Storage"
                PostgreSQL["`PostgreSQL
      (database)\nApplication data
      Celery results`"]
                Valkey["`Valkey
      (redis_server)
      Caching layer`"]
                RabbitMQ["`RabbitMQ
      (rabbitmq)
      Message broker`"]
                MinIO["`MinIO
      (minio_server)
      Object storage`"]
            end
            
            subgraph "Database Migration"
                DBMigrator["`DB Migrator
      (db_migrator)
      Alembic`"]
            end
            
            subgraph "Documentation"
                Docs["`Documentation Server
      (docs)
      MkDocs`"]
            end
            
            %% Connections
            User --> CaddyProxy
            CaddyProxy --> FastAPI
            CaddyProxy --> MinIO
            
            FastAPI --> PostgreSQL
            FastAPI --> Valkey
            FastAPI --> RabbitMQ
            FastAPI --> MinIO
            
            CeleryBeat --> PostgreSQL
            CeleryBeat --> RabbitMQ
            
            DBMigrator --> PostgreSQL
            
            %% Dependencies
            PostgreSQL -.-> DBMigrator
            PostgreSQL -.-> FastAPI
            PostgreSQL -.-> CeleryBeat
            RabbitMQ -.-> CeleryBeat
        end
    ```

## Prod profile

This is a much more prod like system state, suitable for integration testing activities of a configuration before deployment into a k8s cluster.

=== "C4 PlantUML"

      ```plantuml
      @startuml Production Environment
      !include <C4/C4_Container>
      !include <tupadr3/devicons/python>
      !include <tupadr3/devicons/postgresql>
      !include <tupadr3/devicons/redis>
      !include <tupadr3/devicons2/rabbitmq_original>
      !include <tupadr3/font-awesome/server>
      !include <tupadr3/font-awesome/cogs>
      !include <tupadr3/font-awesome/database>
      !include <tupadr3/font-awesome-6/clock>
      !include <tupadr3/material/storage>
      
      LAYOUT_WITH_LEGEND()
      
      Person(user, "User", "System user")
      
      Boundary(docker_compose, "Docker Compose Environment - Production Profile") {
          Container(caddy, "Caddy Reverse Proxy", "Caddy:alpine", "Handles HTTP/HTTPS requests, routes to appropriate services", $sprite="server")
          
          Container(fastapi_prod, "FastAPI Server (Prod)", "Python, Gunicorn with Uvicorn workers", "Production API server with multiple workers", $sprite="python")
          
          Container(celery_beat, "Celery Beat", "Python, Celery", "Schedules periodic tasks", $sprite="clock")
          Container(celery_worker, "Celery Worker", "Python, Celery", "Processes asynchronous tasks", $sprite="cogs")
          
          ContainerDb(postgres, "PostgreSQL", "Postgres 17", "Stores application data and Celery results", $sprite="postgresql")
          ContainerDb(valkey, "Valkey", "Valkey 8.1", "In-memory cache (Redis API compatible)", $sprite="redis")
          ContainerDb(rabbitmq, "RabbitMQ", "RabbitMQ 3.13", "Message broker for task queue", $sprite="rabbitmq_original")
          ContainerDb(minio, "MinIO", "MinIO", "Object storage for files", $sprite="storage")
          
          Container(db_migrator, "DB Migrator", "Python, Alembic", "Handles database migrations", $sprite="cogs")
      }
      
      Rel(user, caddy, "Uses", "HTTP/HTTPS")
      Rel(caddy, fastapi_prod, "Routes requests to", "HTTP")
      Rel(caddy, minio, "Routes storage requests to", "HTTP")
      
      Rel(fastapi_prod, postgres, "Reads/writes data", "SQL/asyncpg")
      Rel(fastapi_prod, valkey, "Caches data", "Redis protocol")
      Rel(fastapi_prod, rabbitmq, "Publishes tasks", "AMQP")
      Rel(fastapi_prod, minio, "Stores/retrieves files", "S3 API")
      
      Rel(celery_beat, postgres, "Schedules tasks in", "SQL/asyncpg")
      Rel(celery_beat, rabbitmq, "Publishes scheduled tasks", "AMQP")
      
      Rel(celery_worker, postgres, "Reads/writes data", "SQL/asyncpg")
      Rel(celery_worker, rabbitmq, "Consumes tasks", "AMQP")
      Rel(celery_worker, minio, "Stores/retrieves files", "S3 API")
      
      Rel(db_migrator, postgres, "Migrates schema", "SQL/alembic")
      
      Lay_D(caddy, fastapi_prod)
      Lay_R(fastapi_prod, postgres)
      Lay_R(postgres, valkey)
      Lay_R(valkey, rabbitmq)
      Lay_R(rabbitmq, minio)
      Lay_D(fastapi_prod, celery_beat)
      Lay_D(celery_beat, celery_worker)
      Lay_D(postgres, db_migrator)
      
      @enduml
      ```

=== "Mermaid"

      ```mermaid
      flowchart TB
          subgraph "Production Environment"
              direction TB
              
              User((User))
              
              subgraph "Web Interface"
                  CaddyProxy["Caddy Reverse Proxy\n(caddy_reverse_proxy)"]
              end
              
              subgraph "API Layer"
                  FastAPI["FastAPI Server\n(fastapi_server_prd)\nGunicorn with Uvicorn workers"]
              end
              
              subgraph "Task Processing"
                  CeleryBeat["Celery Beat\n(celery_beat)\nSchedules tasks"]
                  CeleryWorker["Celery Worker\n(celery_worker)\nProcesses tasks"]
              end
              
              subgraph "Data Storage"
                  PostgreSQL["PostgreSQL\n(database)\nApplication data\nCelery results"]
                  Valkey["Valkey\n(redis_server)\nCaching layer"]
                  RabbitMQ["RabbitMQ\n(rabbitmq)\nMessage broker"]
                  MinIO["MinIO\n(minio_server)\nObject storage"]
              end
              
              subgraph "Database Migration"
                  DBMigrator["DB Migrator\n(db_migrator)\nAlembic"]
              end
              
              %% Connections
              User --> CaddyProxy
              CaddyProxy --> FastAPI
              CaddyProxy --> MinIO
              
              FastAPI --> PostgreSQL
              FastAPI --> Valkey
              FastAPI --> RabbitMQ
              FastAPI --> MinIO
              
              CeleryBeat --> PostgreSQL
              CeleryBeat --> RabbitMQ
              
              CeleryWorker --> PostgreSQL
              CeleryWorker --> RabbitMQ
              CeleryWorker --> MinIO
              
              DBMigrator --> PostgreSQL
              
              %% Dependencies
              PostgreSQL -.-> DBMigrator
              PostgreSQL -.-> FastAPI
              PostgreSQL -.-> CeleryBeat
              PostgreSQL -.-> CeleryWorker
              RabbitMQ -.-> CeleryBeat
              RabbitMQ -.-> CeleryWorker
          end
      
      ```

### Key Differences Between Development and Production Environments:
1. **FastAPI Server**:
    - Development: Uses Uvicorn with hot reload for faster development
    - Production: Uses Gunicorn with multiple Uvicorn workers for better performance and reliability

2. **Celery Worker**:
    - Development: Not included to facilitate test coverage of tasks
    - Production: Included to process asynchronous tasks

3. **Documentation Server**:
    - Development: Available for easy access to documentation
    - Production: Not included as it's not needed in production

Both environments use the same data storage components:
- PostgreSQL for application data and Celery result backend
- Valkey (Redis API-compatible) for caching
- RabbitMQ for message broker
- MinIO for object storage

The database migration component (db_migrator) is present in both environments to ensure the database schema is up-to-date before the application starts.
