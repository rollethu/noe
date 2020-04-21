import os
import datetime as dt

import boto3
from fabric.api import task, lcd, local, run

settings = {
    "staging": {
        "node_env": "staging",
        "backend_host": "https://api.noe.rollet.app",
        "s3_bucket": "noe.rollet.app",
        "cf_distribution": "EDEEHWJ4WTQG",
    },
    "production": {
        "node_env": "production",
        "backend_host": "https://api.tesztallomas.hu",
        "s3_bucket": "regisztracio.tesztallomas.hu",
        "cf_distribution": "E3HVIVZU5PTARC",
    },
}


@task
def build(environment="staging"):

    local("docker build -t project-noe-frontend:latest .")
    try:
        local("docker rm -f temp-project-noe-frontend")
    except:
        pass
    local(
        "docker run "
        "--name temp-project-noe-frontend "
        "-v ${PWD}/src:/project-noe/frontend/src "
        "-v ${PWD}/public:/project-noe/frontend/public "
        "-v ${PWD}/package.json:/project-noe/frontend/package.json "
        "-e REACT_APP_BACKEND_HOST=%s "
        "-e REACT_APP_NODE_ENV=%s "
        "project-noe-frontend:latest "
        "yarn build" % (settings[environment]["backend_host"], settings[environment]["node_env"])
    )
    local("docker cp temp-project-noe-frontend:project-noe/frontend/build temp_build")
    local("docker rm -f temp-project-noe-frontend")


@task
def deploy(environment="staging"):
    local("pwd")
    local("ls -la")
    local("aws s3 sync temp_build s3://{}".format(settings[environment]["s3_bucket"]))
    local("rm -rf temp_build")

    client = boto3.client("cloudfront")
    items_to_invalidate = [
        "/",
        "/static/css/styles.sass",
        "/index.html",
        "/favicon.ico",
        "/manifest.json",
        "/app-icon.png",
    ]
    client.create_invalidation(
        DistributionId=settings[environment]["cf_distribution"],
        InvalidationBatch={
            "Paths": {"Quantity": len(items_to_invalidate), "Items": items_to_invalidate},
            "CallerReference": dt.datetime.now().strftime("%Y%m%d%H%M%S"),
        },
    )
