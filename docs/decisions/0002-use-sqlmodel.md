---
title: 0002 Use SQLModel for ORM
adr: true
status: accepted
date: "2025-05-11"
decision-makers: []
consulted: []
informed: []
tags:
 - backend
 - database
 - orm
 - performance
---

# Use SQLModel as the ORM for Our Database Layer

## Context and Problem Statement

We need to select an Object-Relational Mapping (ORM) tool for our backend services that efficiently integrates with our FastAPI application. The ORM should provide a consistent way to interact with the database, maintain type safety, reduce code duplication, and offer good performance characteristics while maintaining developer productivity. We need a solution that bridges API models and database models seamlessly.

## Decision Drivers

* Need for consistency between API data models and database models
* Desire to reduce code duplication between Pydantic models and SQLAlchemy models
* Type safety and IDE support to catch errors early in development
* Performance considerations for database operations
* Seamless integration with our chosen FastAPI framework
* Developer experience and productivity
* Maintainability of the codebase over time

## Considered Options

* SQLModel
* SQLAlchemy ORM (with separate Pydantic models)
* Raw SQL queries with database drivers
* Django ORM
* Tortoise ORM

## Decision Outcome

Chosen option: "SQLModel", because it provides the best integration between FastAPI's Pydantic models and SQLAlchemy's ORM capabilities. SQLModel allows us to define models once and use them for both API validation/serialization and database operations, significantly reducing code duplication while maintaining type safety.

### Consequences

* Good, because SQLModel integrates the power of Pydantic and SQLAlchemy in a single model
* Good, because it eliminates code duplication between API schemas and database models
* Good, because it maintains full type checking and IDE autocompletion benefits
* Good, because it preserves compatibility with SQLAlchemy's ecosystem and tools
* Good, because it simplifies CRUD operations with clean, intuitive syntax
* Neutral, because the framework is relatively new but developed by the same author as FastAPI
* Bad, because it may have slightly lower performance compared to raw SQL for complex queries
* Bad, because it has less documentation and community support compared to pure SQLAlchemy

### Confirmation

Compliance with this ADR will be confirmed through:
1. Code reviews that verify proper use of SQLModel patterns
2. Database operation performance testing against benchmarks
3. Static type checking to ensure type safety across the application
4. Regular evaluations of developer productivity metrics

## Pros and Cons of the Options

### SQLModel

A library for interacting with SQL databases from Python, designed with simplicity, compatibility, and robustness in mind.

* Good, because it unifies Pydantic and SQLAlchemy models, eliminating code duplication
* Good, because it maintains full compatibility with both FastAPI and SQLAlchemy
* Good, because it provides excellent type hints and IDE support
* Good, because it simplifies creating, reading, updating, and deleting records
* Good, because it's developed by the creator of FastAPI, ensuring philosophical alignment
* Neutral, because it's a newer library with a smaller community
* Bad, because it may have performance overhead compared to raw SQL for complex operations
* Bad, because it has less comprehensive documentation than established alternatives

### SQLAlchemy ORM (with separate Pydantic models)

A mature SQL toolkit and Object-Relational Mapping library for Python.

* Good, because it's a mature, battle-tested ORM with a large ecosystem
* Good, because it offers powerful query composition and optimization capabilities
* Good, because it has extensive documentation and community support
* Neutral, because its performance is acceptable for most use cases
* Bad, because it requires maintaining separate models for API and database layers
* Bad, because it leads to code duplication between Pydantic and SQLAlchemy models
* Bad, because synchronizing changes between API and database models is error-prone

### Raw SQL queries with database drivers

Direct SQL queries using database-specific drivers (e.g., psycopg2 for PostgreSQL).

* Good, because it offers the highest performance for complex queries
* Good, because it provides complete control over query optimization
* Good, because it allows database-specific optimizations and features
* Neutral, because it requires more manual validation and serialization
* Bad, because it lacks type safety and ORM benefits
* Bad, because it creates significant code maintenance overhead
* Bad, because it requires more boilerplate code for common operations
* Bad, because it leads to potential SQL injection risks if not carefully managed

### Django ORM

The Object-Relational Mapping tool included with the Django web framework.

* Good, because it's mature and well-documented
* Good, because it includes a powerful migration system
* Good, because it has a large ecosystem of extensions
* Neutral, because its admin interface could be useful for some projects
* Bad, because it would introduce a dependency on the Django ecosystem
* Bad, because it doesn't integrate well with FastAPI
* Bad, because it would create architectural inconsistencies in our stack

### Tortoise ORM

An easy-to-use asyncio ORM inspired by Django.

* Good, because it has native async/await support
* Good, because it's designed for modern Python
* Good, because it has a Django-like familiar syntax
* Neutral, because its performance is comparable to other ORMs
* Bad, because it lacks the deep integration with Pydantic that SQLModel offers
* Bad, because it has a smaller community and ecosystem
* Bad, because it would still require separate models for API validation

## More Information

SQLModel will be used in conjunction with FastAPI for our RESTful API endpoints and with Alembic for database migrations. The choice aligns with our previous decision to use FastAPI (ADR-0001) and builds upon the advantages of that ecosystem.

Further reading:
- [SQLModel Official Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLModel vs. SQLAlchemy ORM Performance Considerations](https://medium.com/@melihcolpan/sqlalchemy-vs-raw-sql-queries-performance-comparison-and-best-practices-caba49125630) [[1]](https://medium.com/@melihcolpan/sqlalchemy-vs-raw-sql-queries-performance-comparison-and-best-practices-caba49125630)
