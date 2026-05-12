# FinSight AI - Financial Intelligence Backend

A production-ready FastAPI backend for intelligent financial analysis using TAO/ReAct agents, Retrieval Augmented Generation (RAG), and multi-agent orchestration with memory management.

## Tech Stack

- **Python 3.11+** with fully async codebase
- **FastAPI** -- high-performance ASGI framework
- **LangChain** -- LLM orchestration and agent framework
- **Beanie** -- async MongoDB ODM built on Motor
- **FAISS** -- vector store for semantic search and RAG
- **Pydantic v2** -- data validation and settings management
- **structlog** -- structured JSON logging with correlation IDs
- **Docker** -- multi-stage builds with Gunicorn + Uvicorn workers

## Project Structure

```
app/
├── main.py                  # Application entry point
├── server.py                # Server setup and configuration
├── core/                    # Core configuration
│   ├── config.py            # Pydantic settings (env-driven)
│   ├── logging.py           # Structured logging setup
│   └── events.py            # Lifespan events (startup/shutdown)
├── api/v1/                  # Versioned API layer
│   ├── api.py               # Router aggregation
│   └── endpoints/
│       ├── chat.py          # Chat endpoint (TAO/ReAct interface)
│       └── rag.py           # RAG query endpoint
├── ai/                      # AI agents and intelligence
│   ├── agents/
│   │   ├── orchestrator_agent.py    # TAO/ReAct orchestrator (Thought→Action→Observation)
│   │   ├── planner_agent.py         # Query planning and decomposition
│   │   ├── executor_agent.py        # Tool execution with ReAct loop
│   │   └── verification_agent.py    # Output validation and hallucination detection
│   ├── memory/
│   │   ├── memory_manager.py        # Conversation memory orchestration
│   │   ├── summary_memory.py        # Semantic summarization
│   │   └── vector_memory.py         # Embedding-based memory retrieval
│   ├── prompts/
│   │   ├── react_prompt.py          # ReAct (Reason-Act-Observe) template
│   │   ├── planner_prompt.py        # Query planning template
│   │   ├── agent_prompt.py          # Agent system prompt
│   │   └── system.py                # System prompt definitions
│   ├── rag/
│   │   ├── ingest.py                # Document ingestion pipeline
│   │   ├── pipeline.py              # RAG processing pipeline
│   │   ├── retriever.py             # Semantic document retrieval
│   │   └── vectorstore.py           # FAISS vector store integration
│   └── tools/
│       ├── tool_registry.py         # Central tool registry
│       ├── tool_executor.py         # Safe tool execution with validation
│       ├── tool_ranker.py           # LLM-based tool relevance scoring
│       ├── base.py                  # Base tool interface
│       ├── calculator.py            # Mathematical calculations
│       ├── financial_metrics.py     # Financial analysis tools
│       ├── document_search.py       # Document search via RAG
│       └── rag_tool.py              # RAG integration tool
├── services/
│   └── chat_service.py              # Chat business logic
├── db/
│   ├── mongo.py                     # MongoDB connection
│   └── init_db.py                   # Database initialization
├── models/                          # Beanie document models
├── schemas/                         # Pydantic request/response DTOs
│   ├── chat.py
│   ├── rag.py
│   ├── planner_schema.py
│   ├── tool_schema.py
│   └── AgentDecision.py
├── exceptions/                      # Custom exception hierarchy
├── middleware/
│   ├── correlation_id.py            # Request correlation tracking
│   └── logging.py                   # Request/response logging
└── utils/
    ├── retry.py                     # Retry logic with correction
    └── parsing/
        ├── output_parser.py         # Agent output parsing
        └── planner_parser.py        # Planner output parsing
tests/                              # pytest async test suite
rag_files/                          # Documents for RAG ingestion
vectorstore/                        # FAISS vector store indices
```

## Quick Start

### 1. Setup Environment

```bash
cp .env.example .env
# Edit .env with your LLM API key and settings
```

### 2. Install Dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -e ".[dev]"
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` with docs at `/docs`.

### 4. Local Development

```bash
uvicorn app.main:app --reload
```

### 5. Run Tests

```bash
pytest -v
```

## Usage

### Chat with TAO/ReAct Agent

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current revenue trend?",
    "user_id": "user123"
  }'
```

**Response:**
```json
{
  "plan": {
    "steps": [
      {"action": "document_search", "input": {"query": "revenue"}},
      {"action": "financial_metrics", "input": {"metric": "trend"}}
    ]
  },
  "execution": "Revenue increased 15% YoY..."
}
```

### Query via RAG

```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find quarterly earnings reports",
    "top_k": 5
  }'
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Liveness probe |
| POST | `/api/v1/chat` | Chat endpoint with TAO/ReAct agent |
| POST | `/api/v1/chat/stream` | Streaming chat responses |
| POST | `/api/v1/rag/query` | Query documents via RAG |
| POST | `/api/v1/rag/ingest` | Ingest documents for RAG |

## Agent Architecture

### TAO Loop (Thought → Action → Observation)

The application implements the **TAO/ReAct pattern** for intelligent financial reasoning:

1. **Thought** - Agent analyzes the query and reasoning context
2. **Action** - Agent selects and executes appropriate tools
3. **Observation** - Agent observes results and determines if more steps needed

### Multi-Agent System

- **Orchestrator Agent** - Coordinates the overall flow
- **Planner Agent** - Breaks queries into logical tool call sequences
- **Executor Agent** - Executes the plan with ReAct loop and tool ranking
- **Verification Agent** - Validates outputs for hallucinations and confidence

### Tool System

Tools are ranked by relevance using LLM scoring:
- **Financial Metrics** - Calculate key financial indicators
- **Calculator** - Perform mathematical operations
- **Document Search** - Retrieve relevant documents via RAG
- **RAG Tool** - Semantic search over ingested documents

### Memory Management

- **Memory Manager** - Orchestrates conversation history
- **Vector Memory** - Stores embeddings for semantic recall
- **Summary Memory** - Maintains semantic summaries of long conversations

## Configuration

All settings are driven by environment variables (12-factor). Key settings:

| Variable | Description |
|----------|-------------|
| `MONGODB_URL` | MongoDB connection string |
| `LLM_MODEL` | LLM model to use (e.g., `gpt-4`, `claude-3-opus`) |
| `LLM_API_KEY` | API key for LLM provider |
| `EMBEDDING_MODEL` | Embedding model for RAG (e.g., `text-embedding-3-small`) |
| `LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `VECTORSTORE_PATH` | Path to FAISS vector store directory |
| `RAG_CHUNK_SIZE` | Document chunk size for RAG (default: 500) |
| `MAX_MEMORY_STEPS` | Maximum conversation steps to store (default: 10) |
| `MAX_TOOL_RETRIES` | Max retry attempts per tool (default: 2) |

## Code Quality

```bash
ruff check .          # Lint
ruff format .         # Format
mypy app/             # Type checking
```

## Production Deployment

The included `Dockerfile` uses multi-stage builds and runs as a non-root user. `gunicorn.conf.py` configures Uvicorn workers with sensible defaults:

```bash
docker compose -f docker-compose.yml up -d
```

### Environment Setup for Production

Ensure these variables are set:
- `MONGODB_URL` - Production MongoDB connection
- `LLM_API_KEY` - LLM provider API key
- `VECTORSTORE_PATH` - Path to FAISS indices
- `LOG_LEVEL` - Set to `INFO` or `WARNING`
