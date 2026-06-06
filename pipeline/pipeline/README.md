# Tavus AI Agent: Secure Cloud Interview Recorder

A production-ready, low-latency microservice architecture designed to handle webhooks from the Tavus Conversational Video API, stream recordings in real-time, and store them securely within an encrypted cloud architecture.

## Key Features
- **Zero-Disk Streaming:** Videos are piped straight from Tavus to AWS S3 via memory buffers. This completely eliminates local server disk depletion or storage crashes.
- **Enterprise Security:** Enforces server-side KMS encryption (`aws:kms`) on S3 buckets and locks access behind strict IAM roles.
- **Asynchronous Processing:** Utilizes FastAPI BackgroundTasks to respond to webhooks instantly within 100ms, preventing webhook timeouts.

## System Architecture Overview
