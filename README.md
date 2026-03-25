# 🧸 Labubu Marketplace - E-commerce Platform

A sophisticated web application for selling used and collectible Labubu designer toys, featuring a microservices architecture with Flask API Gateway, Tornado async services, MongoDB, DynamoDB, PostgreSQL, Kubernetes orchestration, and an AI-powered Gradio chatbot.

## 🎯 Project Overview

This platform demonstrates enterprise-grade e-commerce architecture with the following technical components:

### Core Technologies

1. **API Gateway**: Flask-based REST API gateway (Port 5000)
2. **Async Processing**: Tornado async service for order processing (Port 8001)
3. **Databases**:
   - MongoDB: Product listings and inventory management
   - DynamoDB: Order processing and transactional data
   - PostgreSQL: Chatbot query logging for ML model training
4. **AI Chatbot**: Gradio interface with GPT-4 integration and RAG pipeline (Port 7860)
5. **Container Orchestration**: Kubernetes with autoscaling at 70% CPU threshold
6. **Frontend**: Modern interactive web application (Port 8000)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (HTML/CSS/JS)                   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                  Flask API Gateway (5000)                   │
│                    API Routes & Routing                     │
├──────────────────────┬──────────────────┬───────────────────┤
│                      │                  │                   │
│  Tornado Service    │   MongoDB        │   DynamoDB       │
│  (8001)             │   (Listings)     │   (Orders)       │
│  - Order Mgmt       │   (27017)        │   (AWS)          │
│  - Async Tasks      │                  │                  │
│                      │                  │                  │
│  Gradio Chatbot     │   PostgreSQL     │   Kubernetes     │
│  (7860)             │   (Queries)      │   - Autoscaling  │
│  - GPT-4            │   (5432)         │   - Load Balance │
│  - RAG Pipeline     │                  │   - 70% CPU      │
└──────────────────────┴──────────────────┴───────────────────┘
```

## 📋 Features

### E-commerce Functionality
- 🛍️ Product listing and search with MongoDB
- 🛒 Shopping cart and order management
- 📦 Order processing via Tornado async services
- 💳 Payment processing (DynamoDB)
- 📊 Inventory management

### AI & Machine Learning
- 🤖 GPT-4 powered chatbot with Gradio interface
- 📚 RAG (Retrieval-Augmented Generation) pipeline
- 🧠 Query logging for model training via PostgreSQL
- 🔍 Intelligent product recommendations

### Deployment & Scaling
- 🐳 Docker containerization
- ☸️ Kubernetes orchestration
- 📈 Horizontal Pod Autoscaling (HPA) at 70% CPU
- 🔄 Multi-node cluster support
- 🏥 Health checks and monitoring

## 📁 Project Structure

```
AWRest/
├── backend/
│   ├── app/
│   │   └── api_gateway.py          # Flask API Gateway
│   ├── services/
│   │   └── tornado_orders.py       # Tornado async service
│   ├── models/
│   │   └── database.py             # Database connections & models
│   ├── chatbot/
│   │   └── gradio_bot.py          # Gradio chatbot with GPT-4
│   └── configs/
│       └── config.py               # Configuration management
├── frontend/
│   ├── index.html                  # Main HTML
│   ├── styles.css                  # Styling
│   └── app.js                      # Frontend logic
├── docker/
│   ├── Dockerfile.flask            # Flask API container
│   ├── Dockerfile.tornado          # Tornado service container
│   └── Dockerfile.chatbot          # Gradio chatbot container
├── kubernetes/
│   ├── namespace-config.yaml       # K8s namespace & secrets
│   ├── mongodb.yaml                # MongoDB deployment
│   ├── postgres.yaml               # PostgreSQL deployment
│   ├── flask-api.yaml              # Flask API with HPA
│   ├── tornado-service.yaml        # Tornado with HPA
│   └── chatbot-service.yaml        # Chatbot with HPA
├── docker-compose.yml              # Local development setup
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
└── start.sh                        # Startup script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Kubernetes cluster (for production)
- AWS account (for DynamoDB)
- OpenAI API key (for GPT-4)

### Local Development with Docker Compose

1. **Clone and setup**:
```bash
cd AWRest
cp .env.example .env
```

