pipeline {
  agent any

  parameters {
    string(name: 'IMAGE_VERSION',description: 'The build version to deploy. Hint: buildnumber')
    choice(name: 'ENV',description: 'The environment you want to deploy this applicaiton to', choices:['dev','prod'] )
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
