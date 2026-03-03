pipeline {
    agent any

    environment {
        SERVER_IP = "13.126.134.254"
        APP_DIR   = "/home/ubuntu/jenkins-python-web-app"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image On EC2') {
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

        stage('Restart Containers Using Compose') {
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

        stage('Verify Application') {
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
                to: 'kartik.18901890@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Successful\n\n${env.BUILD_URL}console",
                attachLog: true
            )
        }

        failure {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Failed\n\n${env.BUILD_URL}console",
                attachLog: true
            )
        }
    }
}
