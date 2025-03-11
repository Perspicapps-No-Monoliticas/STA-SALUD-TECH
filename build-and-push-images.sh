#!/bin/bash

PROJECT_ID="saludtech-alpes"
LOCATION="us-central1"
REPOSITORY="sta-images"
REGISTRY_PATH="${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}"

# Authenticate Docker with GCP Artifact Registry
gcloud auth configure-docker ${LOCATION}-docker.pkg.dev

# Find all directories in src folder
find ./src -maxdepth 1 -type d | grep -v "^./src$" | while read -r dir; do
    # Extract service name from directory path
    SERVICE_NAME=$(basename "$dir")
    TAG="latest"
    
    echo "Building image for $SERVICE_NAME..."
    
    # Check if there's a Dockerfile in the directory
    if [ -f "$dir/Dockerfile" ]; then
        # Build the Docker image
        docker build -t "${REGISTRY_PATH}/${SERVICE_NAME}:${TAG}" "$dir"
        
        # Push the image to Artifact Registry
        docker push "${REGISTRY_PATH}/${SERVICE_NAME}:${TAG}"
        
        echo "Successfully built and pushed ${SERVICE_NAME}:${TAG}"
    else
        echo "No Dockerfile found in $dir, skipping..."
    fi
done