from pathlib import Path

output_path = Path(r"C:\personal\voidstack-complete\voidstack\src\content\articles\cloud-infrastructure.md")

content = """---
title: 'Understanding Cloud Infrastructure'
description: 'A beginner-friendly guide to compute, networking, storage, and managed services with practical examples.'
category: 'CLOUD'
publishedDate: '2026-09-21'
---

# Understanding Cloud Infrastructure

When I first started exploring AWS, I found the number of services confusing.

EC2, S3, VPC, Lambda, RDS, IAM, CloudWatch... there are so many names that it is difficult to understand where to begin.

The problem is not always learning each service individually. The bigger problem is understanding **how these services work together**.

In this article, we will look at the main building blocks of cloud infrastructure:

- Compute
- Networking
- Storage
- Databases
- Managed services
- Security and monitoring

We will use a simple **user management system** as an example throughout the article. Users will be able to register, sign in, update their profiles, and view their account information.

## 1. What is cloud infrastructure?

Cloud infrastructure is the collection of resources required to run applications and services.

These resources include:

- Servers
- Networks
- Storage
- Databases
- Security controls
- Monitoring systems

In the past, companies usually purchased physical servers and maintained them in their own data centers.

If a company needed more servers, it had to purchase additional hardware, configure it, and maintain it.

Cloud platforms changed this approach.

With platforms such as AWS, you can request computing resources through a web console, command line, or API.

You do not necessarily need to purchase physical hardware yourself.

For example, imagine you want to run a Java Spring Boot application for a user management system.

You need somewhere to execute the application, a way for users to access it, and somewhere to store its data.

Cloud infrastructure provides the building blocks for this.

---

## 2. Compute: Where your application runs

Compute is the processing power used to run your application.

In simple words:

**Compute is where your code executes.**

For example, when you start a Spring Boot application on your laptop, your laptop's CPU and memory are being used to run it.

In the cloud, you can use services such as:

- Amazon EC2
- AWS Lambda
- Amazon ECS

Each service provides a different way to run code.

### Amazon EC2

Amazon EC2 provides virtual servers.

You can choose the operating system, instance type, storage, and other settings.

For example, you could create an EC2 instance running Linux and deploy your Spring Boot user management application on it.

A simplified flow looks like this:

```text
User -> EC2 Instance -> Spring Boot Application
```

The application could expose endpoints such as:

```text
POST /users
POST /login
GET  /users/{id}
PUT  /users/{id}
```

An EC2 instance gives you a lot of control, but you are also responsible for tasks such as operating system updates, application deployment, and capacity planning.

### Scaling compute

If many people use the user management system at the same time, one server may not be enough. You can add more instances and place them behind a load balancer.

You can also use an Auto Scaling Group to create or remove instances based on demand. This allows the system to use more capacity during busy periods and less capacity when traffic is low.

The important idea is that compute provides the place where the application runs. The rest of the infrastructure helps users reach it and helps the application safely store and process data.

---

## 3. Networking: How services communicate

Networking connects users, application servers, databases, and other cloud services.

A network for the user management system should allow public requests to reach the application while keeping databases and internal services private.

### Amazon VPC

An Amazon Virtual Private Cloud, or VPC, is an isolated network that you control inside AWS.

A VPC has an IP address range and can contain subnets, route tables, internet gateways, and security controls.

A typical layout looks like this:

```text
Internet
   |
Internet Gateway
   |
Public Subnet: Load Balancer
   |
Private Subnet: User Management API
   |
Private Subnet: RDS Database
```

The load balancer can receive traffic from the internet, while the API and database remain in private subnets.

### Subnets

A subnet is a smaller section of a VPC. Subnets are commonly divided into public and private subnets.

- **Public subnets** have a route to the internet and can contain a load balancer.
- **Private subnets** do not accept direct inbound internet traffic and can contain application servers and databases.

For high availability, create subnets in more than one Availability Zone. If one data center has a problem, another can continue serving requests.

### Load balancer

A load balancer distributes incoming requests across multiple application instances.

For the user management system, a user might request `GET /users/42`. The load balancer receives that request and forwards it to a healthy Spring Boot instance.

This provides two useful benefits:

1. Traffic is shared between instances.
2. Unhealthy instances can be removed from service automatically.

### Security groups

Security groups act as virtual firewalls for cloud resources. They control which inbound and outbound connections are allowed.

A simple set of rules could be:

- The load balancer accepts HTTPS traffic on port 443 from the internet.
- The API instances accept traffic only from the load balancer security group.
- The RDS database accepts traffic only from the API security group.
- SSH access is restricted to an administrative network, or replaced with a managed session service.

This layered design means a user cannot connect directly to the database, even if the database hostname becomes known.

---

## 4. Storage: Keeping files and data

Storage holds information beyond the lifetime of a running server. This is important because an EC2 instance can be replaced, stopped, or scaled down.

The user management system might need to store profile pictures, exported user reports, and application logs.

### Amazon S3

Amazon S3 is object storage. It stores files as objects inside buckets.

For example, a profile picture could be stored at a key such as:

```text
user-profile-images/user-42/avatar.png
```

The database should store the object's key and metadata, while the image itself remains in S3. The application can then generate a short-lived signed URL when the user needs to view it.

S3 is useful for:

- Profile images
- Reports and exports
- Application artifacts
- Backups
- Static website assets

A bucket should not be made public by default. Use private access, encryption, and a bucket policy that grants only the required permissions.

### Amazon EBS

Amazon Elastic Block Store, or EBS, provides block storage for EC2 instances. It behaves similarly to a disk attached to a server.

An application may use EBS for temporary files, local caches, or application logs. EBS volumes should not be treated as the only copy of important user data because they are attached to a particular instance and require backup planning.

### Data persistence

A useful rule is to separate compute from persistent data:

- Keep application code on the instance or in a deployment artifact.
- Keep user records in a database.
- Keep uploaded files in S3.
- Keep backups in durable, separately protected storage.

This allows a failed application server to be replaced without losing user accounts or profile images.

---

## 5. Databases: Storing structured information

A user management system has structured data: user IDs, email addresses, password hashes, profile details, roles, and timestamps.

A database provides durable storage, indexes, transactions, and a way to query this information safely.

### Amazon RDS

Amazon RDS is a managed relational database service. It supports engines such as PostgreSQL and MySQL.

A relational database is a natural choice for users because the data has clear relationships and needs transactions. A simplified table might look like this:

```text
users
-----
id
email
password_hash
display_name
role
created_at
updated_at
```

When a user registers, the Spring Boot API validates the request, hashes the password, and writes a new row to the `users` table. The plain-text password should never be stored.

RDS can provide automated backups, encryption, patching options, and Multi-AZ deployment. The database should be placed in private subnets and its security group should allow connections only from the application servers.

### DynamoDB

Amazon DynamoDB is a managed NoSQL database. It is useful when an application needs very fast access at scale and its access patterns fit a key-value or document model.

For example, the system could use DynamoDB for login attempt records or a user preference document keyed by `userId`.

DynamoDB is not automatically better than a relational database. Choose it when its flexible schema, scaling model, and access patterns match the problem.

### Structured data and transactions

The user management system may update a user record and an audit record together. A relational transaction can ensure that both changes succeed or both are rolled back.

Whichever database is selected, plan for:

- Indexes for common queries such as email lookup
- Encryption at rest and in transit
- Backups and restore testing
- Connection limits and pooling
- Least-privilege database credentials

---

## 6. Managed services: Building less infrastructure yourself

Managed services provide capabilities without requiring you to operate every server yourself. They can reduce maintenance work and give a small team reliable building blocks.

### ElastiCache

Amazon ElastiCache provides managed in-memory caches such as Redis or Memcached.

The user management API could cache a short-lived user profile or a frequently checked permission. A cache can reduce database load and improve response time.

Cached data should not be the only copy of a user record. If the cache is cleared, the API must be able to read the information from the database again.

### SNS

Amazon Simple Notification Service, or SNS, publishes messages to subscribers.

After a user registers, the API could publish a `UserRegistered` event. An email service or audit component can subscribe to that event without making the registration request wait for every downstream task.

This creates looser coupling between the user management API and supporting features.

### IAM

AWS Identity and Access Management, or IAM, controls access to AWS resources.

For example, the application role might be allowed to:

- Read and write objects only in the profile-image S3 bucket
- Read database credentials from a secrets service
- Publish messages to one SNS topic
- Write logs to CloudWatch

It should not have administrator access. Use roles for applications instead of putting long-lived access keys in source code or configuration files.

### Lambda

AWS Lambda runs code in response to events without requiring you to manage a server.

A Lambda function could resize a profile image after it is uploaded to S3, process a user-registration notification, or remove expired temporary files.

Lambda is a good fit for short, event-driven tasks. A continuously running API may still be better suited to EC2, ECS, or another container platform.

---

## 7. Security and monitoring

Security and monitoring should be included from the beginning rather than added after deployment.

### CloudWatch

Amazon CloudWatch collects metrics, logs, and alarms. The user management system can send application logs from the Spring Boot API to CloudWatch.

Useful metrics and alarms include:

- High CPU or memory usage
- Increased API error rates
- Slow database queries
- Failed login spikes
- Low database storage
- Unhealthy load balancer targets

Logs should contain enough information to troubleshoot a request, but should not contain passwords, session tokens, or unnecessary personal information.

### IAM and security controls

Use IAM roles with the smallest practical set of permissions. Separate permissions for development, testing, and production environments.

Additional controls can include:

- HTTPS for all user-facing traffic
- Encryption at rest for S3, EBS, and RDS
- Secrets stored in a secrets manager rather than source code
- Multi-factor authentication for administrators
- Private subnets for APIs and databases
- Network and application-level validation
- Dependency and operating system updates
- Audit logs for administrative actions

Application security also matters. Passwords should be hashed with a modern password-hashing algorithm, authentication tokens should expire, and authorization checks should verify that a user is allowed to access the requested account.

### Backups and recovery

Backups protect against accidental deletion, software bugs, and infrastructure failures. Enable automated database backups and versioning where appropriate for important S3 objects.

A backup is useful only if it can be restored. Periodically test restoring a database and recovering an application in a separate environment. Define a recovery point objective, which describes how much data loss is acceptable, and a recovery time objective, which describes how quickly the system should return to service.

---

## Putting it all together

The complete user management system can follow this flow:

```text
                           +----------------------+
                           |   User's Browser     |
                           +----------+-----------+
                                      |
                                HTTPS request
                                      |
                           +----------v-----------+
                           |   Application Load    |
                           |      Balancer         |
                           +-----+------------+----+
                                 |            |
                    +------------v--+      +-v-------------+
                    | Private Subnet |      | Private Subnet|
                    | Spring Boot API|      | Spring Boot API|
                    |    EC2 #1      |      |    EC2 #2      |
                    +-------+--------+      +-------+--------+
                            |                       |
                            +-----------+-----------+
                                        |
                         +--------------v--------------+
                         |       RDS PostgreSQL        |
                         | users, roles, audit records |
                         +-----------------------------+

       API -> ElastiCache: short-lived cached profiles and permissions
       API -> S3: profile images and exported reports
       API -> SNS: user registration and notification events
       SNS -> Lambda: asynchronous image or notification processing
       All services -> CloudWatch: logs, metrics, and alarms
       IAM roles -> permissions for each service
```

A request to register a user enters through HTTPS and reaches the load balancer. The load balancer forwards it to a healthy Spring Boot instance in a private subnet.

The API validates the request, hashes the password, and stores the user record in RDS. If the user uploads a profile image, the API stores the object in S3 and records its key in the database. The API can publish a registration event through SNS, allowing Lambda or another subscriber to perform background work.

ElastiCache can speed up repeated reads, while CloudWatch collects the logs and metrics needed to operate the service. IAM roles, security groups, encryption, backups, and private subnets protect the system and its data.

This design is only one possible architecture. The correct services depend on traffic, availability requirements, team experience, cost, and compliance needs.

## Key takeaway

Cloud infrastructure is easier to understand when you view it as a group of responsibilities:

- Compute runs the application.
- Networking connects the application to users and other services.
- Storage keeps files and durable data.
- Databases organize structured information.
- Managed services handle common capabilities.
- Security and monitoring keep the system protected and observable.

Start with the application requirements, then choose the simplest architecture that meets them. For a user management system, that usually means a private application layer, a protected database, durable file storage, controlled permissions, useful monitoring, and tested backups.
"""

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(content, encoding="utf-8")
print(f"Wrote {output_path} ({len(content)} characters)")
