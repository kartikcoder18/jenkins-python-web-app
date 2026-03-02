pipeline {
    agent any

    environment {
        IMAGE_NAME = "pythonwebapp"
        IMAGE_TAG  = "dev"
        SERVER_IP  = "13.126.134.254"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Show Docker Images Before Build') {
            steps {
                sh 'docker images'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Show Docker Images After Build') {
            steps {
                sh 'docker images'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker-compose down'
            }
        }

        stage('Start New Container') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Verify Deployment') {
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
