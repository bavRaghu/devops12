# Week 12: Flask Registration App, Selenium Tests, Docker, Jenkins, and Kubernetes

## Project structure

```text
week12_selenium_registration/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── deployment.yaml
├── service.yaml
├── templates/
│   ├── reg.html
│   └── success.html
└── tests/
    └── test_register.py
```

## Run locally on Windows

Open PowerShell in this project directory and run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Keep that terminal open. In a second PowerShell window, from this directory, run:

```powershell
python -m pytest -v tests/test_register.py
```

The tests expect the Flask app to be available at `http://127.0.0.1:5000/`. Do not start a second copy if the app is already running.

## Docker

```powershell
docker build -t simple-demo:seleniumimage .
docker run --rm -p 5000:5000 simple-demo:seleniumimage
```

If port 5000 is already occupied, use a different host port, for example `docker run --rm -p 5001:5000 simple-demo:seleniumimage`, and update the test URL accordingly.

## Jenkins and Kubernetes notes

- Create a Jenkins Username with password credential whose ID is `dockerhub-credentials`, with your Docker Hub username and an access token as the password.
- Update the Docker Hub image path in `Jenkinsfile` and `deployment.yaml` to your real Docker Hub username and repository.
- Ensure Docker Desktop and a Kubernetes cluster are running and that Jenkins can access both `docker` and `kubectl`.
- The test stage starts the Flask app in the background. For a reliable CI setup, use a process-management approach that waits for the app to become ready and shuts it down after testing.
- Selenium tests require Chrome and a compatible ChromeDriver on the machine running pytest. If Jenkins runs as a Windows service, verify that Chrome/driver downloads and browser startup work under that service account.
