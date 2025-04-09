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

# Restart FastAPI service
log_message "Restarting FastAPI service..."
sudo systemctl restart fastapi.service || { log_message "Failed to restart FastAPI. Exiting."; exit 1; }

# Restart Nginx service
log_message "Restarting Nginx service..."
sudo systemctl restart nginx.service || { log_message "Failed to restart Nginx. Exiting."; exit 1; }

log_message "Deployment completed successfully!"
