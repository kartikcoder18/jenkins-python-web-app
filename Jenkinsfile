pipeline {
    agent any

    stages {

        stage('Select Branch') {
            steps {
                script {
                    def userBranch = input(
                        message: 'Enter Branch Name to Build',
                        parameters: [
                            string(
                                name: 'BRANCH_NAME',
                                defaultValue: 'main'
                            )
                        ]
                    )
                    env.BRANCH_NAME = userBranch
                    env.IMAGE_TAG = userBranch
                }
            }
        }

        stage('Clone Code') {
            steps {
                git(
                    branch: "${env.BRANCH_NAME}",
                    url: 'https://github.com/kartikcoder18/jenkins-python-web-app.git'
                )
            }
        }

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
                sh "docker build -t pythonwebapp:${env.IMAGE_TAG} ."
            }
        }

        stage('Stop Old Container (Compose Down)') {
            steps {
                sh 'docker compose down || true'
            }
        }

        stage('Deploy With Compose') {
            steps {
                sh '''
                    export IMAGE_TAG=${IMAGE_TAG}
                    docker compose up -d --build
                '''
            }
        }

        stage('Verify') {
            steps {
                sh 'sleep 5 && curl -f http://localhost:8091'
            }
        }
    }

    post {
        success {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build Successful!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Branch: ${env.BRANCH_NAME}

Check console output:
${env.BUILD_URL}
"""
            )
        }

        failure {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build Failed!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Branch: ${env.BRANCH_NAME}

Check console output:
${env.BUILD_URL}
"""
            )
        }
    }
}
