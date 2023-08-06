#!/usr/bin/env bash
cloudml quota_v2 update -p guaranteed -c 32 -M 64G -e yuanjie@xiaomi.com \
-g 1 \
-gt v100

cloudml quota_v2 update -p guaranteed \
-g 3 -c 100 -M 128 \
-e yuanjie@xiaomi.com

cloudml quota_v2 update -p guaranteed \
-g 1 -c 8 -M 30 \
-gt v100-16g -gt p4-8g \
-gc 1 -gc 2 \
-e yuanjie@xiaomi.com