2. **Configure environment** (edit `.env` with your API keys):
```bash
nano .env
# Add:
# - OpenAI API key
# - AWS credentials (or use LocalStack)
```

3. **Start services**:
```bash
chmod +x start.sh
./start.sh
```

4. **Access the application**:
- Frontend: http://localhost:8000
- API: http://localhost:5000/api/products
- Chatbot: http://localhost:7860
- MongoDB: localhost:27017
- PostgreSQL: localhost:5432

### Without Docker (Development)

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start MongoDB** (separate terminal):
```bash
mongod --dbpath ./data/mongodb
```

3. **Start PostgreSQL** (separate terminal):
```bash
# Ensure PostgreSQL is running on port 5432
```

4. **Start Tornado service** (separate terminal):
```bash
cd backend
python -c "from services.tornado_orders import start_tornado_service; start_tornado_service(None, 8001)"
```

5. **Start Flask API** (separate terminal):
```bash
cd backend
python -m flask run --host=0.0.0.0 --port=5000
```

6. **Start Gradio chatbot** (separate terminal):
```bash
cd backend
python -c "from chatbot.gradio_bot import launch_chatbot; launch_chatbot('your-api-key', None, None)"
```

7. **Serve frontend**:
```bash
cd frontend
python -m http.server 8000
```

## 🐳 Docker Compose Services

The `docker-compose.yml` includes:

- **MongoDB** (27017): Product listings
- **PostgreSQL** (5432): Chatbot queries
- **LocalStack** (4566): Local DynamoDB simulation
- **Flask API** (5000): Main API gateway
- **Tornado** (8001): Async order processing
- **Gradio Chatbot** (7860): AI assistant

Services automatically wait for dependencies and include health checks.

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

1. **Build and push images**:
```bash
docker build -f docker/Dockerfile.flask -t your-registry/labubu-flask:latest .
docker build -f docker/Dockerfile.tornado -t your-registry/labubu-tornado:latest .
docker build -f docker/Dockerfile.chatbot -t your-registry/labubu-chatbot:latest .

docker push your-registry/labubu-flask:latest
docker push your-registry/labubu-tornado:latest
docker push your-registry/labubu-chatbot:latest
```

2. **Deploy namespace and secrets**:
```bash
kubectl apply -f kubernetes/namespace-config.yaml

# Update secrets with your actual values
kubectl -n labubu-marketplace create secret generic labubu-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --from-literal=AWS_ACCESS_KEY_ID="..." \
  --from-literal=AWS_SECRET_ACCESS_KEY="..."
```

3. **Deploy databases**:
```bash
kubectl apply -f kubernetes/mongodb.yaml
kubectl apply -f kubernetes/postgres.yaml
```

4. **Deploy services**:
```bash
kubectl apply -f kubernetes/flask-api.yaml
kubectl apply -f kubernetes/tornado-service.yaml
kubectl apply -f kubernetes/chatbot-service.yaml
```

5. **Monitor HPA**:
```bash
kubectl -n labubu-marketplace get hpa -w
```

### Autoscaling Configuration (70% CPU Threshold)

All services include HorizontalPodAutoscaler with:
- **Minimum replicas**: 2
- **Maximum replicas**: 8-10 (service dependent)
- **CPU target**: 70% utilization
- **Memory target**: 80% utilization (Flask/Chatbot)
- **Scale-up**: Aggressive (100% increase, 10s period)
- **Scale-down**: Conservative (50% decrease, 300s stabilization)

## 🤖 Chatbot Features

The Gradio chatbot implements:

### RAG Pipeline
- Retrieves relevant products from MongoDB based on user queries
- Constructs context with product information
- Supplies context to GPT-4 for accurate responses

### Query Logging
- All user queries and responses logged to PostgreSQL
- Stores context (products shown) for each query
- Enables ML training and model improvement

### Conversation Management
- Maintains conversation history (last 6 messages)
- Allows chat reset
- User-specific interaction tracking

## 📊 API Endpoints

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details
- `POST /api/products/search` - Search products
- `POST /api/products` - Create product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Orders (Tornado Service)
- `POST /api/orders` - Create order
- `GET /api/orders/<id>` - Get order details
- `PATCH /api/orders/<id>` - Update order status

