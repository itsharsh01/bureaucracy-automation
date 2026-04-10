# 🏗️ High-Level Design — Complaint AI Chatbot System

> **Version:** 1.0 | **Status:** Draft | **Domain:** FinTech / RegTech

---

## 🎯 Objective

Design a scalable, intelligent complaint resolution system where customers interact with an AI chatbot, grievances are auto-classified via ML, routed to the appropriate company bot, and all interactions are monitored in real-time by the CFPB regulatory dashboard.

---

## 🧠 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CUSTOMER LAYER                           │
│                  ┌──────────────────────┐                       │
│                  │   Customer (UI/App)   │                       │
│                  │  Login  |  Chat UI   │                       │
│                  └──────────┬───────────┘                       │
└─────────────────────────────┼───────────────────────────────────┘
                              │ HTTPS / WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        GATEWAY LAYER                            │
│                  ┌──────────────────────┐                       │
│                  │     API Gateway       │                       │
│                  │ Rate Limiting │ Auth  │                       │
│                  │ Load Balancer│ Logs  │                       │
│                  └──────────┬───────────┘                       │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
│           ┌──────────────────────────────────────┐             │
│           │      Chatbot Orchestrator (CORE)      │             │
│           │  • Manages conversation state/flow    │             │
│           │  • Coordinates ML + Routing calls     │             │
│           │  • Aggregates responses               │             │
│           └──────────┬───────────────┬────────────┘             │
│                      │               │                          │
│            ┌─────────▼──────┐  ┌────▼──────────┐              │
│            │   ML Service   │  │ Auth Service   │              │
│            │ TF-IDF/Embed.  │  │ JWT / OAuth    │              │
│            │ LR / XGBoost   │  └───────────────┘              │
│            │ → Product      │                                   │
│            │ → Issue Type   │                                   │
│            └────────┬───────┘                                   │
└─────────────────────┼───────────────────────────────────────────┘
                      │ ML Predictions
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ROUTING LAYER                             │
│                ┌─────────────────────────┐                     │
│                │      Routing Engine      │                     │
│                │  prediction → company    │                     │
│                │  credit_card + fraud     │                     │
│                │        → HDFC Bot        │                     │
│                │  loan + billing          │                     │
│                │       → SBI Bot          │                     │
│                └────────────┬────────────┘                     │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   COMPANY INTEGRATION LAYER                     │
│           ┌──────────────────────────────────────┐             │
│           │      Company Chatbot Gateway          │             │
│           │  Webhook / REST API Integration       │             │
│           │  Adapter per company bot protocol     │             │
│           └──────────────────┬───────────────────┘             │
│                              │                                  │
│      ┌───────────────────────┼───────────────────────┐        │
│      ▼                       ▼                         ▼        │
│  [HDFC Bot]             [SBI Bot]               [ICICI Bot]    │
└─────────────────────────────────────────────────────────────────┘
                              │
                (All events stream in parallel)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING LAYER                             │
│                ┌─────────────────────────┐                     │
│                │     CFPB Dashboard       │                     │
│                │  • Live chat monitoring  │                     │
│                │  • Complaint tracking    │                     │
│                │  • ML output insights   │                     │
│                │  • Routing audit logs   │                     │
│                └─────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

---


## 🔄 End-to-End Data Flow

```
Step 1   ──▶  Customer logs in via Customer App
Step 2   ──▶  Customer sends complaint message
Step 3   ──▶  API Gateway authenticates and forwards request
Step 4   ──▶  Chatbot Orchestrator receives message
Step 5   ──▶  ML Service predicts: Product + Issue Type
Step 6   ──▶  Routing Engine maps prediction → Company
Step 7   ──▶  Message forwarded to Company Chatbot via Gateway
Step 8   ──▶  Company Bot processes and responds
Step 9   ──▶  Orchestrator relays response back to Customer
Step 10  ──▶  Multi-turn conversation continues (loop Steps 2–9)
Step 11  ──▶  All events streamed in parallel to CFPB Dashboard
```

---

## 🗂️ Technology Stack (Suggested)

| Layer | Technology |
|---|---|
| Frontend | React.js / Flutter (mobile) |
| API Gateway | AWS API Gateway / Kong |
| Orchestrator | Python (FastAPI) / Node.js |
| ML Service | Python (scikit-learn, HuggingFace) |
| Routing Engine | Python rules engine / Redis cache |
| Company Gateway | REST / Webhook adapters |
| Dashboard | React + WebSocket / Grafana |
| Database | PostgreSQL (structured) + MongoDB (chat logs) |
| Message Queue | Kafka / RabbitMQ (for async routing events) |

---

## ⚠️ Key Non-Functional Requirements

| NFR | Target |
|---|---|
| Latency (end-to-end) | < 2 seconds for ML classification + routing |
| Availability | 99.9% uptime (HA across services) |
| Scalability | Horizontal scaling on Orchestrator + ML pods |
| Security | TLS everywhere, JWT auth, PII masking in logs |
| Compliance | CFPB data retention policies enforced |

---

## 🚧 Risks & Mitigations

| Risk | Mitigation |
|---|---|
| ML misclassification | Confidence threshold + human fallback queue |
| Company bot unavailable | Retry + timeout + escalation flow |
| High traffic spike | Auto-scaling + API rate limiting |
| PII leakage in logs | Log anonymization pipeline before Dashboard |

---

*Document prepared for internal architecture review. Subject to revision.*