pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                echo 'Installing requirements and running Selenium tests'
                bat 'python -m pip install -r requirements.txt'
                bat 'start /B python app.py'
                bat 'python -m pytest -v tests/test_register.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat 'docker build -t simple-demo:seleniumimage .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'bavyaraghu',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    bat 'echo %DOCKER_PASSWORD% | docker login -u "%DOCKER_USERNAME%" --password-stdin'
                }
            }
        }

        stage('Push Image') {
            steps {
                bat 'docker tag simple-demo:seleniumimage bavya-raghu/simple-demo:seleniumimage'
                bat 'docker push bavya-raghu/simple-demo:seleniumimage'
            }
        }

        stage('Deploy') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
