# WebSocket Chat API – FastAPI + WebSocket

A lightweight, scalable real-time chat backend built using **FastAPI WebSockets**, featuring multi-room support, broadcast messaging, clean architecture, Docker setup, and a minimal HTML client. Ideal for learning how WebSockets work or as a starter project for production-ready real-time apps.

---

##  Features

- Real-time messaging using WebSockets  
- Multiple users & chat rooms  
- Join/leave notifications  
- Broadcast messages to room members  
- Clean folder structure (production-ready)  
- Pydantic models for validation  
- REST Health Check API  
- HTML + JavaScript client included  
- Docker & Docker Compose support  
- Unit tests using `pytest` & `websockets`  
- Environment-based configuration (`.env`)

---

##  Project Structure
``` bash
websocket-chat-app/
├── app/
│ ├── init.py
│ ├── main.py # WebSocket endpoint & FastAPI app
│ ├── config.py # Environment settings (pydantic)
│ ├── logger.py # Logging configuration
│ ├── schemas.py # Pydantic models for messages
│ ├── utils.py # Helper functions
│ └── ws_manager.py # WebSocket room & broadcast manager
├── static/
│ └── index.html # Simple WebSocket client UI
├── tests/
│ └── test_ws_chat.py # WebSocket integration test
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uvicorn.sh
└── README.md
```
---

##  Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/websocket-chat-app.git
cd websocket-chat-app
```
### Setup Virtual Environment
```bash
python -m venv .venv
# Activate:
# Windows:
.venv\Scripts\activate
# Unix/Mac:
source .venv/bin/activate

pip install -r requirements.txt  # or `pip install -e .` if using pyproject.toml
```


### Run the Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Now open the WebSocket chat UI in your browser:
```
http://localhost:8000/static/index.html
```

## WebSocket API Usage
📌 Endpoint
```bash
ws://localhost:8000/ws?username=<name>&room=<room_name>
```
| Query Param | Required | Description                |
| ----------- | -------- | -------------------------- |
| `username`  |  Yes    | Display name in chat       |
| `room`      |  No     | Chat room (default: lobby) |
### Incoming Message Format (Client → Server)
```json
{
  "type": "chat",
  "text": "Hello everyone!"
}
```
### Outgoing Message Format (Server → Client)
```json
{
  "type": "chat",
  "sender": "alice",
  "text": "Hello!",
  "room": "lobby"
}
```
- System messages (join/leave):

```json
{
  "type": "system",
  "sender": "system",
  "text": "alice joined",
  "room": "lobby"
}
```

## Docker Deployment

Build and Run
```bash
docker compose up --build

```
Server runs at: http://localhost:8000

WebSocket UI at: http://localhost:8000/static/index.html
## Health Check
```bash
curl http://localhost:8000/health
```
Response:
```json
{ "status": "ok", "app": "WebSocket Chat API" }
```
## Environment Variables

Create a `.env` file (copy from `.env.example`):
```ini
APP_NAME=WebSocket Chat API
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

## Future Improvements (if you want to expand)

- Persist chat history to database (MongoDB, PostgreSQL, Redis)
- JWT authentication / OAuth2 login
- Private messages (user-to-user)
- Typing indicators, message timestamps
- Frontend using React / Vue / Next.js
- Kubernetes deployment (Ingress + Auto-scale)

## Contributing

1. Fork this repository
2. Create your feature branch `(git checkout -b feature-name)`
3. Commit changes `(git commit -m "Add new feature")`
4. Push to branch `(git push origin feature-name)`
5. Create a Pull Request 

## License

This project is open-source and available under the MIT License.

## ⭐ Support

If this project helped you, you can support by:

- Giving a ⭐ on GitHub
- Sharing it with other developers
- Asking for the next API (REST, WebRTC, GraphQL, Webhooks, etc.)