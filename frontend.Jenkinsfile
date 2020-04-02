pipeline {
  agent {
    label 'boto3 && fabric'
  }

  environment {
      AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
      AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
      AWS_CLOUDFRONT_DISTRIBUTION_IDS = credentials('AWS_CLOUDFRONT_DISTRIBUTION_IDS')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        sh "fab deployment.build_frontend"
      }
    }

    stage('Test') {
      steps {
        sh """echo "testing placeholder" """
      }
    }

    stage('Deploy') {
      steps {
        sh "fab deployment.deploy_frontend"
      }
    }
  }
}
