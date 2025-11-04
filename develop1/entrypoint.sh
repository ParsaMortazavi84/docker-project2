#!/bin/bash
set -e
eval $(ssh-agent -s)
ssh-add /root/.ssh/dev1
<<<<<<< HEAD
=======

>>>>>>> v2.0
exec "$@"
