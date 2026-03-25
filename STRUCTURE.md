# Project Directory Structure

```
AWRest/
│
├── README.md                          # Main project documentation
├── BUILD_SUMMARY.md                   # Build completion summary
├── DEPLOYMENT.md                      # Detailed deployment guide
├── ARCHITECTURE.md                    # Technical architecture
├── API_REFERENCE.md                   # API documentation
│
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── docker-compose.yml                 # Local development orchestration
│
├── start.sh                          # Automated startup script
├── deploy-k8s.sh                     # Kubernetes deployment script
│
├── backend/                          # Backend services
│   ├── __init__.py
│   ├── app/                         # Flask API Gateway
│   │   ├── __init__.py
│   │   └── api_gateway.py           # Main Flask application (350 lines)
│   │
│   ├── services/                    # Async services
│   │   ├── __init__.py
│   │   └── tornado_orders.py        # Tornado order service (200 lines)
│   │
│   ├── models/                      # Database models
│   │   ├── __init__.py
│   │   └── database.py              # DB connections & models (300 lines)
│   │
│   ├── chatbot/                     # AI Chatbot
│   │   ├── __init__.py
│   │   └── gradio_bot.py            # GPT-4 chatbot (200 lines)
│   │
│   └── configs/                     # Configuration
│       ├── __init__.py
│       └── config.py                # Config management (70 lines)
│
├── frontend/                        # Web application
│   ├── index.html                   # Main HTML (300 lines)
│   ├── styles.css                   # Styling (450 lines)
│   └── app.js                       # Frontend logic (400 lines)
│
├── docker/                          # Container definitions
│   ├── Dockerfile.flask             # Flask container (20 lines)
│   ├── Dockerfile.tornado           # Tornado container (20 lines)
│   └── Dockerfile.chatbot           # Chatbot container (20 lines)
│
├── kubernetes/                      # K8s orchestration
│   ├── namespace-config.yaml        # Namespace & secrets (50 lines)
│   ├── mongodb.yaml                 # MongoDB deployment (80 lines)
│   ├── postgres.yaml                # PostgreSQL deployment (80 lines)
│   ├── flask-api.yaml               # Flask API with HPA (120 lines)
│   ├── tornado-service.yaml         # Tornado with HPA (100 lines)
│   └── chatbot-service.yaml         # Chatbot with HPA (100 lines)
│
└── .git/                            # Git repository

Total: 30+ files, 3500+ lines of code + documentation
```

## File Descriptions

### Documentation (5 files)
- **README.md**: Complete project guide, features, architecture overview
- **DEPLOYMENT.md**: Step-by-step deployment procedures, scaling configs
- **ARCHITECTURE.md**: Technical deep-dive, data flows, performance
- **API_REFERENCE.md**: Endpoint documentation with examples
- **BUILD_SUMMARY.md**: This build completion summary

### Backend Services (6 Python files)
- **api_gateway.py**: Flask REST API, product management, order routing
- **tornado_orders.py**: Async service, order processing, DynamoDB
- **database.py**: DB connections, models, indexing
- **gradio_bot.py**: GPT-4 chatbot, RAG pipeline, PostgreSQL logging
- **config.py**: Configuration management, environment handling

### Frontend (3 web files)
- **index.html**: Product listing, cart, checkout, chatbot integration
- **styles.css**: Responsive design, animations, gradients
- **app.js**: Shopping cart, API calls, search, notifications

### Docker (3 files)
- **Dockerfile.flask**: Flask API container
- **Dockerfile.tornado**: Tornado service container
- **Dockerfile.chatbot**: Gradio chatbot container

### Kubernetes (6 YAML files)
- **namespace-config.yaml**: Namespace, ConfigMap, Secrets, PVCs
- **mongodb.yaml**: MongoDB Deployment + Service
- **postgres.yaml**: PostgreSQL Deployment + Service
- **flask-api.yaml**: Flask API + Service + HPA (70% CPU)
- **tornado-service.yaml**: Tornado + Service + HPA (70% CPU)
- **chatbot-service.yaml**: Chatbot + Service + HPA (70% CPU)

### Configuration (4 files)
- **.env.example**: Environment variable template
- **requirements.txt**: Python dependencies (15 packages)
- **docker-compose.yml**: 6-service local stack
- **start.sh**: Automated startup script

### Scripts (2 files)
- **deploy-k8s.sh**: Kubernetes deployment automation
- **.git/**: Git version control

## Component Communication

```
Frontend Layer
  ↓ (HTTP)
Flask API Gateway (5000)
  ↓ ↓ ↓ ↓
  ├─→ ProductModel ←→ MongoDB (27017)
  ├─→ OrderHandler ←→ Tornado (8001) ←→ DynamoDB
  ├─→ HealthCheck
  └─→ StatusCheck

Tornado Service (8001)
  ├─→ OrderHandler ←→ DynamoDB
  ├─→ ProcessingHandler ←→ AsyncProcessor
  └─→ Health endpoint

Gradio Chatbot (7860)
  ├─→ RAGPipeline ←→ MongoDB (27017)
  ├─→ LabuboChatbot ←→ OpenAI GPT-4
  └─→ QueryLogger ←→ PostgreSQL (5432)

Kubernetes Layer
  ├─→ 6 Deployments (Flask×2-10, Tornado×2-10, Chatbot×2-8)
  ├─→ 3 Services (LoadBalancer: Flask, Chatbot; ClusterIP: Tornado)
  ├─→ 3 HPAs (70% CPU threshold)
  └─→ 2 StatefulSets (MongoDB, PostgreSQL)
```

## Database Schema

### MongoDB (listings collection)
```
{
  _id: ObjectId,
  product_id: String (unique),
  name: String,
  character_name: String,
  price: Number,
  condition: String,
  description: String,
  seller_id: String,
  status: String,
  created_at: Date
}
```

### DynamoDB (labubu_orders table)
```
Partition Key: order_id (String)
Sort Key: timestamp (Number)
Attributes:
  - user_id, product_id, quantity
  - total_price, status
  - shipping_address, created_at
```

### PostgreSQL
```
chatbot_queries:
  - id, user_id, query, response
  - context_products (JSONB)
  - created_at

product_views:
  - id, user_id, product_id, viewed_at
```

## Deployment Variants

### Local Development
- Docker Compose
- 1 instance each service
- LocalStack for DynamoDB
- Health checks enabled

### Staging
- Kubernetes (3-node cluster)
- 2 replicas per service
- Real AWS DynamoDB
- Monitoring enabled

### Production
- Kubernetes (10+ node cluster)
- Autoscaling 2-10 replicas
- Real DynamoDB, RDS options
- Full observability stack

---

This structure ensures:
✅ Modularity and maintainability
✅ Clear separation of concerns
✅ Easy testing and deployment
✅ Scalability across environments
✅ Production-ready organization
