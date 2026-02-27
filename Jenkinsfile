pipeline {
    agent any

    environment {
        IMAGE_TAG = "${env.BRANCH_NAME}"
    }

    stages {

        stage('GitSecOps - Strict Secret Check') {
            steps {
                sh '''
                    echo "Running strict secret scan..."
                    if grep -r -iE "AWS_ACCESS_KEY|AWS_SECRET|password|secret" . \
                        --exclude=Jenkinsfile \
                        --exclude-dir=.git; then
                        echo "Secret detected! Failing pipeline."
                        exit 1
                    else
                        echo "No secrets detected."
                    fi
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t pythonwebapp:${IMAGE_TAG} ."
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f python-web-app || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d \
                      --name python-web-app \
                      -p 8091:5000 \
                      pythonwebapp:${IMAGE_TAG}
