web: gunicorn --bind 0.0.0.0:$PORT --workers 4 backend.app.api_gateway:app
worker: python backend/services/tornado_orders.py
chatbot: python -c "from backend.chatbot.gradio_bot import launch_chatbot; from backend.models.database import MongoDBConnection, PostgreSQLConnection; from backend.configs.config import Config; mongo_conn = MongoDBConnection(Config()); mongo_db = mongo_conn.connect(); pg_conn = PostgreSQLConnection(Config()); pg_pool = pg_conn.connect(); launch_chatbot(Config().OPENAI_API_KEY, mongo_db, pg_pool, 7860)"
