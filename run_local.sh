#!/bin/bash

# Script para correr la interfaz localmente

echo "🍺 Iniciando Beer Tasting Cicerone..."
echo ""

# Verificar que exista el archivo de secrets
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  No se encontró .streamlit/secrets.toml"
    echo ""
    echo "Crea el archivo con tus credenciales:"
    echo "  cp .streamlit/secrets.toml.example .streamlit/secrets.toml"
    echo "  # Luego edita el archivo con tus credenciales reales"
    echo ""
    exit 1
fi

# Verificar que boto3 esté instalado
python -c "import boto3" 2>/dev/null || {
    echo "⚠️  boto3 no está instalado"
    echo "Instalando dependencias..."
    pip install boto3
}

# Iniciar Streamlit
echo "🚀 Iniciando interfaz en http://localhost:8501"
echo ""
streamlit run chat.py
