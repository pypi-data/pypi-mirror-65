#!/usr/bin/env bash
src=$1
dest=$2
echo "Src is $src"
echo "Dest is $dest"

cd "$src" || exit
make markdown
mkdir -p "$dest"
cp doc/build/markdown/*.md "$dest"

cd examples
jupyter nbconvert intro_to_remo-python.ipynb --to markdown
cp intro_to_remo-python.md "$dest"/../
cp intro_to_remo-python.ipynb "$dest"/../assets

jupyter nbconvert tutorial_upload_annotations.ipynb --to markdown
cp tutorial_upload_annotations.md "$dest"/../
cp tutorial_upload_annotations.ipynb "$dest"/../assets
