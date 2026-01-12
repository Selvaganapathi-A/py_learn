Callback Demo, WebHook Demo with React + FastAPI + python[httpx]
---
Excellent — you're asking for a **full-stack demonstration** of a **callback or webhook flow**, involving:

### 🎯 Stack Components

* **Webhook Sender**: Sends event to your FastAPI server (`httpx`)
* **FastAPI Server**: Receives webhook, processes it, and notifies frontend
* **React Frontend**: Displays real-time updates from webhook (polling, or socket-based)
* ✅ Optional: Persist webhook data to DB, or use message queues (future-proofing)

---

## ✅ Let's Define a Simple Demo

### 🎬 Scenario:

> Your **React frontend** subscribes to a “task created” event.
> An external service (**simulated using FastAPI + `httpx`**) sends a **webhook** to your FastAPI server.
> FastAPI stores the event, and the frontend pulls or listens for updates.

---

## ⚙️ Project Layout

```
webhook-demo/
├── backend/
│   ├── main.py        # FastAPI receiver
│   ├── callback.py    # Simulated webhook sender using httpx
│   └── data.json      # Optional local store
├── frontend/
│   └── React app      # Displays webhook events
```

---

## 🧩 Part 1: FastAPI Webhook Receiver (`backend/main.py`)

```python
# main.py
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data.json"

class Event(BaseModel):
    event: str
    payload: dict

def save_event(event: Event):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(event.dict())

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.post("/webhook")
async def webhook(event: Event, background_tasks: BackgroundTasks):
    print("🔔 Received webhook:", event.dict())
    background_tasks.add_task(save_event, event)
    return {"status": "ok"}

@app.get("/events")
async def get_events():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data
```

---

## 🧩 Part 2: Simulate Webhook Call (`backend/callback.py`)

```python
# callback.py
import httpx
import asyncio

async def send_webhook():
    event_data = {
        "event": "task.created",
        "payload": {
            "task_id": "T-1001",
            "description": "Webhook integration demo",
        },
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/webhook", json=event_data)
        print("Sent webhook:", resp.status_code, resp.text)

if __name__ == "__main__":
    asyncio.run(send_webhook())
```

---

## 🧩 Part 3: React Frontend (Vite + Chakra UI or plain)

### Install:

```bash
npm create vite@latest webhook-frontend --template react
cd webhook-frontend
npm install
npm install axios
```

### React Code (Polling Example)

```tsx
// App.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";

interface Event {
  event: string;
  payload: Record<string, any>;
}

const App = () => {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await axios.get("http://localhost:8000/events", {
          withCredentials: true,
        });
        setEvents(res.data);
      } catch (err) {
        console.error("Error fetching events", err);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📦 Webhook Events</h1>
      {events.map((e, idx) => (
        <div key={idx} style={{ marginBottom: "1rem" }}>
          <strong>Event:</strong> {e.event}
          <pre>{JSON.stringify(e.payload, null, 2)}</pre>
        </div>
      ))}
    </div>
  );
};

export default App;
```

---

## ✅ Running the Demo

1. **Start FastAPI Server**:

   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

2. **Start React Frontend**:

   ```bash
   npm run dev
   ```

3. **Trigger the Webhook**:

   ```bash
   python backend/callback.py
   ```

Your browser should now show the new event from the webhook 🎉

---

## 🔄 Upgrade Options

| Feature                 | How to Do It                                        |
| ----------------------- | --------------------------------------------------- |
| Real-time via WebSocket | Use `fastapi_websocket` + React `socket.io`         |
| Persistent DB           | Replace `data.json` with PostgreSQL/SQLite          |
| Message Queue           | Use `Celery` or `Redis Queue` for heavy webhooks    |
| Signature verification  | Add HMAC header in `callback.py`, verify in FastAPI |
| Retry on failure        | Handle `5xx` with retry queue in sender script      |

---

## 📦 Want the Full GitHub Repo?

I can zip this up into a production-ready starter repo with:

* Modular FastAPI backend
* React + Chakra UI frontend
* WebSocket integration optional
* Deployment configs (e.g., Docker + Nginx + Gunicorn)

Just say: **"Full webhook repo with WebSocket"** or **"Deployable version with DB"** — and I’ll build it for you.
