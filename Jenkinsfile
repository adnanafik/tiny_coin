pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        echo 'Building code'
        withKubeConfig(credentialsId: 'kubeconfig', contextName: 'cluster-kubernetes.dev.affinionservices.com', clusterName: 'cluster-kubernetes.dev.affinionservices.com') {
          echo 'test'
        }

      }
    }
  }
}