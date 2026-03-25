"""
Gradio chatbot with GPT-4 integration and RAG pipeline for product information
"""
import gradio as gr
import openai
from typing import List, Tuple
import json
from datetime import datetime


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline"""
    
    def __init__(self, mongo_db, pg_connection_pool):
        self.mongo_db = mongo_db
        self.pg_pool = pg_connection_pool
    
    def retrieve_products(self, query: str, limit: int = 5) -> List[dict]:
        """Retrieve relevant products from MongoDB based on query"""
        try:
            products = list(self.mongo_db['listings'].find({
                '$or': [
                    {'name': {'$regex': query, '$options': 'i'}},
                    {'description': {'$regex': query, '$options': 'i'}},
                    {'character_name': {'$regex': query, '$options': 'i'}}
                ],
                'status': 'active'
            }).limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for product in products:
                product['_id'] = str(product['_id'])
            
            return products
        except Exception as e:
            print(f"Error retrieving products: {e}")
            return []
    
    def build_context(self, products: List[dict]) -> str:
        """Build context string from retrieved products"""
        if not products:
            return "No products found matching your query."
        
        context = "Here are the relevant Labubu products we found:\n\n"
        for i, product in enumerate(products, 1):
            context += f"{i}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')}\n"
            context += f"   Character: {product.get('character_name', 'N/A')}\n"
            context += f"   Condition: {product.get('condition', 'N/A')}\n"
            context += f"   Description: {product.get('description', 'N/A')[:200]}...\n\n"
        
        return context
    
    def log_query(self, user_id: str, query: str, response: str, products: List[dict]):
        """Log chatbot query to PostgreSQL for model training"""
        try:
            conn = self.pg_pool.getconn()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chatbot_queries (user_id, query, response, context_products, created_at)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                user_id,
                query,
                response,
                json.dumps([p.get('_id') for p in products]),
                datetime.utcnow()
            ))
            
            conn.commit()
            cursor.close()
            self.pg_pool.putconn(conn)
        except Exception as e:
            print(f"Error logging query: {e}")


class LabuboChatbot:
    """GPT-4 powered chatbot for Labubu marketplace"""
    
    def __init__(self, openai_api_key: str, mongo_db, pg_pool):
        openai.api_key = openai_api_key
        self.rag_pipeline = RAGPipeline(mongo_db, pg_pool)
        self.conversation_history = []
        self.system_prompt = """You are a helpful customer service chatbot for a Labubu marketplace specializing 
in selling used Labubu designer toys. You help customers find products, answer questions about Labubus, 
and provide information about orders and shipping. Be friendly, knowledgeable, and helpful."""
    
    def chat(self, user_message: str, user_id: str = "anonymous") -> Tuple[str, str]:
        """
        Process user message and return response
        Returns: (response, context_used)
        """
        try:
            # Retrieve relevant products using RAG
            products = self.rag_pipeline.retrieve_products(user_message)
            context = self.rag_pipeline.build_context(products)
            
            # Build messages for GPT-4
            messages = [
                {
                    "role": "system",
                    "content": f"{self.system_prompt}\n\nProduct Context:\n{context}"
                }
            ]
            
            # Add conversation history
            for msg in self.conversation_history[-6:]:  # Last 6 messages for context
                messages.append(msg)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call GPT-4
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response['choices'][0]['message']['content']
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Log query for training
            self.rag_pipeline.log_query(
                user_id=user_id,
                query=user_message,
                response=assistant_message,
                products=products
            )
            
            context_summary = f"Used {len(products)} product(s) as context"
            return assistant_message, context_summary
            
        except Exception as e:
            error_message = f"I encountered an error: {str(e)}"
            return error_message, "Error"
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        return "Conversation cleared."


def create_gradio_interface(openai_api_key: str, mongo_db, pg_pool):
    """Create Gradio interface for the chatbot"""
    
    chatbot_instance = LabuboChatbot(openai_api_key, mongo_db, pg_pool)
    
    def chat_interface(message, history):
        """Gradio chat interface"""
        response, context = chatbot_instance.chat(message)
        return response
    
    def reset_interface():
        """Reset chat"""
        chatbot_instance.reset_conversation()
        return "Chat reset. How can I help you find your favorite Labubu today?"
    
    # Create interface
    with gr.Blocks(title="Labubu Marketplace Chatbot") as interface:
        gr.Markdown("# 🧸 Labubu Marketplace Assistant")
        gr.Markdown("Ask me anything about our Labubu inventory, characters, pricing, or orders!")
        
        chatbot = gr.Chatbot(label="Chat History")
        
        with gr.Row():
            message_input = gr.Textbox(
                label="Your Message",
                placeholder="Ask me about Labubus...",
                scale=9
            )
            submit_btn = gr.Button("Send", scale=1)
        
        reset_btn = gr.Button("🔄 Reset Chat")
        
        # Event handlers
        submit_btn.click(
            chat_interface,
            inputs=[message_input, chatbot],
            outputs=chatbot
        )
        
        message_input.submit(
            chat_interface,
            inputs=[message_input, chatbot],
            outputs=chatbot
        )
        
        reset_btn.click(
            reset_interface,
            outputs=chatbot
        )
    
    return interface


def launch_chatbot(openai_api_key: str, mongo_db, pg_pool, port: int = 7860):
    """Launch Gradio chatbot"""
    interface = create_gradio_interface(openai_api_key, mongo_db, pg_pool)
    interface.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )
