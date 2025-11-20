# Beer Tasting Agent 🍺

Un agente conversacional construido con Strands Agents que asiste a usuarios durante catas de cerveza.

## Descripción

El Beer Tasting Agent es un cicerone virtual que:
- Guía a los usuarios a través del proceso de cata de cerveza
- Predice qué cerveza será su favorita basándose en sus preferencias
- Proporciona información educativa sobre estilos de cerveza
- Sugiere maridajes de comida
- Obtiene información actualizada del catálogo de Cerveza Fortuna

## Estructura del Proyecto

```
.
├── tools/              # Herramientas del agente (scraping, análisis, recomendaciones)
├── tests/              # Tests unitarios y property-based tests
├── config/             # Configuración y settings
├── requirements.txt    # Dependencias de Python
├── pytest.ini          # Configuración de pytest
├── conftest.py         # Fixtures compartidos para tests
├── .env.example        # Ejemplo de variables de entorno
└── README.md           # Este archivo
```

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales de AWS
   ```

## Testing

El proyecto utiliza pytest y Hypothesis para testing:

```bash
# Ejecutar todos los tests
pytest

# Ejecutar solo tests unitarios
pytest -m unit

# Ejecutar solo property-based tests
pytest -m property

# Ejecutar con verbose output
pytest -v
```

## Tecnologías

- **Framework**: Strands Agents
- **LLM**: Amazon Bedrock (Claude Sonnet 4.5)
- **Runtime**: Amazon Bedrock AgentCore
- **Web Scraping**: requests + BeautifulSoup4
- **Testing**: pytest + Hypothesis
- **UI**: Streamlit

## Deployment

El agente está diseñado para desplegarse en Amazon Bedrock AgentCore Runtime. Ver `DEPLOYMENT.md` para instrucciones detalladas.

### Quick Start

```bash
# Instalar toolkit de deployment
pip install bedrock-agentcore-starter-toolkit

# Configurar el agente
agentcore configure --entrypoint app.py

# Desplegar a AWS
agentcore launch

# Probar el agente
agentcore invoke '{"prompt": "Hola, quiero hacer una cata de cerveza"}'
```

### Estructura de Deployment

```
.
├── app.py              # Integración con AgentCore Runtime
├── agent.py            # Configuración del agente Strands
├── session_manager.py  # Gestión de sesiones
├── tools/              # Herramientas del agente
├── models/             # Modelos de datos
├── DEPLOYMENT.md       # Guía completa de deployment
└── requirements.txt    # Dependencias
```

## Desarrollo

Este proyecto sigue la metodología de desarrollo basado en especificaciones. Ver los documentos en `.kiro/specs/beer-tasting-agent/` para:
- `requirements.md`: Requisitos del sistema
- `design.md`: Diseño detallado con propiedades de corrección
- `tasks.md`: Plan de implementación

## Licencia

[Especificar licencia]
