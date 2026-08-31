#!/bin/zsh

export BASEPATH="$HOME/Library/Application Support/dockerssh/server"
export SCRIPTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PLATFORM=$1
export LIBC=$2

echo "BASEPATH=$BASEPATH"
echo "SCRIPTPATH=$SCRIPTPATH"
echo "PLATFORM=$PLATFORM"
echo "LIBC=$LIBC"

if [[ ! -n $PLATFORM || ! -n $LIBC ]]; then
    echo "require platform and libc."
    exit
fi

mkdir -p "$BASEPATH"
cd "$BASEPATH"

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

if [[ -f $SCRIPTPATH/docker/$LIBC ]]; then
    export DROPBEAR_BUILDPATH="$BASEPATH/$PLATFORM/$LIBC"
    echo "DROPBEAR_BUILDPATH=$BASEPATH/$PLATFORM/$LIBC"
    if [ -e "$DROPBEAR_BUILDPATH" ]; then
        rm -rf "$DROPBEAR_BUILDPATH"
        echo remove "$DROPBEAR_BUILDPATH"
    fi
    mkdir -p "$DROPBEAR_BUILDPATH"
    cd "$DROPBEAR_BUILDPATH"
    cp "$SCRIPTPATH"/scripts/* "$DROPBEAR_BUILDPATH"
    cp "$SCRIPTPATH/docker/$LIBC" "$DROPBEAR_BUILDPATH/Dockerfile"
    git clone https://github.com/mkj/dropbear.git --depth 1
    docker build --platform $PLATFORM -t dockerssh-build-$LIBC .
    docker run --platform $PLATFORM -it --rm -v "$DROPBEAR_BUILDPATH:/build" dockerssh-build-$LIBC bash build.sh
    cp "$SCRIPTPATH"/public/* "$DROPBEAR_BUILDPATH/out"
else
    echo "dockerfile $LIBC not found."
    exit
fi