### System
- `GET /health` - Health check
- `GET /api/status` - System status

## 🔧 Configuration

### Environment Variables

Key variables in `.env`:

```
FLASK_ENV=development
MONGO_HOST=mongodb
DATABASE_URL=postgresql://...
AWS_REGION=us-east-1
OPENAI_API_KEY=sk-...
TORNADO_SERVICE_URL=http://tornado-service:8001
```

See `.env.example` for complete list.

## 🧪 Testing

### Test API endpoints:

```bash
# List products
curl http://localhost:5000/api/products

# Search products
curl -X POST http://localhost:5000/api/products/search \
  -H "Content-Type: application/json" \
  -d '{"query":"labubu"}'

# Create order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":"user1",
    "product_id":"123",
    "quantity":1,
    "total_price":150,
    "shipping_address":"123 Main St"
  }'

# Health check
curl http://localhost:5000/health
```

## 📈 Performance Considerations

### Optimization Strategies
1. **MongoDB indexing** on frequently queried fields
2. **Connection pooling** for PostgreSQL
3. **Tornado async handling** for I/O operations
4. **Kubernetes HPA** for dynamic scaling
5. **API rate limiting** (can be added)
6. **Caching layer** (Redis can be added)

### Monitoring
- Health check endpoints on all services
- Pod metrics via Kubernetes metrics-server
- Application logs via /health endpoint
- Database connection monitoring

## 🔐 Security Considerations

For production:

1. **Secrets Management**:
   - Use AWS Secrets Manager or HashiCorp Vault
   - Never commit `.env` files
   - Rotate credentials regularly

2. **API Security**:
   - Add authentication (JWT tokens)
   - Implement rate limiting
   - Use CORS policies appropriately
   - Add input validation

3. **Database Security**:
   - Enable MongoDB authentication
   - Use PostgreSQL SSL connections
   - Restrict network access

4. **Container Security**:
   - Use non-root users in containers
   - Enable pod security policies
   - Regular image scanning

5. **Data Protection**:
   - Encrypt data at rest
   - Use HTTPS/TLS for all communications
   - Implement data backup and recovery

## 🐛 Troubleshooting

### Services not connecting

```bash
# Check service health
kubectl -n labubu-marketplace get pods
kubectl -n labubu-marketplace describe pod <pod-name>

# View logs
kubectl -n labubu-marketplace logs <pod-name>
```

### Database connection issues

```bash
# MongoDB
mongosh --host mongodb:27017

# PostgreSQL
psql -h postgres -U labubu_user -d labubu_chatbot
```

### Docker Compose issues

```bash
# View logs
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Technologies Breakdown

### Flask API Gateway
- REST API using Flask and Flask-CORS
- Request routing and proxying
- Middleware for logging and validation
- Error handling and status codes

### Tornado Async Service
- Non-blocking HTTP server
- Async order processing
- DynamoDB integration
- Horizontal scaling support

### MongoDB
- Document storage for products
- Full-text search on product names/descriptions
- Indexing for performance
- Connection pooling

### PostgreSQL
- Structured storage for chatbot queries
- Foreign key relationships
- ACID compliance for transactional data
- Connection pooling

### DynamoDB
- NoSQL order storage
- Key-value with sorting key (timestamp)
- On-demand billing
- Global tables support

### Gradio
- User-friendly chat interface
- Real-time interaction
- Easy deployment
- Built-in sharing features

### Kubernetes
- Container orchestration
- Service discovery
- Rolling updates
- Horizontal Pod Autoscaling
- Multi-node support

## 📝 Future Enhancements

1. **Caching**: Add Redis for session and query caching
2. **Message Queue**: Add RabbitMQ/Kafka for async tasks
3. **ML Pipeline**: Train custom recommendation models
4. **Payment Gateway**: Stripe/PayPal integration
5. **Analytics**: Add comprehensive metrics/dashboards
6. **Admin Panel**: Dashboard for inventory management
7. **CI/CD**: GitHub Actions for automated deployment
8. **Monitoring**: Prometheus + Grafana for metrics

## 📄 License

This project is provided as-is for demonstration purposes.

## 👤 Author

Built as a demonstration of enterprise e-commerce architecture with modern cloud-native technologies.

---

**Last Updated**: March 2024