# 🚀 Deployment Guide for Project1

This guide walks you through deploying your Project1 Flask + Docker app to **Azure Container Apps** using GitHub Actions.

---

## ✅ Prerequisites

1. **Azure Account** with:
   - Azure Subscription
   - Azure Container App environment created
   - Azure Cosmos DB for MongoDB (optional if using DB)
2. **Docker Hub Account**
3. **GitHub Repository** (linked with your local project)
4. **Service Principal** created in Azure

---

## 🧩 Azure Service Principal & Secrets

Generate credentials:

```bash
az ad sp create-for-rbac --name "project1-gh" --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID> \
  --sdk-auth
```

Copy the output and add to your repo secrets as `AZURE_CREDENTIALS`

Also add:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

If needed:
- `MONGODB_URI` for Azure Cosmos DB

---

## 🐳 Docker Image

Build and test your container locally:

```bash
docker build --platform linux/amd64 -t iliasbro/project1:latest .
docker run -p 5001:5001 iliasbro/project1:latest
```

Then push:

```bash
docker push iliasbro/project1:latest
```

---

## ⚙️ GitHub Action for CI/CD

Your `.github/workflows/deploy.yml` file should:

1. Log in to Azure
2. Build and push Docker image
3. Deploy to Container App

Already set up? Just commit and push:

```bash
git add .
git commit -m "Trigger deploy"
git push origin main
```

---

## 🛰 Azure Container App

Make sure the container app:
- Is using **linux/amd64** platform
- Opens port 5001
- Has ingress enabled
- Has environment variables set if needed

Check the log stream via:
```bash
az containerapp logs show --name <app-name> --resource-group <rg>
```

---

## ✅ Troubleshooting

### App doesn't load?
- Check if port 5001 is open in your app.
- Visit the **FQDN** from the Azure Container App output.

### MongoDB errors?
- Ensure `MONGODB_URI` is valid.
- Make sure IP access is enabled in Cosmos DB firewall settings.

### Docker error: `unauthorized`
- Your `DOCKERHUB_TOKEN` might be invalid or missing `write` scope.

