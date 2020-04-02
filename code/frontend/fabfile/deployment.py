import os
import datetime as dt

import boto3
from fabric.api import task, lcd, local, run


@task
def build():
    local('docker build -t project-noe-frontend:latest .')
    try:
        local('docker rm -f temp-project-noe-frontend')
    except:
        pass
    local('docker run '
          '--name temp-project-noe-frontend '
          '-v ${PWD}/src:/project-noe/frontend/src '
          '-v ${PWD}/public:/project-noe/frontend/public '
          '-v ${PWD}/package.json:/project-noe/frontend/package.json '
          'project-noe-frontend:latest '
          'yarn build')
    local('docker rm -f temp-project-noe-frontend')


@task
def deploy():
    local('aws s3 sync temp/build s3://noe.rollet.app')
    local('rm -rf temp')

    client = boto3.client('cloudfront')
    items_to_invalidate = [
        '/',
        '/static/css/styles.sass',
        '/index.html',
        '/favicon.ico',
        '/manifest.json',
        '/app-icon.png',
    ]
    for distribution_id in os.environ.get('AWS_CLOUDFRONT_DISTRIBUTION_IDS', '').split(','):
        client.create_invalidation(
            DistributionId=distribution_id.strip(),
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(items_to_invalidate),
                    'Items': items_to_invalidate
                },
                'CallerReference': dt.datetime.now().strftime('%Y%m%d%H%M%S')
            }
    )
