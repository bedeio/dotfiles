#!/usr/bin/bash
# Change <YOUR_MAC_ADDRESS> and add or remove the commands in the deepest "if" block as you like.

while read line; do
  if echo $line | grep -q 'Connect Complete'; then
    read line
    if echo $line | grep -q 'Status: Success'; then
      read line
      read line
      if echo $line | grep -q 'EC:23:45:67:ED:F3'; then
        while :; do
          sleep 1
          /home/botelho/bin/key_change.sh
        done
      fi
    fi
  fi
done
