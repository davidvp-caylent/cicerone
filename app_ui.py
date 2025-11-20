"""
Beer Tasting Agent - Streamlit Web Interface

This module provides a simple chat interface for interacting with the Beer Tasting Agent
deployed on Amazon Bedrock AgentCore Runtime.

Validates: Requirements 6.1, 6.2, 6.3, 6.4
"""

import os
import uuid
import json
import streamlit as st
import boto3
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AGENT_RUNTIME_ARN = os.getenv('AGENT_RUNTIME_ARN', 'arn:aws:bedrock-agentcore:us-east-1:131578276461:runtime/cicerone-szUAIIHGxh')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
QUALIFIER = os.getenv('QUALIFIER', 'DEFAULT')
REQUEST_TIMEOUT = 30  # 30 seconds timeout for agent responses

# Page configuration
st.set_page_config(
    page_title="Beer Tasting Cicerone",
    page_icon="🍺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .main {
        max-width: 800px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables.
    
    Validates: Requirements 6.3, 6.4 - Session management and conversation history
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "started_at" not in st.session_state:
        st.session_state.started_at = datetime.now()


def reset_session():
    """Reset the current tasting session.
    
    Validates: Requirements 6.4 - Clear previous conversation history and initialize new session
    """
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.started_at = datetime.now()


def call_agent(user_message: str, session_id: str) -> Optional[Dict[str, Any]]:
    """Call the AgentCore endpoint with user message using boto3.
    
    Args:
        user_message: The user's input message
        session_id: Current session identifier (must be 33+ characters)
        
    Returns:
        Response dictionary from the agent, or None if request fails
        
    Validates: Requirements 6.2 - Agent response within timeout
    """
    try:
        # Ensure session_id is at least 33 characters
        if len(session_id) < 33:
            session_id = session_id + "-" + str(uuid.uuid4())
        
        # Create boto3 client
        client = boto3.client('bedrock-agentcore', region_name=AWS_REGION)
        
        # Prepare payload
        payload = json.dumps({
            "prompt": user_message,
            "session_id": session_id
        })
        
        # Invoke agent runtime
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=payload,
            qualifier=QUALIFIER
        )
        
        # Read and parse response
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        return response_data
        
    except client.exceptions.ThrottlingException:
        st.error("⏱️ Demasiadas solicitudes. Por favor, espera un momento e intenta de nuevo.")
        return None
        
    except client.exceptions.ValidationException as e:
        st.error(f"❌ Error de validación: {str(e)}")
        return None
        
    except client.exceptions.ResourceNotFoundException:
        st.error("🔌 No se encontró el agente. Verifica la configuración.")
        return None
        
    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")
        return None


def render_sidebar():
    """Render the sidebar with session controls and information.
    
    Validates: Requirements 6.4 - New session button
    """
    with st.sidebar:
        st.title("🍺 Beer Tasting Cicerone")
        st.markdown("---")
        
        # Session information
        st.subheader("Información de Sesión")
        st.text(f"ID: {st.session_state.session_id[:8]}...")
        
        if st.session_state.started_at:
            duration = datetime.now() - st.session_state.started_at
            minutes = int(duration.total_seconds() / 60)
            st.text(f"Duración: {minutes} min")
        
        st.text(f"Mensajes: {len(st.session_state.messages)}")
        
        st.markdown("---")
        
        # New session button
        if st.button("🔄 Nueva Sesión", use_container_width=True):
            reset_session()
            st.rerun()
        
        st.markdown("---")
        
        # Help section
        with st.expander("ℹ️ Cómo usar"):
            st.markdown("""
            **Bienvenido al Beer Tasting Cicerone!**
            
            Este asistente te ayudará durante tu cata de cerveza:
            
            - 🍺 Pregunta sobre cervezas disponibles
            - 📝 Comparte tus impresiones de cada cerveza
            - 🎯 Recibe predicciones sobre tu favorita
            - 🍽️ Obtén recomendaciones de maridaje
            - 📚 Aprende sobre estilos y técnicas
            
            **Ejemplos de preguntas:**
            - "¿Qué cervezas hay disponibles?"
            - "Cuéntame sobre la IPA"
            - "¿Qué comida va bien con esta cerveza?"
            - "¿Cuál crees que será mi favorita?"
            """)
        
        # Configuration section
        with st.expander("⚙️ Configuración"):
            st.text(f"Agent ARN: ...{AGENT_RUNTIME_ARN[-20:]}")
            st.text(f"Region: {AWS_REGION}")
            st.text(f"Qualifier: {QUALIFIER}")
            st.text(f"Timeout: {REQUEST_TIMEOUT}s")


def render_chat_history():
    """Render the conversation history.
    
    Validates: Requirements 6.3 - Display conversation history
    """
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)


def main():
    """Main application entry point.
    
    Validates: Requirements 6.1, 6.2, 6.3, 6.4 - Complete web interface functionality
    """
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main chat interface
    st.title("🍺 Beer Tasting Cicerone")
    st.markdown("*Tu experto personal en catas de cerveza*")
    st.markdown("---")
    
    # Display welcome message if no messages yet
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            welcome_message = """
            ¡Hola! 👋 Soy tu cicerone de cerveza personal. Estoy aquí para ayudarte durante tu cata.
            
            Puedo ayudarte a:
            - Conocer las cervezas disponibles
            - Guiarte en la evaluación de cada cerveza
            - Predecir cuál será tu favorita
            - Sugerir maridajes de comida
            - Enseñarte sobre estilos y técnicas de cata
            
            ¿Por dónde te gustaría empezar?
            """
            st.markdown(welcome_message)
    
    # Render chat history
    render_chat_history()
    
    # Chat input
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Call agent and display response
        with st.chat_message("assistant"):
            with st.spinner("Pensando... 🤔"):
                response_data = call_agent(prompt, st.session_state.session_id)
                
                if response_data and response_data.get("response"):
                    assistant_response = response_data["response"]
                    st.markdown(assistant_response)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                    # Display metadata if available
                    if response_data.get("metadata"):
                        metadata = response_data["metadata"]
                        if metadata.get("beers_tasted_count", 0) > 0:
                            st.caption(f"🍺 Cervezas probadas: {metadata['beers_tasted_count']}")
                else:
                    error_message = "Lo siento, no pude procesar tu mensaje. Por favor, intenta de nuevo."
                    st.markdown(error_message)
                    
                    # Add error message to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })


if __name__ == "__main__":
    main()
