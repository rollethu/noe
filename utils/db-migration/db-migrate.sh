#!/bin/bash

# # Global vars
# AWS_REGION='eu-west-1'
# ECS_CLUSTER='dev-ecs-pri-cluster'
# TD_NAME='juice-db-migrate'
# ORIGINAL_TD_NAME='zxcv'
# IMAGE='asd'

echo "------Starting script." >&2

# Checks
echo "------Doing pre-flight checks" >&2
command -v jq > /dev/null
if [ $? -gt 0 ]; then
  echo "------Pre-flight check have failed. Install JQ" >&2
  exit 2
fi

command -v aws > /dev/null
if [ $? -gt 0 ]; then
  echo "------Pre-flight check have failed. Install AWS CLI" >&2
  exit 2
fi

# stat task-definition.json > /dev/null 2>&1
# if [ $? -gt 0 ]; then
#   echo "------Pre-flight check have failed. Couldn't find task-definition.json" >&2
#   exit 2
# fi

stat override.json > /dev/null 2>&1
if [ $? -gt 0 ]; then
  echo "------Pre-flight check have failed. Couldn't find override.json" >&2
  exit 2
fi

aws ecs describe-task-definition --task-definition ${ORIGINAL_TD_NAME} --region eu-central-1 > task-definition.temp.json
cat task-definition.temp.json | jq ".taskDefinition.containerDefinitions[0].image = \"${IMAGE}\"" | jq -r '{containerDefinitions: .taskDefinition.containerDefinitions}' > task-definition.json

CONTAINER_NAME=$(cat task-definition.json | jq -r '.containerDefinitions[0].name')
LOG_GROUP_NAME=$(cat task-definition.json | jq -r '.containerDefinitions[0].logConfiguration.options."awslogs-group"')
LOG_STREAM_NAME=$(cat task-definition.json | jq -r '.containerDefinitions[0].logConfiguration.options."awslogs-stream-prefix"')

echo "------Registering new Task Definition for the cluster" >&2
aws ecs register-task-definition --region ${AWS_REGION} --cli-input-json file://task-definition.json >/dev/null
if [ $? -gt 0 ]; then
  echo "------Failed registering task to ECS" >&2
  exit 2
fi
RUNTASK_RESPONSE=$(aws ecs run-task \
  --region ${AWS_REGION} \
  --cluster ${ECS_CLUSTER} \
  --task-definition ${TD_NAME}  \
  --cli-input-json file://override.json)

if [ $? -gt 0 ]; then
  echo "------Failed to run task" >&2
  exit 2
fi

TASKID=$(echo $RUNTASK_RESPONSE | jq -r '.tasks[0].containers[0].taskArn')
TASK_CREATED_AT=$(echo $RUNTASK_RESPONSE | jq -r '.tasks[0].createdAt')
TASKID_CLEAN=${TASKID##*/}
TASK_CREATED_AT_CLEAN=${TASK_CREATED_AT%%.*}
LOG_TO_TAIL="$LOG_STREAM_NAME/$CONTAINER_NAME/$TASKID_CLEAN"

echo "------Waiting for the task to start" >&2
aws ecs wait tasks-running --cluster ${ECS_CLUSTER} --tasks ${TASKID} --region ${AWS_REGION}
if [ $? -gt 0 ]; then
  echo "------ Waiting for the task to start have failed. Probably nothing serious, just aws glitch. Carrying on." >&2
fi

echo "------ ${TASKID} started" >&2

echo "------Waiting for the task to finish" >&2
aws ecs wait tasks-stopped --cluster ${ECS_CLUSTER} --tasks ${TASKID} --region ${AWS_REGION}
echo "------Task execution has finished. Getting all the logs." >&2
LOG_ENTRIES=$(aws logs get-log-events \
  --region ${AWS_REGION} \
  --log-group-name ${LOG_GROUP_NAME} \
  --log-stream-name $LOG_TO_TAIL) 
echo $LOG_ENTRIES | jq -r '.events[].message'

echo "------Checking the exit code" >&2
TASK_EXITCODE=$(aws ecs describe-tasks --cluster ${ECS_CLUSTER} --tasks ${TASKID} --region ${AWS_REGION} | jq -e -r '.tasks[0].containers[0].exitCode')
if [ $? -gt 0 ];then
  TASK_EXITCODE=1
fi  
if [ $TASK_EXITCODE -gt 0 ]; then
  echo "------Migration have failed. Exiting." >&2
  exit $TASK_EXITCODE 
else
  echo "------Migration have finished. Exiting." >&2
  exit 0
fi