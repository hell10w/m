#!/bin/bash

(
  flock -n 9 || exit 1

  echo "RSS"
  /scripts/subscriptions.py

) 9>/tmp/.check-rss.lock
