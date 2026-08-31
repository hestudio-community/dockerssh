#!/bin/bash

export DROPBEAR_BUILDPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd $DROPBEAR_BUILDPATH
echo "DROPBEAR_BUILDPATH=$DROPBEAR_BUILDPATH"

cd $DROPBEAR_BUILDPATH/dropbear
./configure --disable-zlib
make STATIC=1

cd $DROPBEAR_BUILDPATH
export DROPBEAR_OUT=$DROPBEAR_BUILDPATH/out
echo "DROPBEAR_OUT=$DROPBEAR_OUT"
mkdir -p $DROPBEAR_OUT
cp $DROPBEAR_BUILDPATH/dropbear/dropbear $DROPBEAR_OUT
cp $DROPBEAR_BUILDPATH/dropbear/dropbearconvert $DROPBEAR_OUT
cp $DROPBEAR_BUILDPATH/dropbear/dropbearkey $DROPBEAR_OUT
