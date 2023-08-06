#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=tql2gpu
fi;

password=xiaomi
cloudml dev create -n $name -p $password \
--priority_class guaranteed \
-d cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:33103tql2dev  \
-cm rw \
-c 32 -M 32G \
-g 1 -gt v100 -gm 32g # [u\'v100-32g\', u\'t4-16g\', u\'p4-8g\', u\'v100-16g\']