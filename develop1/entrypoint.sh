#!/bin/bash
set -e
eval $(ssh-agent -s)
ssh-add /root/.ssh/dev1
exec "$@"
