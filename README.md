# 📊 Prometheus AI Dashboard Backend

This backend powers an AI-driven Prometheus dashboard using CrewAI agents to convert natural language prompts into PromQL, generate chart layouts, and offer follow-up suggestions. It supports real-time updates via WebSockets and stores prompt history in SQLite.

---

## ✅ Features

- 🧠 Natural language to PromQL
- 📈 Dynamic layout generation
- 🤖 Multi-agent logic via CrewAI (Intent → PromQL → Layout → Log → Follow-up)
- 🧠 SLM short response fallback
- ⚠️ Threshold alerting
- 🔌 Prometheus integration (local or remote)
- 📡 Live updates with WebSocket (Socket.IO)
- 🕓 Prompt history & anomaly tracking

---

## 📁 Folder Structure

backend/
├── main.py
├── routes/
│ ├── chat.py
│ ├── suggestion.py
│ ├── history.py
├── agents/
│ ├── crew_agents.py
│ └── crew_router.py
├── utils/
│ ├── slm_router.py
│ ├── predict_next.py
│ └── gemini_wrapper.py
├── dbscripts/
│ ├── audit_db.py
│ └── models.py
├── ws/
│ └── socketio_server.py
├── rag/
│ ├── promql_knowledge.txt
│ └── faiss_index/
├── requirements.txt
├── audit_log.db



---

## ⚙️ Setup Steps

### 🔧 1. Clone & Setup

```bash
git clone https://github.com/your-user/prometheus-ai-dashboard.git
cd prometheus-ai-dashboard/backend


python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


pip install -r requirements.txt


GEMINI_API_KEY=your_gemini_api_key_here
PROMETHEUS_URL=http://localhost:9090

uvicorn main:app --reload --port 8080


python ws/socketio_server.py

curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Show CPU usage for server1"}'


# HELP server_cpu_usage_percent CPU usage percentage
# TYPE server_cpu_usage_percent gauge
server_cpu_usage_percent 25.0


🔐 Gemini API (Free Key)
Go to Google AI Studio

Generate an API key

Set it as GEMINI_API_KEY in .env

🧠 CrewAI Agents
Agents involved:

IntentAgent

PromQLAgent

LayoutAgent

LoggerAgent

FollowupAgent
