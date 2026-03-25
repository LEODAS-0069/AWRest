"""
Configuration management for Labubu marketplace
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/labubu_listings')
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
    MONGO_DB = os.getenv('MONGO_DB', 'labubu_listings')
    
    # DynamoDB
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    DYNAMODB_ORDERS_TABLE = os.getenv('DYNAMODB_ORDERS_TABLE', 'labubu_orders')
    
    # PostgreSQL
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/labubu_chatbot')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Service URLs
    TORNADO_SERVICE_URL = os.getenv('TORNADO_SERVICE_URL', 'http://localhost:8001')
    CHATBOT_SERVICE_URL = os.getenv('CHATBOT_SERVICE_URL', 'http://localhost:7860')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'postgresql://user:password@localhost:5432/labubu_test'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
