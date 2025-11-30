# Beer Tasting Agent 🍺

A conversational agent built with Strands Agents that assists users during beer tastings.

## Description

The Beer Tasting Agent is a virtual cicerone that:
- Guides users through the beer tasting process
- Predicts which beer will be their favorite based on their preferences
- Provides educational information about beer styles
- Suggests food pairings
- Retrieves up-to-date information from the Cerveza Fortuna catalog

## Project Structure

```
.
├── tools/              # Agent tools (scraping, analysis, recommendations)
├── tests/              # Unit tests and property-based tests
├── config/             # Configuration and settings
├── requirements.txt    # Python dependencies
├── pytest.ini          # Pytest configuration
├── conftest.py         # Shared test fixtures
├── .env.example        # Environment variables example
└── README.md           # This file
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

## Testing

The project uses pytest and Hypothesis for testing:

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run only property-based tests
pytest -m property

# Run with verbose output
pytest -v
```

## Technologies

- **Framework**: Strands Agents
- **LLM**: Amazon Bedrock (Claude Sonnet 4.5)
- **Runtime**: Amazon Bedrock AgentCore
- **Web Scraping**: requests + BeautifulSoup4
- **Testing**: pytest + Hypothesis
- **UI**: Streamlit

## Deployment

The agent is designed to be deployed on Amazon Bedrock AgentCore Runtime. See `DEPLOYMENT.md` for detailed instructions.

### Quick Start

```bash
# Install deployment toolkit
pip install bedrock-agentcore-starter-toolkit

# Configure the agent
agentcore configure --entrypoint app.py

# Deploy to AWS
agentcore launch

# Test the agent
agentcore invoke '{"prompt": "Hello, I want to do a beer tasting"}'
```

### Deployment Structure

```
.
├── app.py              # AgentCore Runtime integration
├── agent.py            # Strands agent configuration
├── session_manager.py  # Session management
├── tools/              # Agent tools
├── models/             # Data models
├── DEPLOYMENT.md       # Complete deployment guide
└── requirements.txt    # Dependencies
```

## Development

This project follows a specification-based development methodology. See the documents in `.kiro/specs/beer-tasting-agent/` for:
- `requirements.md`: System requirements
- `design.md`: Detailed design with correctness properties
- `tasks.md`: Implementation plan

## License

[Specify license]
