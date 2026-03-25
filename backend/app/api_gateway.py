"""
Flask API Gateway for Labubu Marketplace
Routes all API requests and integrates MongoDB, DynamoDB, PostgreSQL, and async services
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database connections and models
from models.database import (
    MongoDBConnection, DynamoDBConnection, PostgreSQLConnection, ProductListing
)
from configs.config import config, Config

# Create Flask app
app = Flask(__name__)
environment = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[environment])

# Enable CORS
CORS(app)

# Global database connections
mongo_conn = None
dynamodb_conn = None
postgres_conn = None

# Database instances
mongo_db = None
dynamodb_table = None
postgres_pool = None


def init_databases():
    """Initialize all database connections"""
    global mongo_db, dynamodb_table, postgres_pool
    
    try:
        # MongoDB
        mongo_connection = MongoDBConnection(app.config)
        mongo_db = mongo_connection.connect()
        print("✓ MongoDB connected")
        
        # DynamoDB
        dynamodb_connection = DynamoDBConnection(app.config)
        dynamodb_client = dynamodb_connection.connect()
        dynamodb_table = dynamodb_connection.get_table()
        print("✓ DynamoDB connected")
        
        # PostgreSQL
        postgres_connection = PostgreSQLConnection(app.config)
        postgres_pool = postgres_connection.connect()
        print("✓ PostgreSQL connected")
        
    except Exception as e:
        print(f"Error initializing databases: {e}")
        raise


# Middleware for request logging
@app.before_request
def log_request():
    """Log incoming requests"""
    app.logger.info(f"{request.method} {request.path}")


def require_json(f):
    """Decorator to require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function


# ==================== Product Listing Routes ====================

@app.route('/api/products', methods=['GET'])
def list_products():
    """Get all active product listings with pagination"""
    try:
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        products = ProductListing.find_all_active(mongo_db, skip, limit)
        
        result = []
        for product in products:
            product['_id'] = str(product['_id'])
            result.append(product)
        
        return jsonify({
            'success': True,
            'count': len(result),
            'products': result
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = ProductListing.find_by_id(mongo_db, product_id)
        
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        product['_id'] = str(product['_id'])
        return jsonify({'success': True, 'product': product}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/search', methods=['POST'])
@require_json
def search_products():
    """Search products by name and description"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        skip = data.get('skip', 0)
        limit = data.get('limit', 20)
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        products = ProductListing.search(mongo_db, query, skip, limit)
        
        result = []
        for product in products:
            product['_id'] = str(product['_id'])
            result.append(product)
        
        return jsonify({
            'success': True,
            'count': len(result),
            'query': query,
            'products': result
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products', methods=['POST'])
@require_json
def create_product():
    """Create a new product listing"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'price', 'character_name', 'seller_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        product_id = ProductListing.create(mongo_db, data)
        
        return jsonify({
            'success': True,
            'product_id': product_id,
            'message': 'Product created successfully'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<product_id>', methods=['PUT'])
@require_json
def update_product(product_id):
    """Update a product listing"""
    try:
        data = request.get_json()
        
        success = ProductListing.update(mongo_db, product_id, data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Product updated successfully'
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product listing"""
    try:
        success = ProductListing.delete(mongo_db, product_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Product deleted successfully'
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Order Routes (via Tornado) ====================

@app.route('/api/orders', methods=['POST'])
@require_json
def create_order():
    """Create a new order (proxied to Tornado service)"""
    try:
        data = request.get_json()
        
        tornado_url = app.config.TORNADO_SERVICE_URL
        response = requests.post(f'{tornado_url}/api/orders', json=data, timeout=5)
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Tornado service error: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details (proxied to Tornado service)"""
    try:
        tornado_url = app.config.TORNADO_SERVICE_URL
        response = requests.get(f'{tornado_url}/api/orders/{order_id}', timeout=5)
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Tornado service error: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/orders/<order_id>', methods=['PATCH'])
@require_json
def update_order(order_id):
    """Update order status (proxied to Tornado service)"""
    try:
        data = request.get_json()
        
        tornado_url = app.config.TORNADO_SERVICE_URL
        response = requests.patch(f'{tornado_url}/api/orders/{order_id}', json=data, timeout=5)
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Tornado service error: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Health Check ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'flask-api-gateway',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status including all services"""
    status_info = {
        'flask_gateway': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Check MongoDB
    try:
        mongo_db.command('ping')
        status_info['mongodb'] = 'healthy'
    except:
        status_info['mongodb'] = 'unhealthy'
    
    # Check Tornado service
    try:
        response = requests.get(f'{app.config.TORNADO_SERVICE_URL}/health', timeout=2)
        status_info['tornado_service'] = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        status_info['tornado_service'] = 'unreachable'
    
    return jsonify(status_info), 200


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ==================== Initialize and Run ====================

if __name__ == '__main__':
    try:
        init_databases()
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=app.config.DEBUG
        )
    except Exception as e:
        print(f"Failed to start application: {e}")
        exit(1)
