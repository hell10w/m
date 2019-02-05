#!/bin/bash

(
  flock -n 9 || exit 1

  echo "MAIL"
  offlineimap

) 9>/tmp/.check-mail.lock
