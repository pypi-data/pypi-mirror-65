#!/usr/bin/env bash
dest=$1
echo "Dest is $dest"

echo "Creating folder $PWD/tmp_doc"
mkdir -p "$PWD"/tmp_doc && cd "$PWD"/tmp_doc
git clone --depth=1 https://github.com/rediscovery-io/remo-python.git
cd remo-python
pip install -r requirements.txt
pip install -r doc/requirements.txt
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


cd ../../../
echo "Deleting folder $PWD/tmp_doc"
rm -rf "$PWD"/tmp_doc
