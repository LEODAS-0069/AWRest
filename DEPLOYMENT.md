# Deployment Guide

## Quick Start - Docker Compose (Development)

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API key (optional, for chatbot)
- AWS credentials (optional, for real DynamoDB)

### Steps

1. **Clone the repository**:
```bash
cd AWRest
```

2. **Setup environment**:
```bash
cp .env.example .env
# Edit .env and add your API keys
nano .env
```

3. **Start all services**:
```bash
chmod +x start.sh
./start.sh
```

4. **Access services**:
- Frontend: http://localhost:8000
- API Gateway: http://localhost:5000
- Chatbot: http://localhost:7860

5. **Stop services**:
```bash
docker-compose down
```

---

## Production - Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.20+)
- kubectl installed and configured
- Docker registry (Docker Hub, ECR, GCR, etc.)
- AWS account with DynamoDB access
- OpenAI API key
- Helm (optional, for advanced deployments)

### Step-by-Step Deployment

#### 1. Build and Push Docker Images

```bash
# Build images
docker build -f docker/Dockerfile.flask -t your-registry/labubu-flask:v1.0 .
docker build -f docker/Dockerfile.tornado -t your-registry/labubu-tornado:v1.0 .
docker build -f docker/Dockerfile.chatbot -t your-registry/labubu-chatbot:v1.0 .

# Push to registry
docker push your-registry/labubu-flask:v1.0
docker push your-registry/labubu-tornado:v1.0
docker push your-registry/labubu-chatbot:v1.0
```

#### 2. Update Kubernetes Manifests

Update image references in:
- `kubernetes/flask-api.yaml`
- `kubernetes/tornado-service.yaml`
- `kubernetes/chatbot-service.yaml`

Change `imagePullPolicy: Never` to `imagePullPolicy: Always` and update image references to your registry.

#### 3. Configure Secrets

Create a secrets file with your credentials:

```bash
kubectl -n labubu-marketplace create secret generic labubu-secrets \
  --from-literal=DATABASE_URL="postgresql://labubu_user:your-password@postgres:5432/labubu_chatbot" \
  --from-literal=OPENAI_API_KEY="sk-your-openai-key" \
  --from-literal=AWS_ACCESS_KEY_ID="your-aws-access-key" \
  --from-literal=AWS_SECRET_ACCESS_KEY="your-aws-secret-key" \
  --from-literal=SECRET_KEY="your-flask-secret-key"
```

#### 4. Deploy to Kubernetes

```bash
# Make deployment script executable
chmod +x deploy-k8s.sh

# Run deployment
./deploy-k8s.sh your-registry

# Or manually apply manifests
kubectl apply -f kubernetes/namespace-config.yaml
kubectl apply -f kubernetes/mongodb.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/flask-api.yaml
kubectl apply -f kubernetes/tornado-service.yaml
kubectl apply -f kubernetes/chatbot-service.yaml
```

#### 5. Verify Deployment

```bash
# Check pods
kubectl -n labubu-marketplace get pods

# Check services
kubectl -n labubu-marketplace get svc

# Check HPA
kubectl -n labubu-marketplace get hpa

# View logs
kubectl -n labubu-marketplace logs -f deployment/flask-api
```

#### 6. Access Services

```bash
# Get service details
kubectl -n labubu-marketplace get svc

# For LoadBalancer services, get external IP
kubectl -n labubu-marketplace get svc flask-api -w

# Port-forward if needed
kubectl -n labubu-marketplace port-forward svc/flask-api 5000:5000
```

---

## Autoscaling Configuration

All services are configured with Horizontal Pod Autoscaler (HPA):

### Flask API Service
- Min replicas: 2
- Max replicas: 10
- CPU target: 70% utilization
- Memory target: 80% utilization

### Tornado Service
- Min replicas: 2
- Max replicas: 10
- CPU target: 70% utilization

### Chatbot Service
- Min replicas: 2
- Max replicas: 8
- CPU target: 70% utilization

### Monitor Scaling

```bash
# Watch HPA in action
kubectl -n labubu-marketplace get hpa -w

# Generate load to trigger scaling
kubectl -n labubu-marketplace run -it --image=busybox load-generator -- /bin/sh
# Inside container: while sleep 0.01; do wget -q -O- http://flask-api:5000/api/products; done
```

---

## Advanced Deployment

### Using Helm

Create a `values.yaml`:

