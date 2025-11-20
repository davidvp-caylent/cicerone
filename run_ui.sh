#!/bin/bash

# Script para iniciar la interfaz Streamlit del Beer Tasting Agent

echo "🍺 Iniciando Beer Tasting Cicerone UI..."
echo ""

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Creando desde .env.example..."
    cp .env.example .env
    echo "✓ Archivo .env creado. Por favor, configura tus credenciales de AWS."
    echo ""
fi

# Verificar credenciales de AWS
if [ -z "$AWS_ACCESS_KEY_ID" ] && [ -z "$AWS_PROFILE" ]; then
    echo "⚠️  No se detectaron credenciales de AWS."
    echo ""
    echo "Opciones:"
    echo "1. Configura AWS CLI: aws configure"
    echo "2. Exporta variables: export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=..."
    echo "3. Usa un perfil: export AWS_PROFILE=tu-perfil"
    echo ""
    read -p "¿Continuar de todas formas? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🚀 Iniciando Streamlit..."
echo ""
echo "La interfaz se abrirá en: http://localhost:8501"
echo ""
echo "Para detener: Ctrl+C"
echo ""

streamlit run app_ui.py
