pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "ganesh0912/hw3-backend"
        FRONTEND_IMAGE = "ganesh0912/hw3-frontend"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Ganeshjasti0912/645-hw3.git'
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                script {
                    sh '''
                    cd backend
                    docker build -t $BACKEND_IMAGE:latest .
                    '''
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    sh '''
                    cd frontend
                    docker build -t $FRONTEND_IMAGE:latest .
                    '''
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $BACKEND_IMAGE:latest
                        docker push $FRONTEND_IMAGE:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                    kubectl apply --validate=false --insecure-skip-tls-verify=true -f k8s/backend-deployment.yaml
                    kubectl apply --validate=false --insecure-skip-tls-verify=true -f k8s/backend-service.yaml
                    kubectl apply --validate=false --insecure-skip-tls-verify=true -f k8s/frontend-deployment.yaml
                    kubectl apply --validate=false --insecure-skip-tls-verify=true -f k8s/frontend-service.yaml

                    '''
                }
            }
        }
    }
}
