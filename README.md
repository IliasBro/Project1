# Project1 – Name Trend Predictor

---

## 📚 Table of Contents

- [📘 Overview](#-overview)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Python Dependencies](#2-install-python-dependencies)
- [▶️ Usage](#️-usage)
  - [1. Run Locally with Flask](#1-run-locally-with-flask)
  - [2. Run with Docker (Locally)](#2-run-with-docker-locally)
  - [3. Deploy to Azure Container App](#3-deploy-to-azure-container-app)
- [🧪 Testing](#-testing)
- [📦 Environment Variables & Secrets](#-environment-variables--secrets)
- [📂 Project Structure](#-project-structure)
- [📦 Deployment](#-deployment)
- [👨‍💻 Author](#-author)

---

## 📘 Overview
Project1 is a powerful developer tool designed to predict future name trends using historical ranking data. Built with Flask, Docker, and deployed on Azure, it delivers predictions through a clean web interface.

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

## 📦 Deployment

For detailed deployment instructions (including Docker & Azure), see the [Deployment Guide](./DEPLOYMENT.md).

---

## 👨‍💻 Author
Ilias Ehrensperger – Built as part of the MDM Project 1


