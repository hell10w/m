#!/bin/bash

TIMEOUT=90

while true; do
  /scripts/check-mail.sh
  /scripts/check-rss.sh

  echo
  echo
  echo "----------------------------------------------------"
  sleep $TIMEOUT
  echo
  echo

done
