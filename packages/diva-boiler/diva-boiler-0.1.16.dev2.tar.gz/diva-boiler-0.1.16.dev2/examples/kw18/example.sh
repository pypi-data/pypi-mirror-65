#!/bin/bash

### Video ingest

# ingest a video
boiler video add \
    --video-path ./2018-09-06.08-10-01.08-15-01.alb.G421.mkv \
    --release-batch testing | jq .

# try it again (it will return the same video instance)
boiler video add \
    --video-path ./2018-09-06.08-10-01.08-15-01.alb.G421.mkv \
    --release-batch testing | jq .

### Dispatch to vendor

# dispatch task to vendor
boiler vendor dispatch \
    --name imerit \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --activity-type-list ./activity-type-list.txt \
    --set-name test-set | jq .

# try it again (this will fail)
boiler vendor dispatch \
    --name imerit \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --activity-type-list ./activity-type-list.txt \
    --set-name test-set | jq .

### Upload annotation files

# initial ingest (null -> "annotation", "annotation" -> "audit")
boiler kw18 ingest \
    --types minimal.kw18.types \
    --kw18 minimal.kw18 \
    --txt minimal.txt \
    --regions minimal.kw18.regions \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --vendor-name imerit \
    --activity-type-list activity-type-list.txt | jq .

# try it again (no new status changes)
boiler kw18 ingest \
    --types minimal.kw18.types \
    --kw18 minimal.kw18 \
    --txt minimal.txt \
    --regions minimal.kw18.regions \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --vendor-name imerit \
    --activity-type-list activity-type-list.txt | jq .

# ingest an invalid file ("audit" -> "annotation")
boiler kw18 ingest \
    --types minimal.kw18.types \
    --kw18 invalid.kw18 \
    --txt minimal.txt \
    --regions minimal.kw18.regions \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --vendor-name imerit \
    --activity-type-list activity-type-list.txt | jq .

# ingest a valid file ("annotation" -> "annotation", "annotation" -> "audit")
boiler kw18 ingest \
    --types minimal.kw18.types \
    --kw18 minimal.kw18 \
    --txt minimal.txt \
    --regions minimal.kw18.regions \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --vendor-name imerit \
    --activity-type-list activity-type-list.txt | jq .


### Dispatch annotations to gunrunner
boiler gunrunner dispatch --kw18 minimal \
    --video-name 2018-09-06.08-10-01.08-15-01.alb.G421 \
    --vendor-name imerit \
    --activity-type-list activity-type-list.txt
