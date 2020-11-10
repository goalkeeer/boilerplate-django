#!/bin/sh

set -ex

cd "$(dirname "$0")"
echo "$(date +%Y-%m-%d-%H-%M-%S) - deploy $*"

HOST=$1
PORT=$2
REPO=$3
BRANCH=$4

escape (){
    echo "$1" | tr A-Z a-z | sed "s/[^a-z0-9]/-/g" | sed "s/^-+\|-+$//g"
}

REPO=$( escape ${REPO} )
BRANCH=$( escape ${BRANCH} )

SERVICE_NAME="${REPO}-${BRANCH}"

if [ "${BRANCH}" = "master" ]; then
  SERVICE_NAME="${REPO}"
fi

echo "DEPLOING $SERVICE_NAME"

RELEASE_DATE=$( date '+%Y-%m-%d-%H-%M-%S' )
GIT_REV="$(git rev-parse HEAD)"
ssh -p ${PORT} dokku@${HOST} -C domains:report ${SERVICE_NAME}
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} RELEASE_DATE="'"${RELEASE_DATE}"'"
ssh -p ${PORT} dokku@${HOST} -C config:set --no-restart ${SERVICE_NAME} GIT_REV=${GIT_REV}
git push --force ssh://dokku@${HOST}:${PORT}/${SERVICE_NAME} ${GIT_REV}:refs/heads/master

echo "open !!! http://${SERVICE_NAME}.pik-software.ru/"

