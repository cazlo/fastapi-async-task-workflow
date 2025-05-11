---
title: 0001 Use FastAPI Web Framework
adr: true
status: accepted
date: "2025-05-11"
decision-makers: []
consulted: []
informed: []

tags:
 - backend
 - api
 - framework
 - performance
---

# Use FastAPI as the Web Framework for Our Backend Services

## Context and Problem Statement

We need to select a web framework for our backend API services that will allow us to efficiently build maintainable, well-documented APIs with good performance characteristics. The framework should support modern Python features and asynchronous processing to handle high-throughput scenarios while maintaining developer productivity.

## Decision Drivers

* Need for high-performance API endpoints that can handle concurrent requests efficiently
* Requirements for automatic API documentation that stays in sync with the code
* Developer experience and productivity, including type safety and IDE support
* Integration capabilities with our existing and planned data processing pipelines (Celery)
* Ease of deploying and containerizing the application
* Support for modern Python features and async/await patterns

## Considered Options

* FastAPI
* Django REST Framework
* Flask + extensions (e.g., Flask-RESTful)
* Starlette (lower-level framework)
* Tornado

## Decision Outcome

Chosen option: "FastAPI", because it provides the best combination of performance, developer experience, and built-in features that align with our needs. FastAPI's automatic OpenAPI/Swagger documentation generation, data validation, and native support for asynchronous programming make it the most suitable choice for our microservices architecture.

### Consequences

* Good, because FastAPI's performance is superior to most Python web frameworks due to its Starlette and Pydantic foundations
* Good, because automatic API documentation reduces the effort to maintain up-to-date documentation
* Good, because strong typing with Pydantic models provides better IDE support and catches errors early
* Good, because the framework natively supports both synchronous and asynchronous request handling
* Good, because dependency injection makes testing and code organization cleaner
* Neutral, because team members will need to learn the framework, but the learning curve is relatively shallow
* Bad, because FastAPI is newer than some alternatives and has a smaller ecosystem of extensions

### Confirmation

Compliance with this ADR will be confirmed through:
1. Code reviews that verify proper use of FastAPI patterns and features
2. Performance testing that validates the expected performance improvements
3. Documentation audits that verify API documentation is being auto-generated correctly
4. Developer surveys to measure productivity impact

## Pros and Cons of the Options

### FastAPI

A modern, high-performance web framework for building APIs with Python 3.6+ based on standard Python type hints.

* Good, because it's built on Starlette for high performance and async support
* Good, because it uses Pydantic for data validation, serialization, and documentation
* Good, because it automatically generates OpenAPI and JSON Schema documentation
* Good, because it has excellent developer experience with type hints and IDE support
* Good, because it supports dependency injection for clean, testable code
* Good, because it has built-in security features and OAuth2 with JWT tokens
* Neutral, because it's newer than some alternatives (released in 2018)
* Bad, because it has fewer third-party extensions compared to more established frameworks

### Django REST Framework

A powerful and flexible toolkit for building Web APIs based on Django.

* Good, because it has a mature ecosystem and extensive third-party packages
* Good, because it provides a comprehensive admin interface
* Good, because it has built-in ORM with migration support
* Neutral, because it has moderate performance for API-only applications
* Bad, because it has higher overhead for simple API services
* Bad, because async support is more limited and newer than FastAPI's
* Bad, because full Django can be overkill for microservices

### Flask + Extensions

A lightweight WSGI web application framework with a large ecosystem of extensions.

* Good, because it's simple and minimal for small applications
* Good, because it has a large ecosystem of extensions
* Good, because it's well-established with extensive documentation
* Neutral, because its performance is adequate for many use cases
* Bad, because async support requires additional libraries and is less integrated
* Bad, because API documentation requires separate extensions
* Bad, because data validation and serialization require additional libraries

### Starlette

A lightweight ASGI framework/toolkit for building high-performance services.

* Good, because it has excellent performance characteristics
* Good, because it has built-in WebSocket support
* Neutral, because it's a lower-level framework requiring more boilerplate
* Bad, because it lacks built-in data validation and documentation features
* Bad, because it would require additional libraries to match FastAPI features

### Tornado

A Python web framework and asynchronous networking library.

* Good, because it has built-in asynchronous networking support
* Good, because it's well-established and mature
* Neutral, because its performance is good but not as high as newer ASGI frameworks
* Bad, because it has a different async approach than Python's standard async/await
* Bad, because it lacks automatic API documentation generation
* Bad, because it has a steeper learning curve

## More Information

FastAPI will be used in conjunction with Celery for background task processing, with RabbitMQ as the message broker. The application will be containerized using Docker and deployed in our Kubernetes cluster.

Further reading:
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Starlette Documentation](https://www.starlette.io/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
