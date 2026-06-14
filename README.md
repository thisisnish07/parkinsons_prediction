# Parkinson's Disease Prediction Backend

Production-grade Flask backend for a Parkinson's Disease Prediction platform.

## Features
- Flask REST API with JWT authentication
- SQLAlchemy models (Users, PredictionHistory, ModelMetrics, AuditLogs)
- ML training pipeline with model comparison and selection
- Swagger/OpenAPI documentation
- Logging and audit trails
- Docker + Gunicorn deployment

## Project Structure
See the repository layout in the root folder. Key entrypoint: `app.py`.

## Quick Start (Local)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Train Models
```bash
python -m training.train
```

## Run Tests
```bash
pytest -q
```

## Docker
```bash
docker-compose up --build
```

## API Documentation
Swagger UI is available at:
- `http://localhost:5000/apidocs/`

## Sample Requests
### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"StrongPass123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"StrongPass123"}'
```

### Predict
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"MDVP:Fo(Hz)":119.992,"MDVP:Fhi(Hz)":157.302,"MDVP:Flo(Hz)":74.997,"MDVP:Jitter(%)":0.00784,"MDVP:Jitter(Abs)":0.00007,"MDVP:RAP":0.00370,"MDVP:PPQ":0.00554,"Jitter:DDP":0.01109,"MDVP:Shimmer":0.04374,"MDVP:Shimmer(dB)":0.426,"Shimmer:APQ3":0.02182,"Shimmer:APQ5":0.03130,"MDVP:APQ":0.02971,"Shimmer:DDA":0.06545,"NHR":0.02211,"HNR":21.033,"RPDE":0.414783,"DFA":0.815285,"spread1":-4.813031,"spread2":0.266482,"D2":2.301442,"PPE":0.284654}'
```
