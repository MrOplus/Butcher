#!/bin/sh

/usr/bin/python3 /butcher/Butcher/main.py
status=$?
if [ $status -ne 0 ]; then
  echo "unable to start butcher! : $status"
  exit $status
fi