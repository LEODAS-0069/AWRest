"""
Database models and connections
"""
from pymongo import MongoClient
import boto3
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from datetime import datetime


class MongoDBConnection:
    """MongoDB connection for listings"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish MongoDB connection"""
        self.client = MongoClient(
            host=self.config.MONGO_HOST,
            port=self.config.MONGO_PORT
        )
        self.db = self.client[self.config.MONGO_DB]
        # Create indexes
        self._create_indexes()
        return self.db
    
    def _create_indexes(self):
        """Create database indexes"""
        listings = self.db['listings']
        listings.create_index('product_id', unique=True)
        listings.create_index('status')
        listings.create_index('seller_id')
    
    def get_db(self):
        """Get database instance"""
        return self.db
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()


class DynamoDBConnection:
    """DynamoDB connection for orders"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
    
    def connect(self):
        """Establish DynamoDB connection"""
        self.client = boto3.resource(
            'dynamodb',
            region_name=self.config.AWS_REGION,
            aws_access_key_id=self.config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY
        )
        self._create_table()
        return self.client
    
    def _create_table(self):
        """Create DynamoDB table if not exists"""
        try:
            table = self.client.Table(self.config.DYNAMODB_ORDERS_TABLE)
            table.load()
        except:
            self.client.create_table(
                TableName=self.config.DYNAMODB_ORDERS_TABLE,
                KeySchema=[
                    {'AttributeName': 'order_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'order_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'N'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
    
    def get_table(self):
        """Get orders table"""
        return self.client.Table(self.config.DYNAMODB_ORDERS_TABLE)


class PostgreSQLConnection:
    """PostgreSQL connection for chatbot queries"""
    
    def __init__(self, config):
        self.config = config
        self.pool = None
    
    def connect(self):
        """Establish PostgreSQL connection pool"""
        self.pool = SimpleConnectionPool(1, 20, self.config.DATABASE_URL)
        self._create_tables()
        return self.pool
    
    def _create_tables(self):
        """Create required tables"""
        conn = self.pool.getconn()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chatbot_queries (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                query TEXT NOT NULL,
                response TEXT,
                context_products JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_views (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                product_id VARCHAR(255),
                viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)
    
    def get_connection(self):
        """Get connection from pool"""
        return self.pool.getconn()
    
    def put_connection(self, conn):
        """Return connection to pool"""
        self.pool.putconn(conn)


# Database models
class ProductListing:
    """Product listing model for MongoDB"""
    
    @staticmethod
    def create(db, product_data):
        """Create a new product listing"""
        product_data['created_at'] = datetime.utcnow()
        product_data['status'] = 'active'
        result = db['listings'].insert_one(product_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(db, product_id):
        """Find product by ID"""
        from bson.objectid import ObjectId
        return db['listings'].find_one({'_id': ObjectId(product_id)})
    
    @staticmethod
    def find_all_active(db, skip=0, limit=20):
        """Find all active listings with pagination"""
        return db['listings'].find({'status': 'active'}).skip(skip).limit(limit)
    
    @staticmethod
    def search(db, query, skip=0, limit=20):
        """Search products by name or description"""
        return db['listings'].find({
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }).skip(skip).limit(limit)
    
    @staticmethod
    def update(db, product_id, update_data):
        """Update product listing"""
        from bson.objectid import ObjectId
        result = db['listings'].update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(db, product_id):
        """Delete product listing"""
        from bson.objectid import ObjectId
        result = db['listings'].delete_one({'_id': ObjectId(product_id)})
        return result.deleted_count > 0
