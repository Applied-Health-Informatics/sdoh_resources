# Deployment with GCP

## Utilization Cloud Run
- Prequests:
    - Need to push image to a registry, like docker hub 
        - e.g., `docker build -t sdoh .`
        - e.g., `docker tag sdoh hants/sdoh-demo`
        - e.g., `docker push hants/sdoh-demo`
    - In the current iteration, have pushed image to docker hub (docker.io/hants/sdoh-demo)

- Steps:
    - Create a new service in Cloud Run
    - Select the image from the registry
    - Set the port in the image to match the port in the Cloud Run service, which currently is 5001