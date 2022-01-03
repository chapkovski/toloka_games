#!/bin/bash

filename='.env'

while read -r line
do
  id=$(cut -c-1 <<< "$line")
  if [ $id != '#' ]
  then
    heroku config:set "$line"
  else
    echo line  $line is commented out
  fi
done < "$filename"