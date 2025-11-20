# Requirements Document

## Introduction

El Beer Tasting Agent es un agente conversacional desarrollado con Strands Agents que asiste a usuarios durante catas de cerveza. El agente ayuda a los participantes a comprender las características de las cervezas que van a probar, predice cuál será su favorita basándose en sus preferencias, y proporciona información educativa sobre cada cerveza. El sistema obtiene información de las cervezas desde el catálogo de Cerveza Fortuna (https://cervezafortuna.com/inicio/cervezas/) y se despliega en Amazon Bedrock AgentCore para facilitar su consumo a través de una interfaz web sencilla.

## Glossary

- **Beer Tasting Agent**: El sistema de agente conversacional que asiste en catas de cerveza
- **User**: Persona que participa en la cata de cerveza y interactúa con el agente
- **Beer Catalog**: Colección de cervezas disponibles obtenida desde Cerveza Fortuna
- **Tasting Session**: Una sesión interactiva donde el usuario prueba y evalúa cervezas
- **Preference Profile**: Conjunto de preferencias del usuario basadas en sus respuestas durante la cata
- **AgentCore**: Plataforma de Amazon Bedrock para desplegar y ejecutar agentes
- **Strands Agent**: Framework utilizado para construir el agente conversacional
- **Web Interface**: Interfaz de usuario web para interactuar con el agente

## Requirements

### Requirement 1

**User Story:** Como usuario de una cata de cerveza, quiero obtener información sobre las cervezas que voy a probar, para entender mejor sus características antes de degustarlas.

#### Acceptance Criteria

1. WHEN a user requests information about a specific beer, THEN the Beer Tasting Agent SHALL retrieve and display the beer's name, style, ABV, IBU, and description from the Beer Catalog
2. WHEN the Beer Catalog is queried, THEN the Beer Tasting Agent SHALL fetch current data from the Cerveza Fortuna website
3. WHEN a user asks about available beers, THEN the Beer Tasting Agent SHALL list all beers from the Beer Catalog with their basic information
4. WHEN beer information is unavailable, THEN the Beer Tasting Agent SHALL inform the user and suggest alternative actions

### Requirement 2

**User Story:** Como usuario, quiero que el agente me guíe a través del proceso de cata, para aprender a evaluar correctamente cada cerveza.

#### Acceptance Criteria

1. WHEN a user starts a Tasting Session, THEN the Beer Tasting Agent SHALL explain the four steps of beer tasting: appearance, aroma, taste, and mouthfeel
2. WHEN a user is evaluating a beer, THEN the Beer Tasting Agent SHALL ask guided questions about each tasting step
3. WHEN a user provides feedback on a beer characteristic, THEN the Beer Tasting Agent SHALL record the response in the Preference Profile
4. WHEN a user completes evaluation of one beer, THEN the Beer Tasting Agent SHALL suggest the next beer to taste based on progression from lighter to more intense styles

### Requirement 3

**User Story:** Como usuario, quiero que el agente prediga cuál será mi cerveza favorita, para descubrir qué cerveza se ajusta mejor a mis gustos.

#### Acceptance Criteria

1. WHEN a user has evaluated at least two beers, THEN the Beer Tasting Agent SHALL analyze the Preference Profile to identify patterns
2. WHEN the Beer Tasting Agent makes a prediction, THEN the Beer Tasting Agent SHALL explain the reasoning based on the user's stated preferences
3. WHEN a user completes the tasting of all beers, THEN the Beer Tasting Agent SHALL rank the beers from most to least likely to be the user's favorite
4. WHEN the prediction is made, THEN the Beer Tasting Agent SHALL highlight specific characteristics that match the user's preferences

### Requirement 4

**User Story:** Como usuario, quiero aprender sobre estilos de cerveza y términos técnicos, para enriquecer mi experiencia de cata.

#### Acceptance Criteria

1. WHEN a user asks about a beer style, THEN the Beer Tasting Agent SHALL provide a clear explanation of that style's characteristics
2. WHEN a technical term is mentioned, THEN the Beer Tasting Agent SHALL offer to explain the term in simple language
3. WHEN a user requests educational content, THEN the Beer Tasting Agent SHALL provide information about brewing processes, ingredients, or beer history
4. WHEN explaining concepts, THEN the Beer Tasting Agent SHALL use language appropriate for beer enthusiasts of varying experience levels

### Requirement 5

**User Story:** Como usuario, quiero recibir recomendaciones de maridaje, para saber qué alimentos combinan bien con cada cerveza.

#### Acceptance Criteria

1. WHEN a user asks about food pairing for a specific beer, THEN the Beer Tasting Agent SHALL suggest at least three appropriate food options based on the beer's style and characteristics
2. WHEN providing pairing suggestions, THEN the Beer Tasting Agent SHALL explain why the pairing works
3. WHEN a user mentions a food preference, THEN the Beer Tasting Agent SHALL recommend beers from the Beer Catalog that pair well with that food

### Requirement 6

**User Story:** Como usuario, quiero interactuar con el agente a través de una interfaz web simple, para acceder fácilmente al asistente de cata.

#### Acceptance Criteria

1. WHEN a user accesses the Web Interface, THEN the Beer Tasting Agent SHALL be available for conversation through a chat interface
2. WHEN a user sends a message, THEN the Beer Tasting Agent SHALL respond within 5 seconds under normal conditions
3. WHEN the Tasting Session is active, THEN the Web Interface SHALL display the conversation history
4. WHEN a user starts a new session, THEN the Web Interface SHALL clear previous conversation history and initialize a new Tasting Session

### Requirement 7

**User Story:** Como desarrollador, quiero desplegar el agente en AgentCore, para aprovechar la infraestructura serverless y escalabilidad de AWS.

#### Acceptance Criteria

1. WHEN the Beer Tasting Agent is deployed, THEN the system SHALL run on Amazon Bedrock AgentCore
2. WHEN the agent is invoked, THEN the system SHALL use Strands Agents framework for conversation management
3. WHEN the deployment is complete, THEN the system SHALL expose an API endpoint that the Web Interface can consume
4. WHEN the agent processes requests, THEN the system SHALL handle multiple concurrent users without performance degradation

### Requirement 8

**User Story:** Como usuario, quiero que el agente recuerde mis preferencias durante la sesión, para recibir recomendaciones más precisas.

#### Acceptance Criteria

1. WHEN a user expresses a preference, THEN the Beer Tasting Agent SHALL store it in the Preference Profile for the current Tasting Session
2. WHEN making recommendations, THEN the Beer Tasting Agent SHALL reference previously stated preferences
3. WHEN a Tasting Session ends, THEN the Beer Tasting Agent SHALL offer to save the Preference Profile for future sessions
4. WHILE a Tasting Session is active, THEN the Beer Tasting Agent SHALL maintain consistency in understanding user preferences

### Requirement 9

**User Story:** Como usuario, quiero que el agente maneje errores de manera elegante, para tener una experiencia fluida incluso cuando ocurran problemas técnicos.

#### Acceptance Criteria

1. WHEN the Cerveza Fortuna website is unavailable, THEN the Beer Tasting Agent SHALL inform the user and continue with cached data if available
2. WHEN an invalid user input is received, THEN the Beer Tasting Agent SHALL ask for clarification without terminating the conversation
3. WHEN an unexpected error occurs, THEN the Beer Tasting Agent SHALL log the error and provide a helpful message to the user
4. WHEN the system recovers from an error, THEN the Beer Tasting Agent SHALL resume the Tasting Session from the last valid state