```yaml
flask:
  replicas: 2
  image: your-registry/labubu-flask:v1.0
  resources:
    requests:
      cpu: 200m
      memory: 512Mi

tornado:
  replicas: 2
  image: your-registry/labubu-tornado:v1.0

chatbot:
  replicas: 2
  image: your-registry/labubu-chatbot:v1.0

mongodb:
  storage: 10Gi

postgres:
  storage: 10Gi
```

### Using GitOps (ArgoCD)

Add to your ArgoCD Application:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: labubu-marketplace
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/labubu-marketplace
    targetRevision: HEAD
    path: kubernetes/
  destination:
    server: https://kubernetes.default.svc
    namespace: labubu-marketplace
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Using Kustomize

Create `kubernetes/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: labubu-marketplace

resources:
  - namespace-config.yaml
  - mongodb.yaml
  - postgres.yaml
  - flask-api.yaml
  - tornado-service.yaml
  - chatbot-service.yaml

commonLabels:
  app: labubu-marketplace
  version: v1.0
```

Deploy with:
```bash
kubectl apply -k kubernetes/
```

---

## Monitoring & Observability

### Prometheus Metrics

Add to service manifests:

```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: flask-api
spec:
  selector:
    matchLabels:
      app: flask-api
  endpoints:
  - port: metrics
    interval: 30s
```

### Logging

View logs across all services:

```bash
# All services
kubectl -n labubu-marketplace logs -f -l app=labubu-marketplace

# Specific service
kubectl -n labubu-marketplace logs -f deployment/flask-api --tail=100
```

### Distributed Tracing (Jaeger)

Add environment variables for tracing:

```yaml
env:
  - name: JAEGER_AGENT_HOST
    value: jaeger-agent
  - name: JAEGER_AGENT_PORT
    value: "6831"
```

---

## Scaling Best Practices

### CPU-based Scaling
- Set resource requests/limits appropriately
- Monitor actual usage patterns
- Adjust HPA thresholds based on load testing

### Application-level Optimization
- Use connection pooling
- Implement caching (Redis)
- Optimize database queries
- Use async/await patterns

### Infrastructure Optimization
- Use spot instances for cost savings
- Configure cluster autoscaler
- Use node affinity for performance
- Implement pod disruption budgets

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: flask-api-pdb
  namespace: labubu-marketplace
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: flask-api
```

---

## Backup & Recovery

### Database Backups

MongoDB:
```bash
kubectl -n labubu-marketplace exec deployment/mongodb -- \
  mongodump --out /tmp/backup
```

PostgreSQL:
```bash
kubectl -n labubu-marketplace exec deployment/postgres -- \
  pg_dump -U labubu_user labubu_chatbot > backup.sql
```

### PVC Snapshots

```bash
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: mongodb-snapshot
  namespace: labubu-marketplace
spec:
  volumeSnapshotClassName: default
  source:
    persistentVolumeClaimName: mongodb-pvc
```

---

## Troubleshooting

### Services not starting

```bash
# Check pod status
kubectl -n labubu-marketplace describe pod <pod-name>

# Check events
kubectl -n labubu-marketplace get events --sort-by='.lastTimestamp'

# View logs
kubectl -n labubu-marketplace logs <pod-name> --previous
```

### HPA not scaling

```bash
# Check HPA status
kubectl -n labubu-marketplace describe hpa flask-api-hpa

# Check metrics-server
kubectl get deployment metrics-server -n kube-system

# Check pod metrics
kubectl -n labubu-marketplace top pods
```

### Database connection issues

```bash
# Test MongoDB
kubectl -n labubu-marketplace exec -it deployment/mongodb -- mongosh

# Test PostgreSQL
kubectl -n labubu-marketplace exec -it deployment/postgres -- \
  psql -U labubu_user -d labubu_chatbot
```

---

## Cost Optimization

1. **Use minimal resource requests**:
```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
```

2. **Configure cluster autoscaler**:
- Scale nodes up/down based on demand
- Use spot instances for non-critical workloads

3. **Database optimization**:
- Use managed services (AWS RDS instead of self-managed)
- Configure appropriate backup retention
- Monitor query performance

4. **Network optimization**:
- Use internal DNS for inter-service communication
- Implement connection pooling
- Cache frequently accessed data

---

## Security Hardening

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: labubu-network-policy
  namespace: labubu-marketplace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector: {}
```

### Pod Security Policies

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
```

### RBAC Configuration

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: flask-api-viewer
  namespace: labubu-marketplace
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: view
subjects:
- kind: ServiceAccount
  name: default
  namespace: labubu-marketplace
```

---

Last Updated: March 2024
