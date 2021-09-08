#!/bin/zsh

LOCAL_PYTHON="/usr/bin/env python3"
BUILD_DIR=./dist
BUILD_OUT=${BUILD_DIR}/meecxprofile

if [ ! -d ${BUILD_DIR} ]; then
    mkdir -p ${BUILD_DIR}
fi

# To provide your own python path, just add '--python=/path/to/python' after './build'
# For example: ./build.sh --python="/usr/bin/env python3.7"
# or           ./build.sh --python="/usr/local/munki/python"
if [[ ! -z ${1} ]]; then
    DIST_CMD=$(echo /usr/local/bin/python3 -m zipapp src --compress --output ${BUILD_OUT} ${1})
else
    DIST_CMD=$(echo /usr/local/bin/python3 -m zipapp src --compress --output ${BUILD_OUT} --python=\"${LOCAL_PYTHON}\")
fi

# Clean up
/bin/rm ${BUILD_OUT} &> /dev/null

# Build
eval ${DIST_CMD}
chmod +x ${BUILD_OUT}
