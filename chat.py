"""
Beer Tasting Agent - Public Chat Interface

This is a wrapper that uses boto3 to invoke the AgentCore runtime directly,
allowing deployment to Streamlit Cloud without exposing AWS credentials.

The credentials are stored securely in Streamlit secrets.
"""

import os
import json
import uuid
import streamlit as st
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

# Page configuration
st.set_page_config(
    page_title="Beer Tasting Cicerone",
    page_icon="🍺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
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


def get_agentcore_client():
    """Initialize AgentCore client with credentials.
    
    Supports:
    - IAM role when running on App Runner (recommended for production)
    - Streamlit secrets for local development
    - Session tokens for temporary credentials (AWS SSO, AssumeRole, etc.)
    """
    try:
        # Try to get credentials from Streamlit secrets (for local development)
        if hasattr(st, 'secrets') and 'aws' in st.secrets:
            client_kwargs = {
                'region_name': st.secrets['aws']['region'],
                'aws_access_key_id': st.secrets['aws']['access_key_id'],
                'aws_secret_access_key': st.secrets['aws']['secret_access_key']
            }
            
            # Add session token if present (for temporary credentials)
            if 'session_token' in st.secrets['aws']:
                client_kwargs['aws_session_token'] = st.secrets['aws']['session_token']
            
            return boto3.client('bedrock-agentcore', **client_kwargs)
        else:
            # Use IAM role (App Runner) or environment credentials
            return boto3.client(
                'bedrock-agentcore',
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
    except Exception as e:
        st.error(f"Error al conectar con AWS: {str(e)}")
        return None


def get_agent_arn():
    """Get the agent ARN from secrets or environment."""
    if hasattr(st, 'secrets') and 'agentcore' in st.secrets:
        return st.secrets['agentcore']['agent_arn']
    return os.getenv('AGENT_RUNTIME_ARN') or os.getenv('AGENTCORE_AGENT_ARN')


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        # Generate a session ID that meets AgentCore requirements (min 33 chars)
        st.session_state.session_id = f"streamlit-session-{uuid.uuid4()}"
    
    if "started_at" not in st.session_state:
        st.session_state.started_at = datetime.now()


def reset_session():
    """Reset the current tasting session."""
    st.session_state.messages = []
    st.session_state.session_id = f"streamlit-session-{uuid.uuid4()}"
    st.session_state.started_at = datetime.now()


def invoke_agent(user_message: str, session_id: str):
    """Invoke the AgentCore runtime with user message.
    
    Args:
        user_message: The user's input message
        session_id: Current session identifier
        
    Returns:
        Response text from the agent, or None if request fails
    """
    client = get_agentcore_client()
    if not client:
        return None
    
    agent_arn = get_agent_arn()
    if not agent_arn:
        st.error("⚠️ Agent ARN no configurado. Verifica la configuración.")
        return None
    
    try:
        # Prepare payload
        payload = json.dumps({
            "prompt": user_message,
            "session_id": session_id
        }).encode('utf-8')
        
        # Invoke agent
        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_arn,
            runtimeSessionId=session_id,
            payload=payload
        )
        
        # Parse response
        response_body = response['response'].read()
        result = json.loads(response_body)
        
        return result.get('response', 'Lo siento, no recibí una respuesta válida.')
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ThrottlingException':
            st.error("⏱️ Demasiadas solicitudes. Por favor, espera un momento.")
        elif error_code == 'ValidationException':
            st.error("❌ Error de validación. Verifica la configuración.")
        else:
            st.error(f"❌ Error de AWS: {error_code}")
        return None
        
    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")
        return None


def render_sidebar():
    """Render the sidebar with session controls and information."""
    with st.sidebar:
        st.title("🍺 Beer Tasting Cicerone")
        st.markdown("---")
        
        # Session information
        st.subheader("Información de Sesión")
        st.text(f"ID: {st.session_state.session_id[:20]}...")
        
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


def render_chat_history():
    """Render the conversation history."""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)


def main():
    """Main application entry point."""
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
                assistant_response = invoke_agent(prompt, st.session_state.session_id)
                
                if assistant_response:
                    st.markdown(assistant_response)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
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
