#!/bin/bash

SAMPLE_RATE=16000

# fetch_youtube_clip(videoID, startTime, endTime)
fetch_youtube_clip() {
  echo "Fetching $1 ($2 to $3)..."
  outname="$1_$2"
  if [ -f "${outname}.wav.gz" ]; then
    echo "File already exists."
    return
  fi

  youtube-dl https://youtube.com/watch?v=$1 \
    --quiet --extract-audio --audio-format wav \
    --output "$outname.%(ext)s"
  if [ $? -eq 0 ]; then
    # If we don't pipe `yes`, ffmpeg seems to steal a
    # character from stdin. I have no idea why.
    yes | ffmpeg -loglevel quiet -i "./$outname.wav" -ar $SAMPLE_RATE \
      -ac 1 -ss "$2" -to "$3" "./${outname}_out.wav"
    mv "./${outname}_out.wav" "./$outname.wav"
    gzip "./$outname.wav"
  else
    sleep 1
  fi
}

grep -E '^[^#]' | while read line
do
  fetch_youtube_clip $(echo "$line" | sed -E 's/, / /g')
done
