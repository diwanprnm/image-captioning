# Image Captioning Service

A FastAPI microservice that generates image captions/alt-text using a vision LLM via 9router.

## Features

- Upload image (PNG, JPEG, WebP) and get descriptive caption
- Optional storage of image metadata and caption in Postgres
- Vision model call via 9router (OpenAI-compatible)
- Error handling, file size limits, content-type validation
- Interactive API docs (Swagger UI) at `/docs`

## Requirements

- Python 3.11+
- Docker (for local database and potential future deployment)
- Postgres 15+ (or use Docker)
- A 9router instance (or compatible OpenAI vision endpoint) with API key

## Local Development

### 1. Clone the repository

bash
git clone <your-repo-url>
cd image-captioning-service

### 2. Create and activate virtual environment

bash
On Windows
py -m venv venv
.\venv\Scripts\Activate.ps1
On Linux/Mac
python3 -m venv venv

### 3. Install dependencies

bash
pip install -r requirements.txt

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your secrets:
bash
cp .env.example .env

Then edit .env with your secrets
notepad .env
**Important:**

- `POSTGRES_PASSWORD`: Your Postgres password.
- `POSTGRES_PORT`: Use `5433` if your container maps to that port, or `5432` if default.
- `POSTGRES_SERVER`: Use `localhost` if connecting to local Postgres, or `db` if using `docker-compose`.
- `NINE_ROUTER_API_KEY`: Your actual 9router API key.
- `NINE_ROUTER_VISION_MODEL`: Model name (e.g., `combofreetwo`, `gpt-4-vision-preview`).

### 5. Start the database (if using Docker)

bash
docker compose up -d db
Ensure it's running: `docker ps`

### 6. Run the FastAPI application

bash
uvicorn app.main:app --reload
Access the API docs at `http://127.0.0.1:8000/docs`.

## Docker Deployment

### 1. Build the Docker image

bash
docker compose build

### 2. Run the application with Docker Compose

bash
docker compose up -d (1/2)
The application will be available at `http://localhost:8000`.

## API Usage

**POST `/api/v1/caption/`**

- Accepts `multipart/form-data` with a file field named `file`.
- Supports image types: PNG, JPEG, WebP.
- Max upload size: 5MB.
- **Response:**
  json
  {
  "id": 1,
  "filename": "upload.png",
  "caption": "A detailed description of the image content.",
  "model_used": "combofreetwo",
  "created_at": "2026-08-18T09:45:00Z"
  }

## Testing

Run the test suite to verify functionality:
bash
Activate venv first if needed
.\venv\Scripts\Activate.ps1
python -m pytest tests\ -v
This runs unit tests, integration tests, and E2E tests.
