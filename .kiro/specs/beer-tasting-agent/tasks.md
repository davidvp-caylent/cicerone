# Implementation Plan

- [x] 1. Configurar estructura del proyecto y dependencias
  - Crear estructura de directorios (tools/, tests/, config/)
  - Configurar requirements.txt con todas las dependencias
  - Crear archivo .env.example para variables de entorno
  - Configurar pytest y Hypothesis para testing
  - _Requirements: 7.1, 7.2_

- [x] 2. Implementar Beer Catalog Scraper
  - Crear módulo tools/beer_scraper.py
  - Implementar función para hacer request a cervezafortuna.com
  - Implementar parser de HTML con BeautifulSoup4
  - Implementar sistema de cache local con TTL de 24 horas
  - Implementar manejo de errores y fallback a cache
  - _Requirements: 1.2, 9.1_

- [ ]* 2.1 Escribir property test para scraper
  - **Property 2: Catalog listing completeness**
  - **Validates: Requirements 1.3**

- [x] 3. Implementar modelos de datos
  - Crear dataclasses para Beer, BeerDetails, PreferenceProfile
  - Crear dataclasses para TastingSession, BeerEvaluation, Message
  - Implementar validación de datos en constructores
  - _Requirements: 1.1, 2.3, 8.1_

- [ ]* 3.1 Escribir property test para modelos
  - **Property 1: Beer information completeness**
  - **Validates: Requirements 1.1**

- [x] 4. Implementar herramientas del agente
  - Crear tools/catalog_tools.py con get_beer_catalog y get_beer_details
  - Crear tools/preference_tools.py con analyze_preferences
  - Crear tools/recommendation_tools.py con predict_favorite y suggest_tasting_order
  - Crear tools/pairing_tools.py con get_food_pairing
  - Decorar todas las funciones con @tool de Strands
  - _Requirements: 1.1, 1.3, 3.1, 3.3, 5.1_

- [ ]* 4.1 Escribir property test para preference recording
  - **Property 3: Preference recording**
  - **Validates: Requirements 2.3, 8.1**

- [ ]* 4.2 Escribir property test para tasting progression
  - **Property 4: Tasting progression ordering**
  - **Validates: Requirements 2.4**
ho
- [ ]* 4.3 Escribir property test para ranking completo
  - **Property 7: Complete beer ranking**
  - **Validates: Requirements 3.3**

- [ ]* 4.4 Escribir property test para food pairing
  - **Property 9: Food pairing minimum suggestions**
  - **Validates: Requirements 5.1**

- [x] 5. Implementar lógica de análisis de preferencias
  - Implementar algoritmo de extracción de características de feedback
  - Implementar construcción de PreferenceProfile
  - Implementar detección de patrones en preferencias
  - _Requirements: 3.1, 3.2, 8.4_

- [ ]* 5.1 Escribir property test para análisis de preferencias
  - **Property 5: Preference analysis trigger**
  - **Validates: Requirements 3.1**

- [ ]* 5.2 Escribir property test para consistencia de preferencias
  - **Property 13: Preference consistency**
  - **Validates: Requirements 8.4**

- [x] 6. Implementar algoritmo de predicción y ranking
  - Implementar función de scoring de compatibilidad
  - Implementar ponderación por características del perfil
  - Implementar generación de explicaciones basadas en preferencias
  - _Requirements: 3.2, 3.3, 3.4_

- [ ]* 6.1 Escribir property test para predicción
  - **Property 6: Prediction reasoning**
  - **Validates: Requirements 3.2, 3.4**

- [ ]* 6.2 Escribir property test para alineación de recomendaciones
  - **Property 14: Recommendation preference alignment**
  - **Validates: Requirements 8.2**

- [x] 7. Implementar base de conocimiento de maridajes
  - Crear diccionario de reglas de maridaje por estilo de cerveza
  - Implementar función de búsqueda de maridajes
  - Implementar generación de explicaciones de maridaje
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 7.1 Escribir property test para explicaciones de maridaje
  - **Property 10: Pairing explanation inclusion**
  - **Validates: Requirements 5.2**

- [ ]* 7.2 Escribir property test para reverse pairing
  - **Property 11: Reverse pairing validity**
  - **Validates: Requirements 5.3**

- [x] 8. Implementar gestión de sesiones
  - Crear módulo session_manager.py
  - Implementar funciones get_session_state y save_session_state
  - Implementar almacenamiento en memoria (dict) para sesiones
  - Implementar limpieza de sesiones antiguas
  - _Requirements: 6.4, 8.1, 8.3_

- [ ]* 8.1 Escribir property test para recuperación de estado
  - **Property 17: State recovery after error**
  - **Validates: Requirements 9.4**

- [x] 9. Configurar y crear el agente Strands
  - Crear archivo agent.py con configuración del agente
  - Definir instructions del agente como cicerone experto
  - Registrar todas las herramientas en el agente
  - Configurar modelo Claude Sonnet 4.5
  - _Requirements: 2.1, 2.2, 4.1, 4.3, 7.2_

- [ ]* 9.1 Escribir property test para respuestas educativas
  - **Property 8: Educational response provision**
  - **Validates: Requirements 4.1, 4.3**

- [ ] 10. Implementar manejo de errores
  - Implementar ErrorResponse dataclass
  - Implementar manejo de errores de scraping
  - Implementar manejo de errores de validación
  - Implementar manejo de errores de input del usuario
  - Implementar logging con niveles apropiados
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ]* 10.1 Escribir property test para manejo de input inválido
  - **Property 15: Invalid input handling**
  - **Validates: Requirements 9.2**

- [ ]* 10.2 Escribir property test para error logging
  - **Property 16: Error logging and messaging**
  - **Validates: Requirements 9.3**

- [x] 11. Integrar con AgentCore Runtime
  - Crear archivo app.py con BedrockAgentCoreApp
  - Implementar entrypoint handler
  - Integrar gestión de sesiones con el handler
  - Configurar variables de entorno para AWS
  - _Requirements: 7.1, 7.3_

- [ ] 12. Checkpoint - Verificar que el agente funciona localmente
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Crear interfaz Streamlit
  - Crear archivo app_ui.py con interfaz de chat
  - Implementar st.chat_message para mostrar mensajes
  - Implementar st.chat_input para entrada del usuario
  - Implementar gestión de session_state para historial
  - Implementar botón de nueva sesión en sidebar
  - Implementar llamada al endpoint de AgentCore
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ]* 13.1 Escribir property test para tiempo de respuesta
  - **Property 12: Response time constraint**
  - **Validates: Requirements 6.2**

- [ ] 14. Crear archivos de configuración y deployment
  - Crear requirements.txt completo
  - Crear Dockerfile para la aplicación del agente
  - Crear Dockerfile para la interfaz Streamlit
  - Crear script de deployment para AgentCore
  - Documentar proceso de deployment en README.md
  - _Requirements: 7.1, 7.3_

- [ ] 15. Checkpoint final - Verificar integración completa
  - Ensure all tests pass, ask the user if questions arise.
