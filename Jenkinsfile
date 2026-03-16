pipeline {
    agent any

    environment {
        SERVER_IP = "13.233.215.255"
        APP_DIR   = "/home/ubuntu/jenkins-python-web-app"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('GitSecOps') {
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

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv('sonarqube-server') {
                        sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=python-web-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://13.233.215.255:9000 \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Build') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} '
                        cd ${APP_DIR} &&
                        docker build -t pythonwebapp:${IMAGE_TAG} .
                    '
                    """
                }
            }
        }

        stage('Containers Update') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} '
                        cd ${APP_DIR} &&
                        docker rm -f python-web-app || true &&
                        IMAGE_TAG=${IMAGE_TAG} docker-compose down &&
                        IMAGE_TAG=${IMAGE_TAG} docker-compose up -d
                    '
                    """
                }
            }
        }

        stage('Verify') {
            steps {
                sh """
                sleep 10
                curl -f http://${SERVER_IP}:8091
                """
            }
        }

    }

    post {

        success {
            emailext(
                to: 'kartikkaistha6339@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Successful\n\n${env.BUILD_URL}console",
                attachLog: true
            )
        }

        failure {
            emailext(
                to: 'kartikkaistha6339@gmail.com',
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Failed\n\n${env.BUILD_URL}console",
                attachLog: true
            )
        }

    }
}
