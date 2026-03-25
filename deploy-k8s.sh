#!/bin/bash
# Deploy Labubu Marketplace to Kubernetes

set -e

NAMESPACE="labubu-marketplace"
REGISTRY="${1:-local}"

echo "🚀 Deploying Labubu Marketplace to Kubernetes"
echo "Namespace: $NAMESPACE"
echo "Registry: $REGISTRY"
echo ""

# Create namespace and secrets
echo "📦 Applying namespace and configuration..."
kubectl apply -f kubernetes/namespace-config.yaml

# Update image registry if needed
if [ "$REGISTRY" != "local" ]; then
    echo "🔧 Updating image registry to: $REGISTRY"
    sed -i "s|labubu-flask:latest|$REGISTRY/labubu-flask:latest|g" kubernetes/flask-api.yaml
    sed -i "s|labubu-tornado:latest|$REGISTRY/labubu-tornado:latest|g" kubernetes/tornado-service.yaml
    sed -i "s|labubu-chatbot:latest|$REGISTRY/labubu-chatbot:latest|g" kubernetes/chatbot-service.yaml
fi

# Deploy databases
echo "🗄️  Deploying databases..."
kubectl apply -f kubernetes/mongodb.yaml
kubectl apply -f kubernetes/postgres.yaml

# Wait for databases to be ready
echo "⏳ Waiting for databases to be ready..."
kubectl -n $NAMESPACE wait --for=condition=ready pod -l app=mongodb --timeout=300s 2>/dev/null || true
kubectl -n $NAMESPACE wait --for=condition=ready pod -l app=postgres --timeout=300s 2>/dev/null || true

# Deploy services
echo "🚀 Deploying services..."
kubectl apply -f kubernetes/flask-api.yaml
kubectl apply -f kubernetes/tornado-service.yaml
kubectl apply -f kubernetes/chatbot-service.yaml

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Check deployment status:"
echo "   kubectl -n $NAMESPACE get pods"
echo "   kubectl -n $NAMESPACE get svc"
echo "   kubectl -n $NAMESPACE get hpa"
echo ""
echo "📊 Monitor HPA scaling:"
echo "   kubectl -n $NAMESPACE get hpa -w"
echo ""
echo "🔍 View logs:"
echo "   kubectl -n $NAMESPACE logs -f deployment/flask-api"
echo "   kubectl -n $NAMESPACE logs -f deployment/tornado-service"
echo "   kubectl -n $NAMESPACE logs -f deployment/chatbot-service"
echo ""
