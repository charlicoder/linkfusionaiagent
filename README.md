Here's a **README update** that includes the deployment automation steps:  

---

# **LinkFusionAIAgent - Deployment Guide**  

This guide outlines the automated deployment process for **LinkFusionAIAgent** using a Bash script.  

## **Deployment Automation Script**  

To streamline deployment, we use a Bash script that:  
- Pulls the latest changes from the repository  
- Stops running containers  
- Builds the **LangGraph** project  
- Starts updated containers  
- Restarts necessary services  

### **Setup & Usage**  

#### **1. Create the Deployment Script**  
Save the following script as `deploy.sh` in your project root:  

```bash
#!/bin/bash

# Define log file
LOG_FILE="deployment.log"

# Function to log messages
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a $LOG_FILE
}

log_message "Starting deployment of LinkFusionAIAgent..."

# Pull the latest changes from the main branch
log_message "Pulling latest changes from Git..."
git pull origin main || { log_message "Failed to pull from Git. Exiting."; exit 1; }

# Stop and remove existing Docker containers
log_message "Stopping existing Docker containers..."
docker compose down || { log_message "Failed to stop Docker containers. Exiting."; exit 1; }

# Build the LangGraph project
log_message "Building LangGraph project..."
langgraph build -t linkfusionaiagent || { log_message "LangGraph build failed. Exiting."; exit 1; }

# Start Docker containers
log_message "Starting Docker containers..."
docker compose up -d || { log_message "Failed to start Docker containers. Exiting."; exit 1; }

# Restart FastAPI service
log_message "Restarting FastAPI service..."
sudo systemctl restart fastapi || { log_message "Failed to restart FastAPI. Exiting."; exit 1; }

# Restart Nginx service
log_message "Restarting Nginx service..."
sudo systemctl restart nginx.service || { log_message "Failed to restart Nginx. Exiting."; exit 1; }

log_message "Deployment completed successfully!"
```

#### **2. Make the Script Executable**  
Run the following command to grant execution permissions:  
```bash
chmod +x deploy.sh
```

#### **3. Execute the Deployment Script**  
To deploy the latest updates, run:  
```bash
./deploy.sh
```

#### **4. Logs & Troubleshooting**  
- All deployment logs are stored in `deployment.log`.  
- If any step fails, check the log file for details.  
- Ensure you have the necessary permissions to restart **FastAPI** and **Nginx** (`sudo` access required).  




# LinkFusionAIAgent

How to run agent ai:

1. git pull origin main
1. docker compose down
2. langgraph build -t linkfusionaiagent
3. docker compose up -d
4. sudo systemctl restart fastapi
5. sudo systemctl restart nginx.service




---

# AIAGETN flow diagram

![Memories Explorer](./static/diagram.png)

## How to setup local development environment?

## How to deploy in dev/production site?


