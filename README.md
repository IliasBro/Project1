# Project1 – Name Trend Predictor

## 📘 Overview
Project1 is a powerful developer tool designed to predict future name trends using historical ranking data. Built with Flask, Docker, and deployed on Azure, it delivers predictions through a clean web interface.

### 🔍 Why Project1?
- **🐳 Dockerized Deployment**: Ensures consistency across environments.
- **☁️ Azure Integration**: Easily deploys to Azure Container Apps.
- **📊 Data-Driven Predictions**: Uses historical name data to estimate probability of trend resurgence.
- **🌐 User Interface**: Allows users to interactively test name predictions.
- **🔄 CI/CD Pipeline**: GitHub Actions automates the full deployment process.
- **📈 Machine Learning Ready**: Supports CSV-based input and model persistence via `model.plk`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker (optional but recommended)
- Azure account (for deployment)

### 1. Clone the Repository
```bash
git clone https://github.com/IliasBro/Project1
cd Project1
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Run Locally with Flask
```bash
python backend/app.py
```
Then open [http://localhost:5001](http://localhost:5001) in your browser.

### 2. Run with Docker (Locally)
```bash
docker build --platform linux/amd64 -t iliasbro/project1:latest .
docker run -p 5001:5001 iliasbro/project1:latest
```

### 3. Deploy to Azure Container App
1. Push Docker image to Docker Hub
2. Set secrets in GitHub repository:
   - `AZURE_CREDENTIALS`
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
3. Commit to `main` branch – GitHub Action in `.github/workflows/deploy.yml` will:
   - Build image
   - Push to Docker Hub
   - Deploy to Azure

---

## 🧪 Testing
Project1 uses `pytest`. To run the tests:
```bash
pytest
```

---

## 📦 Environment Variables & Secrets
| Variable | Description |
|----------|-------------|
| `AZURE_CREDENTIALS` | Azure service principal JSON |
| `DOCKERHUB_USERNAME` | DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token |
| `MONGODB_URI` (optional) | MongoDB/Cosmos DB URI |

---

## 📂 Project Structure
```
Project1/
├── backend/
│   ├── app.py              # Flask API
│   └── model/model.plk     # Pickled model payload
├── frontend/
│   └── index.html          # User interface
├── scraped_data.csv        # Raw name data
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── .github/workflows/
    └── deploy.yml          # GitHub Actions deployment config
```

---

## 👨‍💻 Author
Ilias Ehrensperger – Built as part of the MDM Project 1


