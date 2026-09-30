# 🤖 AI Research Agent

An AI-powered research assistant built with the **OpenAI Agents SDK**. The project is being developed incrementally to explore agentic AI concepts, tool calling, execution context, state management, observability, and production-oriented architecture.

The project intentionally evolves through multiple versions — starting from a simple agent and gradually introducing more advanced engineering concepts.

> **Current Version: v0.2.0**

---

## 🎯 Project Goal

The goal of this project is not simply to build another AI chatbot.

It is a hands-on learning project focused on understanding how to design and engineer **Agentic AI systems** from the ground up.

The project follows this development philosophy:

```text
Build
  ↓
Encounter a problem
  ↓
Research documentation
  ↓
Understand the underlying concept
  ↓
Use AI as a development assistant
  ↓
Implement
  ↓
Test
  ↓
Iterate
```

The system will gradually evolve from a simple single-agent application into a more complete production-style Agentic AI system.

---

# ✨ Current Features

## v0.1.0 — Basic Agent

The first version established the core Agentic AI architecture.

* OpenAI Agents SDK
* Single research agent
* Agent instructions
* Runner execution
* Custom research tool
* Basic agent-to-tool interaction
* Context passed through the agent execution
* Final research response

Basic architecture:

```text
User
 ↓
Agent
 ↓
Tool
 ↓
Research
 ↓
Agent
 ↓
Final Answer
```

---

# 🚀 v0.2.0 — Interactive Research Application

Version 2 introduced a user interface and transformed the basic agent into an interactive research application.

### Added

* Streamlit interface
* Interactive chat
* Research agent
* Research tool
* Agent context
* `RunContextWrapper`
* OpenAI Agents SDK Runner
* Asynchronous execution
* Persistent chat interaction during the Streamlit session
* Event-loop handling for Streamlit
* LangSmith environment configuration for observability

Architecture:

```text
┌───────────────┐
│   Streamlit   │
│      UI       │
└───────┬───────┘
        │
        ↓
┌───────────────┐
│ Research Agent│
└───────┬───────┘
        │
        ↓
┌───────────────┐
│ Research Tool │
└───────┬───────┘
        │
        ↓
    Research
        │
        ↓
┌───────────────┐
│ Final Answer  │
└───────────────┘
```

---

# 🧠 Technologies

### Core

* Python
* OpenAI Agents SDK
* AsyncIO
* Streamlit

### Agentic AI

* Agents
* Runner
* Tools
* Tool calling
* Agent context
* `RunContextWrapper`
* Structured agent execution

### Observability

* LangSmith

---

# 📂 Project Structure

The project intentionally starts with a small structure rather than creating a large production architecture before it is needed.

```text
ai-research-agent/
│
├── app/
│   ├── main.py
│   ├── agent.py
│   └── tools.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The structure will evolve as the system becomes more complex.

---

# ⚙️ How It Works

The user interacts with the Streamlit application and provides a research request.

The request is passed to the Agent.

The Agent determines when the research tool should be used and provides the required information to the tool.

The tool performs the research and returns the result to the Agent.

The Agent then processes the result and generates the final response for the user.

```text
User Request
     ↓
Streamlit
     ↓
OpenAI Agent
     ↓
Tool Selection
     ↓
Research Tool
     ↓
Research Result
     ↓
Agent Processing
     ↓
Final Response
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_openai_api_key

LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=ai-research-agent
```

> Never commit your `.env` file to GitHub.

Make sure `.env` is included in `.gitignore`.

Example:

```gitignore
.env
__pycache__/
.venv/
```

---

# ▶️ Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-research-agent
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create `.env` and add your API keys.

## 5. Run the application

```bash
streamlit run app/main.py
```

The application will then be available through the local Streamlit server.

---

# 🔭 Roadmap

The project is intentionally being developed in stages.

## v0.1.0 — Foundation ✅

* [x] Basic Agent
* [x] Runner
* [x] Research Tool
* [x] Agent instructions
* [x] Context

---

## v0.2.0 — Interactive Application ✅

* [x] Streamlit UI
* [x] Interactive chat
* [x] Async execution
* [x] Event-loop handling
* [x] Research workflow
* [x] LangSmith configuration

---

## v0.3.0 — State & Persistence 🚧

Planned:

* [ ] Conversation/session state
* [ ] Application state
* [ ] Persistent research jobs
* [ ] Database integration
* [ ] PostgreSQL
* [ ] Research history
* [ ] Better separation of application components

---

## v0.4.0 — Multi-Agent Architecture

Planned:

```text
                Planner
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
   Researcher   Analyst    Specialist
        └──────────┼──────────┘
                   ↓
                 Writer
                   ↓
             Final Report
