#!/bin/bash
export PYTHONPATH=./src
# pass in a string to run a subset of tests
# i.e.
#   ./_test.sh download
#   ./_test.sh "not download"
MARKER=$1

if [ -z "$MARKER" ]
then
  pytest -s ./tests
else
  pytest -s ./tests -m "$MARKER"
fi
