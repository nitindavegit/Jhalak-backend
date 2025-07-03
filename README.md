# Jhalak Backend

A modern FastAPI backend for the Jhalak project, providing cultural personality quiz logic, authentication, and integration with Firebase and OpenAI.

---

## 🚀 Features
- FastAPI-based REST API
- JWT authentication (Firebase)
- Cultural personality quiz endpoints
- OpenAI integration
- Dockerized for easy deployment
- CORS enabled for frontend integration

---

## 🛠️ Tech Stack
- Python 3.13
- FastAPI
- Firebase Admin SDK
- OpenAI API
- Docker

---

## ⚡ Quick Start (Local)

1. **Clone the repo:**
   ```sh
   git clone https://github.com/yourusername/jhalak-backend.git
   cd hak-backend
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Add your `.env` file** (see below for required variables).
5. **Run the server:**
   ```sh
   uvicorn main:app --reload
   ```
6. **API available at:**
   - [http://localhost:8000](http://localhost:8000)

---

## 🐳 Run with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t jhalak-backend .
   ```
2. **Run the container:**
   ```sh
   docker run --env-file .env -p 8000:8000 hak-backend
   ```
   - If using a service account JSON file:
     ```sh
     docker run --env-file .env -v $(pwd)/serviceAccount.json:/app/serviceAccount.json -p 8000:8000 hak-backend
     ```

---

## 🌱 Environment Variables
Create a `.env` file in the backend folder with the following (example):

```
OPENAI_API_KEY=your-openai-key
OPENAI_BASE_URL=your-openai-base-url
# Firebase config
apiKey=...
authDomain=...
projectId=...
storageBucket=...
messagingSenderId=...
appId=...
measurementId=...
databaseURL=...
# Service account (if using env vars for each field)
SERVICE_ACCOUNT_TYPE=service_account
SERVICE_ACCOUNT_PROJECT_ID=...
SERVICE_ACCOUNT_PRIVATE_KEY_ID=...
SERVICE_ACCOUNT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n
SERVICE_ACCOUNT_CLIENT_EMAIL=...
SERVICE_ACCOUNT_CLIENT_ID=...
SERVICE_ACCOUNT_AUTH_URI=...
SERVICE_ACCOUNT_TOKEN_URI=...
SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL=...
SERVICE_ACCOUNT_CLIENT_X509_CERT_URL=...
SERVICE_ACCOUNT_UNIVERSE_DOMAIN=...
# Or, if using a file:
SERVICE_ACCOUNT_PATH=/app/serviceAccount.json
```

---

## 🌍 Deployment (Render)
- Push your code to GitHub.
- Create a new Web Service on [Render](https://render.com/):
  - **Runtime:** Docker
  - **Port:** `$PORT` (use `$PORT` env variable in your Dockerfile or set to 10000)
  - **Set all environment variables in the Render dashboard**
- For service account, use env vars or mount the file as shown above.

---

## 🔒 Security Notes
- **Never commit your `.env` or `serviceAccount.json` to version control.**
- Use `.gitignore` and `.dockerignore` to keep secrets out of your repo and Docker images.
- Store all secrets in environment variables or secure mounts.

---

## 📚 API Endpoints (Examples)
- `GET /get-quiz` — Get quiz questions
- `POST /submit-quiz` — Submit quiz answers
- `POST /signup` — Create a new user
- `POST /login` — Login and get JWT

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
[MIT](../LICENSE) 