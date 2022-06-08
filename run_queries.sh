#!/bin/bash
QUERY=count_violations.rq
DATA=function_description.ttl
sparql --query=$QUERY --data=$DATA