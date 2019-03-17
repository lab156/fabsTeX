#!/bin/bash

# TODO: 1. Comment out tikz(-cd), epstopdf imports. 
#       2. Add \labels to the TeX document as mentioned in the README. 
# echo "Make a WEB directory"
# mkdir WEB
# cd WEB

echo "Assign tags and place them in 'tags'..."
python tagger.py >> tags

echo "Get processed TeX file..."
python labeller.py >> stacks.tex

echo "Run plasTeX on it..."
plastex --renderer=Gerby fsg.tex

# echo "Compile LaTeX..."
# pdftex stacks.tex

mv tags stacks.tags

echo "Install gerby-website..."
git clone https://github.com/gerby-project/gerby-website.git
cd gerby-website/gerby/static || exit
echo "Installing CSS..."
git clone https://github.com/aexmachina/jquery-bonsai
cp jquery-bonsai/jquery.bonsai.css css/
# echo "Move to gerby/tools/."
cd ../../gerby/tools || exit
#pip install .

# echo"Setting up softlinks."
ln -s ../../../fsg stacks
ln -s ../../../fsg.paux stacks.paux
ln -s ../../../stacks.tags stacks.tags
# ln -s ../../../stacks.pdf stacks.pdf
echo "Run the update file."
python update.py

mv *.sqlite ../../
cd ../../ || exit

export FLASK_APP=gerby
flask run 
