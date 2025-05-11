---
title: 0006 Use RabbitMQ for Celery Message Broker
adr: true
status: accepted
date: "2025-05-11"
decision-makers: []
consulted: []
informed: []
tags:
 - backend
 - messaging
 - monitoring
 - scalability
 - aws
---

# Use RabbitMQ Instead of Redis/Valkey for Celery Message Broker

## Context and Problem Statement

Our application uses Celery for asynchronous task processing, which requires a message broker to facilitate communication between task producers and consumers. While both Redis/Valkey and RabbitMQ are supported as Celery message brokers, we need a solution that provides detailed per-queue metrics to enable effective auto-scaling of worker nodes based on queue length. Additionally, we need reliable message delivery with strong guarantees for task persistence in case of system failures.

## Decision Drivers

* Need for detailed per-queue metrics to enable auto-scaling of worker nodes
* Requirements for CloudWatch integration in AWS environment
* Message persistence and delivery guarantees
* Queue monitoring and management capabilities
* Scalability as message volume increases
* Operational complexity and management overhead
* Cost considerations for AWS-managed services
* Integration with our existing technology stack

## Considered Options

* RabbitMQ (via AWS MQ)
* Redis/Valkey (via AWS ElastiCache)
* Amazon SQS
* Apache Kafka (via Amazon MSK)
* Combination of brokers for different task types

## Decision Outcome

Chosen option: "RabbitMQ (via AWS MQ)", because it provides superior queue monitoring capabilities with detailed per-queue CloudWatch metrics that facilitate auto-scaling worker nodes based on queue length. RabbitMQ also offers stronger message delivery guarantees and persistence than Redis/Valkey, which is critical for ensuring task processing reliability.

### Consequences

* Good, because RabbitMQ exposes detailed CloudWatch metrics per queue in AWS MQ
* Good, because it enables auto-scaling worker nodes based on specific queue lengths
* Good, because it provides stronger message delivery guarantees with persistent messaging
* Good, because it has a robust management interface for monitoring queue health
* Good, because it offers advanced routing capabilities with exchanges and bindings
* Neutral, because it requires more configuration than Redis/Valkey
* Bad, because AWS MQ for RabbitMQ has higher costs compared to serverless Redis/Valkey options
* Bad, because it adds operational complexity to our infrastructure

### Confirmation

Compliance with this ADR will be confirmed through:
1. Implementation of CloudWatch alarms and auto-scaling policies based on queue metrics
2. Verification of message persistence during broker restarts
3. Load testing to validate broker performance under high message volume
4. Cost monitoring to ensure the solution remains economically viable

## Pros and Cons of the Options

### RabbitMQ (via AWS MQ)

A robust message broker with advanced routing capabilities, strong delivery guarantees, and comprehensive monitoring.

* Good, because it emits detailed CloudWatch metrics per queue for precise auto-scaling [[1]](https://www.reddit.com/r/django/comments/loqmad/do_you_recommend_using_rabbitmq_or_redis_as_a/)
* Good, because it has strong message persistence and delivery guarantees
* Good, because it provides sophisticated routing with exchanges and binding keys
* Good, because it offers a comprehensive management interface for monitoring
* Good, because it supports various messaging patterns (direct, fanout, topic)
* Good, because it has mature client libraries and extensive documentation
* Good, because AWS MQ provides managed service with high availability options [[7]](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/best-practices-rabbitmq.html)
* Neutral, because it has a steeper learning curve than Redis/Valkey
* Bad, because it has higher costs in AWS compared to serverless options
* Bad, because it has more complex configuration requirements

### Redis/Valkey (via AWS ElastiCache)

An in-memory data structure store that can be used as a message broker, offering high performance with simpler configuration.

* Good, because it provides faster message processing for high-throughput scenarios [[3]](https://aws.amazon.com/compare/the-difference-between-rabbitmq-and-redis/)
* Good, because it has simpler configuration and deployment
* Good, because it offers lower cost with serverless options in AWS
* Good, because it can serve multiple purposes (cache, broker, data store)
* Neutral, because it has adequate performance for many task processing needs
* Bad, because it lacks detailed per-queue CloudWatch metrics in AWS ElastiCache
* Bad, because it offers weaker message persistence and delivery guarantees
* Bad, because it has limited routing capabilities compared to RabbitMQ
* Bad, because it makes auto-scaling based on specific queue lengths difficult

### Amazon SQS

A fully managed message queuing service that integrates natively with AWS services.

* Good, because it is a fully managed serverless service with minimal operational overhead
* Good, because it integrates natively with AWS CloudWatch and auto-scaling
* Good, because it provides strong durability and reliability guarantees
* Good, because it has predictable pricing based on message volume
* Neutral, because it offers simplified queue management
* Bad, because it requires a custom Celery transport layer or adapter
* Bad, because it lacks the advanced routing features of RabbitMQ
* Bad, because it has potential compatibility issues with some Celery features

### Apache Kafka (via Amazon MSK)

A distributed event streaming platform designed for high-throughput messaging.

* Good, because it excels at handling very high message volumes
* Good, because it provides strong durability with replication
* Good, because it allows message replay and stream processing
* Neutral, because it offers scalability for large-scale distributed systems
* Bad, because it requires a custom Celery transport implementation
* Bad, because it has higher complexity and operational overhead
* Bad, because it comes with significantly higher costs in AWS
* Bad, because it may be overkill for typical Celery workloads

### Combination of brokers for different task types

Using different brokers optimized for specific task types and requirements.

* Good, because it allows optimization for different message patterns
* Good, because it enables cost optimization for different workloads
* Neutral, because it provides flexibility to choose the best tool for each job
* Bad, because it significantly increases system complexity
* Bad, because it creates operational overhead of managing multiple brokers
* Bad, because it introduces potential synchronization and consistency challenges
* Bad, because it complicates monitoring and troubleshooting

## More Information

RabbitMQ will be deployed using AWS MQ in a multi-AZ configuration for high availability. We'll configure CloudWatch alarms on queue length metrics to trigger auto-scaling of Celery worker nodes, ensuring efficient task processing as demand fluctuates. This decision aligns with our previous choices to use Celery for task processing (ADR-0003) and PostgreSQL for the result backend (ADR-0005).

Further reading:
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [AWS MQ for RabbitMQ Documentation](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html)
- [Celery with RabbitMQ Guide](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html)
- [RabbitMQ Monitoring Best Practices](https://www.elastic.co/observability-labs/blog/amazonmq-observability-rabbitmq-integration) [[6]](https://www.elastic.co/observability-labs/blog/amazonmq-observability-rabbitmq-integration)
- [AWS MQ for RabbitMQ Best Practices](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/best-practices-rabbitmq.html) [[7]](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/best-practices-rabbitmq.html)
