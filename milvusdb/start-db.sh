#!/bin/bash

podman volume create --ignore milvus_data

exec podman run -d \
		--name milvus \
		--security-opt seccomp:unconfined \
		-e ETCD_USE_EMBED=true \
		-e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml \
		-e COMMON_STORAGETYPE=local \
		-v milvus_data:/var/lib/milvus \
		-v ./embedEtcd.yaml:/milvus/configs/embedEtcd.yaml:ro \
		-p 19530:19530 \
        	-p 9091:9091 \
        	-p 2379:2379 \
		--health-cmd="curl -f http://localhost:9091/healthz" \
		--health-interval=30s \
		--health-start-period=90s \
		--health-timeout=20s \
		--health-retries=3 \
	        docker.io/milvusdb/milvus:v2.4.8 \
		milvus run standalone
