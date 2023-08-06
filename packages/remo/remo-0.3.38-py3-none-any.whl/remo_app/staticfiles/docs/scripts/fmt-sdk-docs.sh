#!/usr/bin/env bash
src=$1

for entry in "$src"/*.md
do
  ."$(PWD)"/fmt "$entry" "$entry"
done
