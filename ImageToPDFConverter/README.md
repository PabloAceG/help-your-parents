# Converter Image to PDF

### Introduction 

First of all, allow me to execuse myself for using multiple languages, but I'm 
used to writing code in English, but my parents only know Spanish.

Lots of days they have to scan many documents and send them via email but, as 
it seems, some of the receivers couldn't open de images (`.BMP` files, I don't 
know why they couldn't either, don't ask me). Anyways, my they don't know how 
to convert an image to a PDF... so I thought... why not?

![](https://github.com/PabloAceG/help-your-parents/blob/master/ImageToPDFConverter/images/computer.jpg)

### Prerequisites

You need to have installed:
- [Python](https://www.python.org/downloads/) - I use the 3.7, son anything 
after that should do.
- [Python Pillow](https://python-pillow.org/) - run `pip install Pillow` on 
your command shell (`Bash`, `Cmd`, ...) after having Python installed. 

![](https://github.com/PabloAceG/help-your-parents/blob/master/ImageToPDFConverter/images/pillow.jpg)

### How does it work?

To make it simple:
1. You give the folders that contain the images.
2. It transforms the images to PDFs and deletes the images (in my case I need 
it not to create too much garbage) - delete it if you need to).
3. Compresses the files into a `.ZIP` file to that it is easier to send it
via email and once again it deletes the garbage files.
4. There is no 4, this is just to make this a little bit longer, but you're 
done.

### How to run it

1. Place this file where your folders that contain your images are (it's the 
simplest way, you can also insert the path to those folders manually, but it's
slower).
2. Run `python convertidorImagenPDF.py`.
3. Follow the steps.

![](https://github.com/PabloAceG/help-your-parents/blob/master/ImageToPDFConverter/images/done.jpg)