#!/bin/bash

RES_FILE="links.txt"
SEPARATOR="	"

while read line; do
	title=${line%%$SEPARATOR*}
	url=${line##*$SEPARATOR}

	wget -nv --show-progress $url -O "${title}".pdf
done < $RES_FILE