```

Planned features:

* [ ] Planner Agent
* [ ] Research Agent
* [ ] Analyst Agent
* [ ] Critic Agent
* [ ] Writer Agent
* [ ] Agent handoffs
* [ ] More advanced orchestration

---

## v0.5.0 — Background Processing

Planned:

* [ ] Background research jobs
* [ ] Redis
* [ ] Queue/worker architecture
* [ ] Job status
* [ ] Long-running research
* [ ] Retry handling
* [ ] Failure states

Example:

```text
POST /research
      ↓
Create Job
      ↓
Queue
      ↓
Worker
      ↓
Agent System
      ↓
Research Complete
```

---

## v0.6.0 — Human-in-the-Loop

Planned:

* [ ] Human approval
* [ ] Approval checkpoints
* [ ] Pause/resume execution
* [ ] Sensitive tool approval
* [ ] Resumable agent runs

Example:

```text
Agent
 ↓
Request sensitive action
 ↓
Human Approval
 ↓
Approve / Reject
 ↓
Agent continues
```

---

## v0.7.0 — Reliability & Security

Planned:

* [ ] Authentication
* [ ] Authorization
* [ ] Input validation
* [ ] Output validation
* [ ] Guardrails
* [ ] Rate limiting
* [ ] Timeouts
* [ ] Retries
* [ ] Error handling
* [ ] Permission boundaries
* [ ] Prompt-injection protection

---

## v0.8.0 — Observability & Evaluation

Planned:

* [ ] LangSmith tracing
* [ ] Agent execution tracing
* [ ] Tool-call tracing
* [ ] Token/cost tracking
* [ ] Latency monitoring
* [ ] Evaluation dataset
* [ ] Agent evaluation
* [ ] Regression testing

---

## v0.9.0 — Production Engineering

Planned:

* [ ] Docker
* [ ] Docker Compose
* [ ] Production configuration
* [ ] CI/CD
* [ ] Cloud deployment
* [ ] Monitoring
* [ ] Logging
* [ ] Production database
* [ ] Scalability improvements

---

## v1.0.0 — Production-Ready Milestone

The final goal is a production-style Agentic AI research platform capable of:

* Persistent users
* Persistent research jobs
* Multi-agent orchestration
* Tool execution
* Background processing
* Human approval
* Guardrails
* Evaluation
* Observability
* Authentication
* Production deployment

Target architecture:

```text
                         User
                           │
                           ▼
                    ┌─────────────┐
                    │  Frontend   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    │ Auth / API  │
                    └──────┬──────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Agent Orchestrator│
                  └────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Planner      Researcher      Analyst
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                         Writer
                           │
                           ▼
                 ┌─────────────────┐
                 │ Tools / APIs    │
                 └────────┬────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
         PostgreSQL     Redis      External APIs
```

---

# 🧪 Development Philosophy

This project is intentionally not being built by generating the entire application at once.

Each version introduces new engineering challenges.

The development process is:

1. Start simple.
2. Build the current version.
3. Encounter a real problem.
4. Investigate the problem.
5. Read documentation.
6. Understand the underlying concept.
7. Use AI as a development assistant when useful.
8. Implement the solution.
9. Test it.
10. Refactor when the complexity justifies it.
11. Move to the next version.

AI may be used for:

* Code generation
* Debugging
* Documentation research
* Code explanations
* Architecture discussion
* Refactoring suggestions

However, the goal is to **understand the system rather than blindly copy generated code**.

---

# 📌 Current Development Status

**Current version:** `v0.2.0`

**Status:** 🚧 Active Development

The current version successfully provides an interactive research application using the OpenAI Agents SDK and Streamlit.

The next major milestone is **v0.3.0 — State & Persistence**.

---

# 📚 Learning Objectives

Through this project, the following concepts will progressively be explored:

* Agent architecture
* Tool calling
* Agent context
* Async Python
* FastAPI
* Streamlit
* State management
* Persistence
* PostgreSQL
* Multi-agent systems
* Agent orchestration
* Background jobs
* Queues
* Redis
* Human-in-the-loop
* Guardrails
* Authentication
* Security
* Observability
* Evaluation
* Docker
* Cloud deployment
* System design
* Production Agentic AI architecture

---

# 👨‍💻 Project Philosophy

> **Start simple. Let complexity earn its way into the architecture.**

This project is a practical journey from:

```text
Simple Agent
      ↓
Agent + Tools
      ↓
Interactive Application
      ↓
State
      ↓
Persistence
      ↓
Multi-Agent System
      ↓
Background Processing
      ↓
Human-in-the-Loop
      ↓
Production Engineering
      ↓
Production-Style Agentic AI System
```

The objective is not merely to learn another AI framework.

The objective is to develop the ability to **design, build, debug, and evolve complete Agentic AI systems.**

---

## 📄 License

Add your preferred license here before publishing the project publicly.
