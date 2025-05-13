---
title: 0005 Use PostgreSQL for Data Storage
adr: true
status: accepted
date: "2025-05-11"
decision-makers: []
consulted: []
informed: []
tags:
 - backend
 - database
 - performance
 - storage
 - celery
---

# Use PostgreSQL for Application Data and Celery Result Storage

## Context and Problem Statement

Our application requires a robust, performant database solution for storing both structured application data and Celery task results. We need a database system that can efficiently handle relational data with strict schemas while also providing flexibility for semi-structured data. Additionally, the solution should support the storage and querying of Celery task results and scheduled tasks while maintaining good performance characteristics under varying loads.

## Decision Drivers

* Need for schema flexibility alongside strict relational integrity where appropriate
* Performance requirements for both structured and semi-structured data queries
* Support for Celery result backend and beat scheduling storage
* Scalability for growing data volumes and increasing query complexity
* Reliability and data integrity guarantees
* Developer familiarity and ecosystem maturity
* Integration capabilities with our existing technology stack (FastAPI, SQLModel, Celery)
* Long-term maintainability and operational considerations

## Considered Options

* PostgreSQL
* MySQL/MariaDB
* MongoDB
* Hybrid approach (relational DB + document DB)
* SQLite (for development)

## Decision Outcome

Chosen option: "PostgreSQL", because it provides the best combination of strict relational data modeling with schema flexibility through its JSONB data type. PostgreSQL offers robust transaction support, excellent performance for mixed workloads, and native capabilities that support both our application data needs and Celery's result storage requirements.

### Consequences

* Good, because PostgreSQL provides strong ACID compliance for critical data
* Good, because JSONB columns offer schema flexibility for evolving data structures
* Good, because PostgreSQL has excellent indexing capabilities for both relational and JSON data
* Good, because it eliminates the need for multiple database systems, simplifying our architecture
* Good, because it integrates well with SQLModel and Celery's database result backend
* Good, because it has mature tooling, monitoring, and backup solutions
* Neutral, because it requires appropriate configuration and tuning for optimal performance
* Bad, because it may have higher initial setup complexity compared to some alternatives
* Bad, because it may require more careful query optimization for very large JSON documents

### Confirmation

Compliance with this ADR will be confirmed through:
1. Performance testing of database operations with realistic data volumes
2. Verification of Celery result backend functionality with PostgreSQL
3. Successful implementation of both strict schema tables and flexible JSONB columns
4. Monitoring of query performance in development and production environments

## Pros and Cons of the Options

### PostgreSQL

A powerful, open-source object-relational database system with over 30 years of active development.

* Good, because it provides robust support for both relational data and JSONB document storage [[1]](https://community.sisense.com/t5/knowledge-base/postgres-vs-mongodb-for-storing-json-data-which-should-you/ta-p/111)
* Good, because it offers sophisticated query capabilities for both structured and semi-structured data
* Good, because it can outperform specialized document databases for many JSON workloads [[2]](https://www.reddit.com/r/PostgreSQL/comments/mh4hfl/any_good_stats_on_jsonb_vs_normal_column/)
* Good, because it has strong transaction support and ACID compliance
* Good, because it provides advanced features like table partitioning, replication, and full-text search
* Good, because it has excellent community support and extensive documentation
* Good, because it integrates well with SQLModel through SQLAlchemy
* Neutral, because it may require more careful configuration than simpler databases
* Bad, because JSONB storage can be less space-efficient than specialized document stores for some workloads [[3]](https://medium.com/@yurexus/can-postgresql-with-its-jsonb-column-type-replace-mongodb-30dc7feffaf3)

### MySQL/MariaDB

Popular open-source relational database management systems.

* Good, because they are widely used with extensive community support
* Good, because they generally perform well for read-heavy workloads
* Good, because they have a simpler setup process compared to PostgreSQL
* Neutral, because they offer JSON support but with less advanced capabilities than PostgreSQL's JSONB
* Bad, because their JSON implementation lacks some of the querying capabilities of PostgreSQL
* Bad, because they have more limited support for complex data types
* Bad, because they don't integrate as seamlessly with Celery for result storage

### MongoDB

A document-oriented NoSQL database designed for storing JSON-like documents.

* Good, because it natively handles document data without schema constraints
* Good, because it has a flexible document model for evolving data structures
* Good, because it offers horizontal scaling through sharding
* Neutral, because it provides its own query language that differs from SQL
* Bad, because it lacks the robust transaction support of PostgreSQL
* Bad, because it would require maintaining a separate system for relational data
* Bad, because it doesn't integrate as well with our SQLModel ORM
* Bad, because it's not an ideal solution for Celery result backend storage

### Hybrid approach (relational DB + document DB)

Using both a relational database and a document database in combination.

* Good, because each database type can be used for its strengths
* Good, because it allows specialized optimization for different data types
* Neutral, because it provides maximum flexibility in data storage options
* Bad, because it significantly increases operational complexity
* Bad, because it requires managing multiple database systems
* Bad, because it introduces potential data synchronization challenges
* Bad, because it increases infrastructure costs

### SQLite (for development)

A lightweight, file-based relational database.

* Good, because it's simple to set up with zero configuration
* Good, because it has no separate server process, reducing complexity
* Good, because it works well for development and testing environments
* Neutral, because it supports basic JSON functionality
* Bad, because it doesn't scale for production workloads
* Bad, because it lacks many advanced features needed for our application
* Bad, because it has limited concurrency support
* Bad, because it's not suitable as a Celery result backend in production

## More Information

PostgreSQL will be used to store our application's relational data through SQLModel, as well as Celery task results and beat schedules. We'll use the JSONB column type for flexible schema requirements while maintaining traditional relational structures for data with well-defined schemas. This choice aligns with our previous decisions to use FastAPI (ADR-0001), SQLModel (ADR-0002), and Celery (ADR-0003).

Further reading:
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL JSONB Documentation](https://www.postgresql.org/docs/current/datatype-json.html)
- [Celery with PostgreSQL Backend](https://docs.celeryq.dev/en/stable/userguide/configuration.html#database-backend-settings)
- [Comparing PostgreSQL JSONB Performance](https://www.architecture-weekly.com/p/postgresql-jsonb-powerful-storage) [[5]](https://www.architecture-weekly.com/p/postgresql-jsonb-powerful-storage)
