pipeline {
    agent any

    environment {
        IMAGE_TAG = "dev"
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

        stage('Deploy') {
            steps {
                sh '''
                    docker-compose up -d --build --force-recreate
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://13.126.134.254:8091
                '''
            }
        }
    }

    post {
        success {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build Successful!

Job Name: ${env.JOB_NAME}
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

Job Name: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: FAILURE

Console Output:
${env.BUILD_URL}console
""",
                attachLog: true
            )
        }
    }
}
