pipeline {
    agent any

    environment {
        SERVER_IP   = "13.126.134.254"
        SERVER_USER = "ubuntu"
        APP_DIR     = "/home/ubuntu/jenkins-python-web-app"
        BRANCH      = "dev/kartik"
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Test SSH Connection') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_IP} "echo SSH Connection Successful"
                """
            }
        }

        stage('Pull Latest Code on EC2') {
            steps {
                sh """
                ssh ${SERVER_USER}@${SERVER_IP} '
                    cd ${APP_DIR} &&
                    git pull origin ${BRANCH}
                '
                """
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh """
                ssh ${SERVER_USER}@${SERVER_IP} '
                    cd ${APP_DIR} &&
                    docker-compose down || true
                '
                """
            }
        }

        stage('Build Docker Image Using Compose') {
            steps {
                sh """
                ssh ${SERVER_USER}@${SERVER_IP} '
                    cd ${APP_DIR} &&
                    docker-compose build
                '
                """
            }
        }

        stage('Start Containers') {
            steps {
                sh """
                ssh ${SERVER_USER}@${SERVER_IP} '
                    cd ${APP_DIR} &&
                    docker-compose up -d
                '
                """
            }
        }

        stage('Verify Running Containers') {
            steps {
                sh """
                ssh ${SERVER_USER}@${SERVER_IP} '
                    docker ps
                '
                """
            }
        }

        stage('Verify Application Deployment') {
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
                body: """Build Successful!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: SUCCESS

Console Output:
${env.BUILD_URL}console
""",
                attachLog: true
            )
        }

        failure {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build Failed!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: FAILURE

Console Output:
${env.BUILD_URL}console
""",
                attachLog: true
            )
        }

        always {
            echo "Pipeline Finished."
        }
    }
}
