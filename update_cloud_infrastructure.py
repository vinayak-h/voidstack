from pathlib import Path
import re

article_path = Path("src/content/articles/cloud-infrastructure.md")
content = article_path.read_text(encoding="utf-8-sig")

replacement = r'''## Putting it all together

The user management system can be organized as the following production-oriented architecture:

```mermaid
flowchart LR
    Browser["🌐 User Browser"] -->|HTTPS| LB["⚖️ Application Load Balancer"]

    subgraph Compute["Application tier"]
        API1["🖥️ API Instance 1\nEC2"]
        API2["🖥️ API Instance 2\nEC2"]
    end

    subgraph Data["Data tier"]
        RDS[("🗄️ Database\nRDS PostgreSQL")]
        Cache[("⚡ Cache\nElastiCache")]
    end

    subgraph Services["Managed services"]
        S3["📦 Object Storage\nS3"]
        SNS["📣 Event Bus\nSNS"]
        Lambda["λ Background Jobs\nLambda"]
    end

    CW["📊 Observability\nCloudWatch"]
    IAM["🔐 Access Control\nIAM"]

    LB -->|Routes to healthy instance| API1
    LB -->|Routes to healthy instance| API2
    API1 -->|Reads and writes| RDS
    API2 -->|Reads and writes| RDS
    API1 <-->|Cached profiles and permissions| Cache
    API2 <-->|Cached profiles and permissions| Cache
    API1 -->|Images and reports| S3
    API2 -->|Images and reports| S3
    API1 -->|Publishes domain events| SNS
    API2 -->|Publishes domain events| SNS
    SNS -->|Invokes asynchronously| Lambda
    API1 -.->|Logs, metrics, alarms| CW
    API2 -.->|Logs, metrics, alarms| CW
    RDS -.->|Database monitoring| CW
    IAM -.->|Least-privilege roles| API1
    IAM -.->|Least-privilege roles| API2
    IAM -.->|Service permissions| Lambda
    IAM -.->|Service permissions| S3

    classDef client fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px
    classDef network fill:#fef3c7,stroke:#d97706,color:#0f172a,stroke-width:2px
    classDef compute fill:#dcfce7,stroke:#16a34a,color:#0f172a,stroke-width:2px
    classDef data fill:#f3e8ff,stroke:#9333ea,color:#0f172a,stroke-width:2px
    classDef service fill:#ffe4e6,stroke:#e11d48,color:#0f172a,stroke-width:2px
    classDef operations fill:#cffafe,stroke:#0891b2,color:#0f172a,stroke-width:2px
    class Browser client
    class LB network
    class API1,API2 compute
    class RDS,Cache data
    class S3,SNS,Lambda service
    class CW,IAM operations
```

### Architecture flow

1. A user sends an HTTPS request from the browser to the Application Load Balancer. The load balancer terminates TLS, performs health checks, and routes traffic only to healthy EC2 API instances.
2. The API instances run in private subnets and remain stateless, allowing the service to scale horizontally. Each instance validates input, authenticates the request, and applies the user-management business rules.
3. RDS PostgreSQL is the system of record for users, roles, and audit records. Transactions keep related changes consistent, while backups and Multi-AZ options can improve durability and availability.
4. ElastiCache stores short-lived profiles, permissions, and other frequently requested data. The API treats the cache as disposable and falls back to RDS when an entry is missing or expires.
5. S3 stores profile images and exported reports as durable objects. The database stores object metadata and keys rather than large binary files.
6. SNS receives events such as user registration or password changes. Lambda consumes those events asynchronously for tasks such as image processing, notifications, or audit enrichment, keeping the request path fast.
7. CloudWatch receives application logs, infrastructure metrics, and alarms from the API and data services. IAM roles grant each component only the permissions it needs, without embedding long-lived credentials in the application.

### Design principles applied

- **Separation of concerns:** Compute, durable data, object storage, messaging, and observability each have a focused responsibility.
- **Horizontal scalability:** Multiple stateless API instances behind a load balancer can scale independently as demand changes.
- **Durability by default:** RDS is the source of truth and S3 holds files; cached data can be rebuilt without data loss.
- **Asynchronous processing:** SNS and Lambda move slow or retryable work off the user-facing request path.
- **Least privilege and defense in depth:** Private subnets, security groups, encryption, and narrowly scoped IAM roles limit access.
- **Operational visibility:** Centralized logs, metrics, health checks, and alarms make failures easier to detect and diagnose.

This design is only one possible architecture. The correct services depend on traffic, availability requirements, team experience, cost, and compliance needs.'''

pattern = r"## Putting it all together.*?This design is only one possible architecture\."
content, replacements = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
if replacements != 1:
    raise RuntimeError(f"Expected exactly one target section, found {replacements}")

article_path.write_text(content, encoding="utf-8")
print(f"Updated {article_path} ({len(content)} characters)")
