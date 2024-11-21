#!/usr/bin/env bash

# A Modified version of the original script availible at:
#   https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
#  Modifications: 
#   - switchted to podman
#   - changed the docker image to a build that runs on ppc64le
#   - parametrised the script for usage in ansible scripts.
#
#   Usage: standalone_embed_ppc64le.sh start|stop|delete [-m MILVUSPORT] [-e ETCDPORT]
#
#
# Original Copyright Notice: 
#
# Licensed to the LF AI & Data foundation under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

milvus_port=19530
etcd_port=2379
container_util=podman

run_embed() {
    cat << EOF > embedEtcd.yaml
listen-client-urls: http://0.0.0.0:2379
advertise-client-urls: http://0.0.0.0:2379
quota-backend-bytes: 4294967296
auto-compaction-mode: revision
auto-compaction-retention: '1000'
EOF

    ${container_util} run -d \
        --name milvus-standalone \
        --security-opt seccomp:unconfined \
        -e ETCD_USE_EMBED=true \
        -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
        -e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml \
        -e COMMON_STORAGETYPE=local \
        -v $(pwd)/volumes/milvus:/var/lib/milvus \
        -v $(pwd)/embedEtcd.yaml:/milvus/configs/embedEtcd.yaml \
        -p ${milvus_port:-19530}:19530 \
        -p 9091:9091 \
        -p ${etcd_port:-2379}:2379 \
        --health-cmd="curl -f http://localhost:9091/healthz" \
        --health-interval=30s \
        --health-start-period=90s \
        --health-timeout=20s \
        --health-retries=3 \
        quay.io/mgiessing/milvus:v2.3.1 \
        milvus run standalone  1> /dev/null
}

wait_for_milvus_running() {
    echo "Wait for Milvus Starting..."
    while true
    do
        res=`${container_util} ps|grep milvus-standalone|grep healthy|wc -l`
        if [ $res -eq 1 ]
        then
            echo "Start successfully."
            break
        fi
        sleep 1
    done
}

start() {
    res=`${container_util} ps|grep milvus-standalone|grep healthy|wc -l`
    if [ $res -eq 1 ]
    then
        echo "Milvus is running."
        exit 0
    fi

    res=`${container_util} ps -a|grep milvus-standalone|wc -l`
    if [ $res -eq 1 ]
    then
        ${container_util} start milvus-standalone 1> /dev/null
    else
        mkdir -p $(pwd)/volumes/milvus
        run_embed
    fi

    if [ $? -ne 0 ]
    then
        echo "Start failed."
        exit 1
    fi

    wait_for_milvus_running
}

stop() {
    ${container_util} stop milvus-standalone 1> /dev/null

    if [ $? -ne 0 ]
    then
        echo "Stop failed."
        exit 1
    fi
    echo "Stop successfully."

}

delete() {
    res=`${container_util}  ps|grep milvus-standalone|wc -l`
    if [ $res -eq 1 ]
    then
        echo "Please stop Milvus service before delete."
        exit 1
    fi
    ${container_util} rm milvus-standalone 1> /dev/null
    if [ $? -ne 0 ]
    then
        echo "Delete failed."
        exit 1
    fi
    sudo rm -rf $(pwd)/volumes
    sudo rm -rf $(pwd)/embedEtcd.yaml
    echo "Delete successfully."
}

status() {
    res=`${container_util} ps|grep milvus-standalone|wc -l`
    if [ $res -eq 1 ]
    then
        echo "running." 
        exit 0
    else
        echo "not running." 
        exit 1
    fi
    
}

op=$1
shift 1
while getopts "e:m:c:" flag;
do 
    case "${flag}" in
        m) milvus_port=${OPTARG};;
        e) etcd_port=${OPTARG};;
        c) container_util=${OPTARG};;
        \?)
            echo "Invalid argument! Use -e for the etcd port, -m for the milvus port, -c podman|docker to use podman (default) or docker."
            exit 1
            ;;
    esac
done


case $op in
    start)
        start
        ;;
    stop)
        stop
        ;;
    delete)
        delete
        ;;
    status)
        status
        ;;
    *)
        echo "please use bash standalone_embed_ppc64le.sh start|stop|delete|status [-e ETCD_PORT] [-m MILVUS_PORT] [-c podman|docker]"
        ;;
esac