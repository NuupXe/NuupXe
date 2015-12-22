#!/bin/bash

set -x

text=$1
mashapekey=`cat configuration/voicerss.mk`
apikey=`cat configuration/voicerss.ak`

curl -X POST --include "https://voicerss-text-to-speech.p.mashape.com/?key=${apikey}" \
  -H "X-Mashape-Key: ${mashapekey}" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'c=mp3' \
  -d 'f=48khz_16bit_stereo' \
  -d 'hl=es-mx' \
  -d 'r=0' \
  -d "src=${text}" > output/voicerss.sound

mpg123 output/voicerss.sound

# End of File
