#!/bin/bash

export BASEPATH="/var/lib/dockerssh/resources"
export SCRIPTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PLATFORM=$1

echo "BASEPATH=$BASEPATH"
echo "SCRIPTPATH=$SCRIPTPATH"
echo "PLATFORM=$PLATFORM"

if [[ -z $PLATFORM ]]; then
    echo "require platform."
    exit
fi

mkdir -p $BASEPATH
cd $BASEPATH

if [[ $EUID -eq 0 ]]; then
    echo "script run with root permission."
else
    echo "script run without root permission."
    exit
fi

if command -v docker &>/dev/null; then
    echo "docker already install."
else
    echo "docker not install."
    exit 
fi

if command -v git &>/dev/null; then
    echo "git already install."
else
    echo "git not install."
    exit 
fi

export DROPBEAR_BUILDPATH="$BASEPATH/$PLATFORM"
echo "DROPBEAR_BUILDPATH=$DROPBEAR_BUILDPATH"
mkdir -p "$DROPBEAR_BUILDPATH"
cd "$DROPBEAR_BUILDPATH"
cp "$SCRIPTPATH"/scripts/* "$DROPBEAR_BUILDPATH"
cp "$SCRIPTPATH/docker/Dockerfile" "$DROPBEAR_BUILDPATH/Dockerfile"
git clone https://github.com/mkj/dropbear.git --depth 1
docker build --platform $PLATFORM -t dockerssh-build .
docker run --platform $PLATFORM -it --rm -v "$DROPBEAR_BUILDPATH:/build" dockerssh-build sh build.sh
cp "$SCRIPTPATH"/public/* "$DROPBEAR_BUILDPATH/out"
