#!/bin/bash

# Script para renovar credenciales temporales de AWS (SSO, AssumeRole, etc.)

set -e

echo "🔐 Renovando credenciales de AWS..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detectar si usa SSO
if aws configure list | grep -q "sso"; then
    echo "Detectado AWS SSO"
    
    # Obtener el profile
    PROFILE=$(aws configure list | grep profile | awk '{print $2}')
    
    if [ -z "$PROFILE" ]; then
        PROFILE="default"
    fi
    
    echo "Profile: $PROFILE"
    echo ""
    
    # Login con SSO
    echo "Iniciando sesión con AWS SSO..."
    aws sso login --profile $PROFILE
    
    echo ""
    echo "✅ Login exitoso"
    echo ""
    
    # Obtener credenciales
    echo "Obteniendo credenciales temporales..."
    
    # Verificar si jq está instalado
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}⚠️  jq no está instalado. Instalando...${NC}"
        
        # Detectar OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install jq
            else
                echo -e "${RED}❌ Homebrew no está instalado. Instala jq manualmente:${NC}"
                echo "  brew install jq"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            sudo apt-get update && sudo apt-get install -y jq
        else
            echo -e "${RED}❌ No se pudo instalar jq automáticamente${NC}"
            echo "Instálalo manualmente y vuelve a correr este script"
            exit 1
        fi
    fi
    
    # Exportar credenciales
    CREDS=$(aws configure export-credentials --profile $PROFILE --format json)
    
    ACCESS_KEY=$(echo $CREDS | jq -r '.AccessKeyId')
    SECRET_KEY=$(echo $CREDS | jq -r '.SecretAccessKey')
    SESSION_TOKEN=$(echo $CREDS | jq -r '.SessionToken')
    
else
    # No usa SSO, obtener credenciales del profile default
    echo "Obteniendo credenciales del profile default..."
    
    ACCESS_KEY=$(aws configure get aws_access_key_id)
    SECRET_KEY=$(aws configure get aws_secret_access_key)
    SESSION_TOKEN=$(aws configure get aws_session_token)
    
    if [ -z "$SESSION_TOKEN" ]; then
        echo -e "${YELLOW}⚠️  No se encontró session token${NC}"
        echo "Si usas credenciales permanentes, no necesitas este script"
        echo ""
        read -p "¿Continuar de todas formas? (y/n) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
fi

# Verificar que tenemos las credenciales
if [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ]; then
    echo -e "${RED}❌ No se pudieron obtener las credenciales${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Credenciales obtenidas"
echo ""

# Crear directorio .streamlit si no existe
mkdir -p .streamlit

# Actualizar secrets.toml
echo "Actualizando .streamlit/secrets.toml..."

cat > .streamlit/secrets.toml <<EOF
# Streamlit Secrets - Auto-generado por refresh_credentials.sh
# Última actualización: $(date)

[aws]
region = "us-east-1"
access_key_id = "$ACCESS_KEY"
secret_access_key = "$SECRET_KEY"
EOF

# Agregar session token solo si existe
if [ -n "$SESSION_TOKEN" ]; then
    echo "session_token = \"$SESSION_TOKEN\"" >> .streamlit/secrets.toml
fi

cat >> .streamlit/secrets.toml <<EOF

[agentcore]
agent_arn = "arn:aws:bedrock-agentcore:us-east-1:131578276461:runtime/cicerone-szUAIIHGxh"
EOF

echo -e "${GREEN}✓${NC} Archivo .streamlit/secrets.toml actualizado"
echo ""

# Verificar que las credenciales funcionan
echo "Verificando credenciales..."
if aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Credenciales válidas"
    
    # Mostrar información de la cuenta
    ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
    USER=$(aws sts get-caller-identity --query Arn --output text)
    
    echo ""
    echo "Información de la cuenta:"
    echo "  Account: $ACCOUNT"
    echo "  User: $USER"
else
    echo -e "${RED}❌ Las credenciales no son válidas${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ ¡Credenciales renovadas exitosamente!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Ahora puedes correr la aplicación:"
echo "  streamlit run chat.py"
echo ""

# Mostrar cuándo expiran (si es posible)
if [ -n "$SESSION_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  Nota: Las credenciales temporales expiran después de algunas horas${NC}"
    echo "Vuelve a correr este script cuando expiren:"
    echo "  ./refresh_credentials.sh"
    echo ""
fi
