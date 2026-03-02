pipeline {
    agent any

    environment {
        SERVER_IP = "13.126.134.254"
        APP_DIR   = "/home/ubuntu/jenkins-python-web-app"
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
                    ssh -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} "
                        cd ${APP_DIR} &&
                        docker build -t pythonwebapp:latest .
                    "
                    """
                }
            }
        }

        stage('Restart Containers Using Compose') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} "
                        cd ${APP_DIR} &&
                        docker-compose down &&
                        docker-compose up -d
                    "
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
                body: """Build Successful

Job: ${env.JOB_NAME}
Build: ${env.BUILD_NUMBER}

Console:
${env.BUILD_URL}console
""",
                attachLog: true
            )
        }

        failure {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build Failed

Job: ${env.JOB_NAME}
Build: ${env.BUILD_NUMBER}

Console:
${env.BUILD_URL}console
""",
                attachLog: true
            )
        }
    }
}
