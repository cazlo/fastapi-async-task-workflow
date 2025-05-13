---
title: 0003 Use Celery for Asynchronous Task Processing
adr: true
status: accepted
date: "2025-05-11"
decision-makers: []
consulted: []
informed: []
tags:
 - backend
 - tasks
 - performance
 - scalability
---

# Use Celery for Long-Running Asynchronous Task Processing

## Context and Problem Statement

Our application needs to handle various long-running and computationally intensive tasks that would negatively impact API response times if processed synchronously. These include data processing, report generation, external service integration, email notifications, and scheduled operations. We need a robust, reliable, and scalable solution for managing asynchronous task execution that integrates well with our FastAPI backend.

## Decision Drivers

* Need for reliable execution of background tasks without blocking API responses
* Requirement to handle task scheduling, retries, and monitoring
* Support for distributed task processing across multiple workers
* Ability to scale horizontally as workload increases
* Integration capabilities with our existing technology stack
* Support for task prioritization and management
* Need for visibility into task execution status and history
* Robustness in handling system failures and recovery

## Considered Options

* Celery with RabbitMQ/Redis
* FastAPI background tasks
* RQ (Redis Queue)
* Dramatiq
* Apache Airflow
* Homegrown task queue solution

## Decision Outcome

Chosen option: "Celery with RabbitMQ/Redis", because it provides a mature, battle-tested solution for distributed task processing with extensive features for reliability, scalability, and monitoring. Celery's rich ecosystem, flexibility, and integration capabilities with our existing stack make it the most suitable choice for our requirements.

### Consequences

* Good, because Celery offers robust task distribution and management capabilities
* Good, because it provides automatic retries, error handling, and task monitoring
* Good, because it can scale horizontally by adding more worker nodes
* Good, because it supports various message brokers including RabbitMQ and Redis
* Good, because it enables scheduled tasks (via Celery Beat) and periodic job execution
* Neutral, because it has a steeper learning curve compared to simpler alternatives
* Bad, because it adds complexity to the system architecture
* Bad, because it requires additional infrastructure components (message broker, workers)

### Confirmation

Compliance with this ADR will be confirmed through:
1. Implementation of task worker deployments in our Docker/Kubernetes environment
2. Performance testing to validate task processing scalability and reliability
3. Code reviews to ensure proper use of Celery patterns and practices
4. Monitoring of task execution metrics in production

## Pros and Cons of the Options

### Celery with RabbitMQ/Redis

A distributed task queue system for Python with support for multiple message brokers.

* Good, because it's a mature, battle-tested solution with wide industry adoption
* Good, because it provides extensive features for task management, scheduling, and monitoring
* Good, because it supports distributed processing across multiple worker nodes
* Good, because it offers task prioritization, rate limiting, and concurrency control
* Good, because it has excellent integration with FastAPI and SQLAlchemy
* Neutral, because it requires a message broker (RabbitMQ or Redis) as an additional component
* Bad, because it adds operational complexity to the system
* Bad, because it has a steeper learning curve compared to simpler alternatives [[1]](https://www.fullstackpython.com/task-queues.html)

### FastAPI Background Tasks

Built-in background task functionality provided by FastAPI.

* Good, because it's simple and integrated directly into FastAPI
* Good, because it requires no additional infrastructure components
* Good, because it has minimal setup overhead
* Neutral, because it works well for simple, short-running tasks
* Bad, because it lacks advanced features like retries, scheduling, and monitoring
* Bad, because tasks are tied to the web server process and not truly distributed
* Bad, because it doesn't scale well for compute-intensive or high-volume tasks
* Bad, because it offers no persistence or task history

### RQ (Redis Queue)

A simple Python library for queueing jobs and processing them in the background with workers.

* Good, because it's simpler and easier to set up than Celery
* Good, because it has a clean, straightforward API
* Good, because it uses Redis as its only dependency
* Neutral, because it has adequate performance for moderate workloads
* Bad, because it lacks some advanced features Celery provides
* Bad, because it only supports Redis as a broker
* Bad, because it has more limited scaling options compared to Celery
* Bad, because it has fewer monitoring and management tools [[5]](https://stackoverflow.com/questions/13440875/pros-and-cons-to-use-celery-vs-rq)

### Dramatiq

A fast and reliable background task processing library for Python with a focus on simplicity.

* Good, because it's designed to be simpler than Celery while maintaining good performance
* Good, because it has a clean, explicit API
* Good, because it supports both RabbitMQ and Redis as message brokers
* Neutral, because it's gaining popularity but has a smaller community than Celery
* Bad, because it has fewer integrations with third-party tools
* Bad, because it lacks some advanced features Celery provides
* Bad, because it has fewer monitoring and management options

### Apache Airflow

A platform for programmatically authoring, scheduling, and monitoring workflows.

* Good, because it excels at complex, DAG-based workflow orchestration
* Good, because it provides excellent visualization of task dependencies and execution
* Good, because it has robust scheduling capabilities
* Neutral, because it offers a rich web UI for monitoring and management
* Bad, because it's overly complex for simple task queue needs
* Bad, because it's designed for ETL and data workflows rather than general task processing
* Bad, because it requires significantly more resources and infrastructure

### Homegrown Task Queue Solution

A custom-built system for managing background tasks.

* Good, because it can be tailored specifically to our needs
* Good, because it could potentially be simpler than existing solutions
* Neutral, because it gives complete control over implementation details
* Bad, because it would require significant development and maintenance effort
* Bad, because it would lack the maturity and reliability of established solutions
* Bad, because it would need to solve problems that existing tools have already addressed
* Bad, because it would increase the technical debt of the project

## More Information

Celery will be used with Reddis as the message broker for reliability and Postgres for result backend. We'll implement Celery Beat for scheduled tasks and use Flower for monitoring. This choice aligns with our previous decisions to use FastAPI (ADR-0001) and SQLModel (ADR-0002), creating a cohesive technology stack.

Further reading:
- [Celery Documentation](https://docs.celeryq.dev/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Celery Best Practices](https://medium.com/@taylorhughes/three-quick-tips-from-two-years-with-celery-c05ff9d7f9eb)
- [Task Queues Comparison](https://www.fullstackpython.com/task-queues.html) [[1]](https://www.fullstackpython.com/task-queues.html)
