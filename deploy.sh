#!/bin/bash

# Define log file
LOG_FILE="deployment.log"

# Function to log messages
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a $LOG_FILE
}

log_message "Starting deployment of aiagent..."

# Pull the latest changes from the main branch
log_message "Pulling latest changes from Git..."
git pull origin develop || { log_message "Failed to pull from Git. Exiting."; exit 1; }

echo "creating docker image"
docker build -t aiagent  .

### Complete Deployment
echo "killing the running docker"
docker ps -a | egrep 'aiagent' | awk '{print $1}'| xargs docker kill
docker ps -a | egrep 'aiagent' | awk '{print $1}'| xargs docker rm


# echo "running celery"
# celery -A core worker -l info -D

echo "running the aiagent using docker"

docker run -d \
    --restart=unless-stopped \
    --name aiagent \
    -p 8002:8002 \
    -v /home/linkfusion/production/linkfusionaiagent/data:/app/data \
    aiagent

echo "We are done !"
