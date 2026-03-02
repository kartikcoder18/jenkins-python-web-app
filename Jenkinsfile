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

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d \
                      --name python-web-app \
                      -p 8091:5000 \
                      pythonwebapp:${IMAGE_TAG}
                '''
            }
        }

        stage('Verify') {
            steps {
                sh 'sleep 5 && curl -f http://13.126.134.254:8091'
            }
        }
    }

    post {
        success {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Successful!\n\n${env.BUILD_URL}"
            )
        }
        failure {
            emailext(
                to: 'kartik.18901890@gmail.com',
                subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Failed!\n\n${env.BUILD_URL}"
            )
        }
    }
}
