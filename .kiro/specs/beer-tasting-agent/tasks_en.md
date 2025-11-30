# Implementation Plan

- [x] 1. Configure project structure and dependencies
  - Create directory structure (tools/, tests/, config/)
  - Configure requirements.txt with all dependencies
  - Create .env.example file for environment variables
  - Configure pytest and Hypothesis for testing
  - _Requirements: 7.1, 7.2_

- [x] 2. Implement Beer Catalog Scraper
  - Create tools/beer_scraper.py module
  - Implement function to request cervezafortuna.com
  - Implement HTML parser with BeautifulSoup4
  - Implement local cache system with 24-hour TTL
  - Implement error handling and fallback to cache
  - _Requirements: 1.2, 9.1_

- [ ]* 2.1 Write property test for scraper
  - **Property 2: Catalog listing completeness**
  - **Validates: Requirements 1.3**

- [x] 3. Implement data models
  - Create dataclasses for Beer, BeerDetails, PreferenceProfile
  - Create dataclasses for TastingSession, BeerEvaluation, Message
  - Implement data validation in constructors
  - _Requirements: 1.1, 2.3, 8.1_

- [ ]* 3.1 Write property test for models
  - **Property 1: Beer information completeness**
  - **Validates: Requirements 1.1**

- [x] 4. Implement agent tools
  - Create tools/catalog_tools.py with get_beer_catalog and get_beer_details
  - Create tools/preference_tools.py with analyze_preferences
  - Create tools/recommendation_tools.py with predict_favorite and suggest_tasting_order
  - Create tools/pairing_tools.py with get_food_pairing
  - Decorate all functions with @tool from Strands
  - _Requirements: 1.1, 1.3, 3.1, 3.3, 5.1_

- [ ]* 4.1 Write property test for preference recording
  - **Property 3: Preference recording**
  - **Validates: Requirements 2.3, 8.1**

- [ ]* 4.2 Write property test for tasting progression
  - **Property 4: Tasting progression ordering**
  - **Validates: Requirements 2.4**

- [ ]* 4.3 Write property test for complete ranking
  - **Property 7: Complete beer ranking**
  - **Validates: Requirements 3.3**

- [ ]* 4.4 Write property test for food pairing
  - **Property 9: Food pairing minimum suggestions**
  - **Validates: Requirements 5.1**

- [x] 5. Implement preference analysis logic
  - Implement algorithm to extract characteristics from feedback
  - Implement PreferenceProfile construction
  - Implement pattern detection in preferences
  - _Requirements: 3.1, 3.2, 8.4_

- [ ]* 5.1 Write property test for preference analysis
  - **Property 5: Preference analysis trigger**
  - **Validates: Requirements 3.1**

- [ ]* 5.2 Write property test for preference consistency
  - **Property 13: Preference consistency**
  - **Validates: Requirements 8.4**

- [x] 6. Implement prediction and ranking algorithm
  - Implement compatibility scoring function
  - Implement weighting by profile characteristics
  - Implement generation of explanations based on preferences
  - _Requirements: 3.2, 3.3, 3.4_

- [ ]* 6.1 Write property test for prediction
  - **Property 6: Prediction reasoning**
  - **Validates: Requirements 3.2, 3.4**

- [ ]* 6.2 Write property test for recommendation alignment
  - **Property 14: Recommendation preference alignment**
  - **Validates: Requirements 8.2**

- [x] 7. Implement food pairing knowledge base
  - Create dictionary of pairing rules by beer style
  - Implement pairing search function
  - Implement generation of pairing explanations
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 7.1 Write property test for pairing explanations
  - **Property 10: Pairing explanation inclusion**
  - **Validates: Requirements 5.2**

- [ ]* 7.2 Write property test for reverse pairing
  - **Property 11: Reverse pairing validity**
  - **Validates: Requirements 5.3**

- [x] 8. Implement session management
  - Create session_manager.py module
  - Implement get_session_state and save_session_state functions
  - Implement in-memory storage (dict) for sessions
  - Implement cleanup of old sessions
  - _Requirements: 6.4, 8.1, 8.3_

- [ ]* 8.1 Write property test for state recovery
  - **Property 17: State recovery after error**
  - **Validates: Requirements 9.4**

- [x] 9. Configure and create Strands agent
  - Create agent.py file with agent configuration
  - Define agent instructions as expert cicerone
  - Register all tools in the agent
  - Configure Claude Sonnet 4.5 model
  - _Requirements: 2.1, 2.2, 4.1, 4.3, 7.2_

- [ ]* 9.1 Write property test for educational responses
  - **Property 8: Educational response provision**
  - **Validates: Requirements 4.1, 4.3**

- [ ] 10. Implement error handling
  - Implement ErrorResponse dataclass
  - Implement scraping error handling
  - Implement validation error handling
  - Implement user input error handling
  - Implement logging with appropriate levels
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ]* 10.1 Write property test for invalid input handling
  - **Property 15: Invalid input handling**
  - **Validates: Requirements 9.2**

- [ ]* 10.2 Write property test for error logging
  - **Property 16: Error logging and messaging**
  - **Validates: Requirements 9.3**

- [x] 11. Integrate with AgentCore Runtime
  - Create app.py file with BedrockAgentCoreApp
  - Implement entrypoint handler
  - Integrate session management with handler
  - Configure environment variables for AWS
  - _Requirements: 7.1, 7.3_

- [ ] 12. Checkpoint - Verify agent works locally
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Create Streamlit interface
  - Create app_ui.py file with chat interface
  - Implement st.chat_message to display messages
  - Implement st.chat_input for user input
  - Implement session_state management for history
  - Implement new session button in sidebar
  - Implement call to AgentCore endpoint
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ]* 13.1 Write property test for response time
  - **Property 12: Response time constraint**
  - **Validates: Requirements 6.2**

- [ ] 14. Create configuration and deployment files
  - Create complete requirements.txt
  - Create Dockerfile for agent application
  - Create Dockerfile for Streamlit interface
  - Create deployment script for AgentCore
  - Document deployment process in README.md
  - _Requirements: 7.1, 7.3_

- [ ] 15. Final checkpoint - Verify complete integration
  - Ensure all tests pass, ask the user if questions arise.
