#!/usr/bin/env sh

set -ex

cd "$(dirname "$0")"
echo "$(date +%Y-%m-%d-%H-%M-%S) - init-dokku-back.sh $@"

HOST=$1
SERVICE_NAME=$2
PORT=$3
MEDIA_ROOT=/DATA/${SERVICE_NAME}
DOMAIN=${SERVICE_NAME}.pik-software.ru

if [[ -z "$HOST" ]]; then
    echo "Use: $0 <HOST>"
    exit 1
fi
if [[ -z "$SERVICE_NAME" ]]; then
    echo "Use: $0 $HOST <SERVICE_NAME>"
    exit 1
fi

if ssh -p ${PORT} dokku@${HOST} -C apps:list | grep -qFx ${SERVICE_NAME}; then
    echo "App ${SERVICE_NAME} is already exists on ${HOST}";
    exit 2
fi

SECRET_KEY=$( openssl rand -base64 18 )

ssh -p ${PORT} ${HOST} -C dokku events:on
ssh -p ${PORT} ${HOST} -C dokku apps:create ${SERVICE_NAME}
ssh -p ${PORT} dokku@${HOST} -C storage:mount ${SERVICE_NAME} "${MEDIA_ROOT}:${MEDIA_ROOT}"
ssh -p ${PORT} dokku@${HOST} -C domains:set ${SERVICE_NAME} ${DOMAIN}

## postgres (root required!)
ssh -p ${PORT} ${HOST} -C POSTGRES_IMAGE="postgres" POSTGRES_IMAGE_VERSION="13" dokku postgres:create ${SERVICE_NAME}
ssh -p ${PORT} dokku@${HOST} -C postgres:link ${SERVICE_NAME} ${SERVICE_NAME}

## redis
ssh -p ${PORT} dokku@${HOST} -C redis:create ${SERVICE_NAME}
ssh -p ${PORT} dokku@${HOST} -C redis:link ${SERVICE_NAME} ${SERVICE_NAME}

# CONFIGS

# base
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} SERVICE_NAME=${SERVICE_NAME}
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} DOKKU_APP_TYPE=dockerfile
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} SECRET_KEY=${SECRET_KEY}
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} MEDIA_ROOT=${MEDIA_ROOT}

# environment
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} ENVIRONMENT=staging

# OPTIONS
ssh -p ${PORT} dokku@${HOST} -C ps:set-restart-policy ${SERVICE_NAME} always
ssh -p ${PORT} dokku@${HOST} -C ps:scale ${SERVICE_NAME} web=1 beat=1 worker=1
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} DOKKU_DEFAULT_CHECKS_WAIT=5
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} DOKKU_WAIT_TO_RETIRE=60
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} DOKKU_DOCKER_STOP_TIMEOUT=600

# LIMITS
ssh -p ${PORT} dokku@${HOST} -C limit:set --no-restart ${SERVICE_NAME} web memory=1Gb cpu=100
ssh -p ${PORT} dokku@${HOST} -C limit:set --no-restart ${SERVICE_NAME} beat memory=1Gb cpu=100
ssh -p ${PORT} dokku@${HOST} -C limit:set --no-restart ${SERVICE_NAME} worker memory=1Gb cpu=100
