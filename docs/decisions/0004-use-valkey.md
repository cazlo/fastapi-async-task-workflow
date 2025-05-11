---
title: 0004 Use Valkey Instead of Redis
adr: true
status: accepted
date: "2025-05-11"
decision-makers: []
consulted: []
informed: []
tags:
 - backend
 - database
 - caching
 - licensing
 - open-source
 - cost
---

# Use Valkey Instead of Redis for In-Memory Data Storage

## Context and Problem Statement

Our application requires a high-performance in-memory data store for caching, session management, and supporting our message broker needs. While Redis has been the industry standard for these requirements, recent changes to Redis licensing (moving to the Server Side Public License - SSPL) have created concerns about long-term open-source compatibility and usage restrictions. We need to select an in-memory data store solution that maintains the performance characteristics of Redis while ensuring better alignment with free and open-source software principles.

## Decision Drivers

* Need for superior Free Software Foundation (FSF) compatible licensing
* Requirement for complete API and protocol compatibility with Redis
* Compatibility with existing Redis clients and tools in our ecosystem
* Performance characteristics comparable to Redis
* Cost considerations for commercial Redis vs. open-source alternatives
* Long-term maintainability and community support
* Potential legal implications of using SSPL-licensed software
* Alignment with organizational open-source values and policies

## Considered Options

* Redis (current version with SSPL license)
* Valkey (with GPLv3 license)
* KeyDB
* Dragonfly
* Building a custom in-memory solution

## Decision Outcome

Chosen option: "Valkey version 8", because it provides full Redis API compatibility while using the FSF-approved GPLv3 license instead of Redis's more restrictive SSPL. Valkey 8 is a drop-in replacement for Redis that maintains wire protocol compatibility with existing Redis clients and tools while offering a more permissive licensing model.

### Consequences

* Good, because Valkey uses the GPLv3 license which is FSF-approved and more aligned with open-source principles [[2]](https://devoriales.com/post/387/redis-returns-to-open-source-the-agplv3-licensing-decision)
* Good, because Valkey 8 maintains full command set compatibility with Redis, allowing seamless migration [[3]](https://valkey.io/blog/valkey-8-ga/)
* Good, because existing Redis clients and libraries will work without modification
* Good, because we avoid potential future legal concerns related to Redis's SSPL license
* Good, because Valkey has strong backing from major cloud providers and the open-source community
* Good, because Valkey typically results in significant cost savings compared to commercial Redis offerings and licenses
* Neutral, because some Redis-specific optimizations may not be available in Valkey
* Bad, because Valkey, being a fork, may eventually diverge from Redis in feature parity
* Bad, because the ecosystem around Valkey is still maturing compared to Redis

### Confirmation

Compliance with this ADR will be confirmed through:
1. Successful deployment of Valkey 8 in development and testing environments
2. Compatibility testing with all Redis-dependent services in our stack
3. Performance benchmarking comparing Valkey to Redis
4. Legal review confirming compliance with licensing requirements

## Pros and Cons of the Options

### Valkey (with GPLv3 license)

A community-led fork of Redis that maintains API compatibility while using FSF-approved licensing.

* Good, because it uses the GPLv3 license which is FSF-approved and more permissive than SSPL
* Good, because it maintains full API compatibility with Redis 8 [[3]](https://valkey.io/blog/valkey-8-ga/)
* Good, because it's supported by major cloud providers (AWS, Google Cloud, etc.)
* Good, because it has active development and community support
* Good, because it's a drop-in replacement requiring minimal configuration changes
* Good, because it offers significant cost savings compared to commercial Redis instances and licensing fees
* Neutral, because it's a relatively new fork with less operational history
* Bad, because some Redis Enterprise features are not available
* Bad, because documentation and community resources are still growing

### Redis (current version with SSPL license)

The original in-memory data structure store, now under the Server Side Public License.

* Good, because it has a mature ecosystem with extensive documentation
* Good, because it has proven performance and reliability
* Good, because it has the widest community support and adoption
* Neutral, because it offers enterprise features not available in forks
* Bad, because the SSPL license is not FSF-approved and creates potential legal concerns
* Bad, because the licensing restrictions could impact future cloud deployment options
* Bad, because it represents a deviation from purely open-source principles
* Bad, because it incurs higher costs for commercial licensing and managed services

### KeyDB

A high-performance fork of Redis with a focus on multithreading and higher throughput.

* Good, because it offers enhanced multithreading capabilities over Redis
* Good, because it maintains Redis compatibility
* Good, because it is licensed under the more permissive BSD license
* Neutral, because it offers some performance improvements for specific workloads
* Bad, because it has a smaller community compared to Redis and Valkey
* Bad, because it may diverge more significantly from Redis over time
* Bad, because it has less backing from major cloud providers

### Dragonfly

A modern in-memory database compatible with Redis and Memcached APIs, focusing on high throughput.

* Good, because it's built with modern architecture for improved performance
* Good, because it maintains compatibility with Redis clients
* Good, because it has a permissive BSL license
* Neutral, because it offers some unique features not available in Redis
* Bad, because it has less maturity compared to Redis and Valkey
* Bad, because it has a smaller community and ecosystem
* Bad, because it may have more significant divergence from Redis in the future

### Building a custom in-memory solution

Developing our own in-memory data store tailored to our specific needs.

* Good, because it could be optimized specifically for our use cases
* Good, because we would have complete control over the implementation
* Neutral, because we could choose any license we prefer
* Bad, because it would require significant development resources
* Bad, because it would lack the maturity and testing of established solutions
* Bad, because it would create long-term maintenance burden
* Bad, because it would require custom client implementations

## More Information

Valkey 8.x will be used as a drop-in replacement for Redis in our infrastructure. It will serve primarily as a caching layer and support for our FastAPI application. The choice aligns with our commitment to open-source software and ensures compatibility with our existing technology stack while providing substantial cost savings over commercial Redis offerings, particularly for AWS ElastiCache deployments.

Further reading:
- [Valkey Official Documentation](https://docs.valkey.io/)
- [Valkey 8.0 Release Notes](https://valkey.io/blog/valkey-8-ga/) [[3]](https://valkey.io/blog/valkey-8-ga/)
- [Redis vs. Valkey Comparison](https://redis.io/blog/what-is-valkey/) [[4]](https://redis.io/blog/what-is-valkey/)
- [Understanding Open Source Licensing](https://www.gnu.org/licenses/license-list.html)
