#!/usr/bin/env bash
# @Project      : tql-cloudml
# @Time         : 2019-06-10 19:19
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

docker rmi # 删除镜像
docker image prune # 清空镜像

docker container ls -a
docker rm # 删除容器
docker container prune -f # 清空容器

docker pull cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:1.13.1-xm1.0.0-zjyprc-hadoop-py3

docker run -it --rm --name tql-ml 93b bash

docker commit  -a 'yuanjie' -m 'ml tools' --change='CMD /prepare_dev.py && /run_jupyter.sh' tql-ml cr.d.xiaomi.net/yuanjie/tql-ml:v1


docker run -it --rm --name ann milvusdb/milvus:cpu-latest bash

ContainerID=930
ImageName=milvus-admin:0.7.0
docker commit  -a 'yuanjie' -m 'ann' $ContainerID cr.d.xiaomi.net/yuanjie/$ImageName
docker push cr.d.xiaomi.net/yuanjie/$ImageName




