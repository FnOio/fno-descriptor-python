#!/bin/bash

function printBanner() {
    echo "---------------------------------------------------------------------"
}
echo "🔎 $(date) SHACL VALIDATION"

SHACL_SHAPE='./shapes/parameter.ttl'
SHACL_INPUT='./partial_fno_descriptions/parameters.ttl'
echo "👉 $SHACL_SHAPE"
echo "📃 $SHACL_INPUT"
shacl v --data $SHACL_INPUT --shapes $SHACL_SHAPE
printBanner;

SHACL_SHAPE='./shapes/output.ttl'
SHACL_INPUT='./partial_fno_descriptions/output.ttl'
echo "👉 $SHACL_SHAPE"
echo "📃 $SHACL_INPUT"
shacl v --data $SHACL_INPUT --shapes $SHACL_SHAPE
printBanner;
