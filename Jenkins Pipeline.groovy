pipeline {
    agent {
        label "builtin"
    }
    
    environment{
        Docker_image = 'rahib685/schema-generator:latest'
        
    }
    
    stages {
        stage('Checkout') {
            steps {
                dir('schema-generator') {
                    git branch: 'main', url: 'https://github.com/Rahib20/schema-generator.git'
                }
                dir('api-test') {
                    git branch: 'main', url: 'https://github.com/Rahib20/test_api.git' 
                }
                 }
        }

        
        stage('Run Unit Tests') {
            steps {
                dir('schema-generator') {
                    withPythonEnv('python3') {
                        sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        export FLASK_APP=Scema.py
                        sleep 5
                        nohup flask run --host=0.0.0.0 --port=5000 &
                        python3 -m pytest
                        '''
                    }
                }
            }
        }
        
        
        stage('Coverage set up') {
            steps {
                dir('schema-generator') {
                    sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest --cov=Scema --cov-report=xml
                    '''
                }
            }
        }
        
        stage('SonarScan') {
            steps {
                dir('schema-generator') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        withSonarQubeEnv('RR SonarCloud') {
                            sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=Rahib20_schema-generator \
                            -Dsonar.organization=rahib20 \
                            -Dsonar.host.url=https://sonarcloud.io \
                            -Dsonar.sources=Scema.py \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.qualitygate.wait=true \
                            -Dsonar.qualitygate.timeout=300
                            """
                        }
                    }
                }
            }
        }
        
        stage('Run api Tests') {
            steps {
                dir('api-test') {
                    withPythonEnv('python3') {
                        sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        python api_test.py
                     
                    
                        '''
                    }
                }
            }
        }
    
    
        
        stage('Build and Push Docker Image') {
            steps {
                dir('schema-generator') {
                    withCredentials([usernamePassword(credentialsId: 'rr-dockerhub', usernameVariable: 'docker_username', passwordVariable: 'docker_pass')]) {
                        sh '''
                        echo "$docker_pass" | docker login -u "$docker_username" --password-stdin
                        docker build -t $Docker_image .
                        docker push $Docker_image
                        '''
                    }
                }
            }
        }
 
        
    stage('Deploy to VM') {
            steps {
                script {
                    def remote = [:]
                    remote.name = 'Rahib VM'
                    remote.host = '18.208.212.20' 
                    remote.user = 'ubuntu'
                    remote.allowAnyHosts = true

                    withCredentials([sshUserPrivateKey(credentialsId: 'rr-newvm-ssh', keyFileVariable: 'identity', usernameVariable: 'userName')]) {
                        remote.user = userName
                        remote.identityFile = identity

                        writeFile file: 'deploy_server.sh', text: """
                        kubectl -n schema-gen rollout restart statefulset schema-generator
                        kubectl -n schema-gen rollout status statefulset/schema-generator --timeout=120s
                        pkill -f "kubectl -n schema-gen port-forward svc/schema-generator" || true
                        echo "killing old server"
                        nohup kubectl -n schema-gen port-forward svc/schema-generator 30080:80 --address=0.0.0.0 > portforward.log 2>&1 &
                        echo "Server restarted"
                        """
                        sshScript remote: remote, script: 'deploy_server.sh'
                        
                        
                    }
                }
            }
    }


    }

    post {
        success {
            sh 'pkill -f "flask run" || true'
            echo "success"
            
        }
    }
}
