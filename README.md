# GitHub Actions Practice

![Docker Build and Publish](https://github.com/RushabhSahare/github-actions-practice/actions/workflows/docker-publish.yml/badge.svg)

Daily hands-on GitHub Actions practice as part of the 90 Days of DevOps program by TrainWithShubham.

## Day 45: Docker Build & Push CI/CD

The `docker-publish.yml` workflow builds the Flask To-Do app from Day 36 into a Docker image and pushes it to Docker Hub on every push to `main`. Feature branches build the image but skip the push step.

Image: [rushabhs7/flask-todo](https://hub.docker.com/r/rushabhs7/flask-todo)
