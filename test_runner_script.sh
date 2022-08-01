#!/bin/bash

COMMIT=$2

source run_or_fail.sh

run_or_fail "Repository folder not found" pushd $1 1> /dev/null

run_or_fail "Could not clean repository" git clean -f -d -x
run_or_fail "Could not call git pull" git pull
run_or_fail "Could not update to given commit hash" git reset --hard "$COMMIT"