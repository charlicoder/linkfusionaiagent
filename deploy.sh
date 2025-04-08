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
git pull origin develop || { log_message "Failed to pull from Git. Exiting."; exit 1; }

echo "creating docker image"
docker build -t linkfusionaiagent .

### Complete Deployment
echo "killing the running docker"
docker ps -a | egrep 'aiagent' | awk '{print $1}'| xargs docker kill
docker ps -a | egrep 'aiagent' | awk '{print $1}'| xargs docker rm


echo "running the linkfusion using docker"
# docker run -d --restart=unless-stopped --name linkfusion-v2-dev -p 8000:8000 linkfusion-v2-dev
docker run -d \
    --restart=unless-stopped \
    --name aiagent \
    -p 8002:8002 \
    -v /home/linkfusion/production/linkfusionaiagent/data:/app/data \
    linkfusionaiagent

echo "We are done !"

log_message "Deployment completed successfully!"
