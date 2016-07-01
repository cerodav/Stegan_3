# Stegan_3
Hiding data in plain sight :P

Requirements :
cImage
`pip install cImage`
libjpeg-dev
`sudo apt-get install libjpeg-dev`
libjpeg8-dev (Required if Ubuntu 14.04) 
`sudo apt-get install libjpeg8-dev`
re-install pillow
`pip install --no-cache-dir -I pillow`

What it does ?

Hiding data in plain sight, i.e given a text document it hides the text within a given specified image file, to finally produce a .png file that has no loss in visual fidelity (negligible) but at the same time holds the text information in it.

Want to test ?

Try this to encode : `python SteganEncoder.py ./Test/messi.jpg ./Test/text.txt ./Test/messi_stegan.png`
Try this to decode : `python SteganDecoder.py ./messi_stegan.png`
