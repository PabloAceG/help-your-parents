""" This module implements an image convertor to PDF files.

After converting the images to PDF, all the images in the same folder are 
compressed to a ZIP file.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Pablo Acereda García"
__authors__ = ["Pablo Acereda García"]
__contact__ = "p.aceredag@gmail.com"
__copyright__ = "Copyright 2020"
__credits__ = ["Pablo Acereda García"]
__date__ = "2020/04/09"
__deprecated__ = False
__email__ =  "p.aceredag@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Pablo Acereda García"
__status__ = "Development"
__version__ = "0.0.1"

import pdfminer
import sys
import os

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout    import LAParams
from pdfminer.pdfpage   import PDFPage

#from pdfminer import extract_text

"""
    Ask for where the file is being executed.
    If it is not being executed from where the folder to be transformed are,
    it allows the user to insert the path.
    Inputs:
    Outputs:
        - path: location from where the folder containing the files are.
"""
def ask_for_location ():
    text = "Are you executing this from the same directory that has the PDF \
file with the links to download? (y/n) "
    in_directory = input (text)

    valid_path = False 
    
    path = ""

    while not valid_path:
        try:
            if   ( in_directory == "y" ):
                print ("Continuing...", end="\n")

                valid_path = True

                path = os.getcwd().replace("\\", "/")
            elif ( in_directory == "n" ):
                correct_path = False
                
                # Logging message 
                print ("I need the path then...", end="\n\n")

                while not correct_path:
                    # Ask for path to user
                    path = input (
                        "Where is the folder that contains such PDF? "
                    )
                    
                    # Valid path?
                    if (os.path.isdir (path)):
                        print ("Continuing...", end="\n")
                        correct_path = True
                        valid_path = True
                
            else:
                print ("Not valid input", end="\n")
        except:
            print ("An error ocurred, try again", end="\n")

    return path + "/"

"""
    Ask for the name of a file, checking if it exists within a path.
    If it is not being executed from where the folder to be transformed are,
    it allows the user to insert the path.
    Inputs:
        - path: file's location.
    Outputs:
        - name: name of the file.
"""
# TODO: Add code to include the .pdf at the end of the name
def ask_for_name_file(path):
    valid_name = False 

    name = ""

    while not valid_name:
        try:
            question = 'What is the name of the file? (without the .pdf) '
            name = input(question)

            file_exists = os.path.isfile(path + name)

            if file_exists:
                valid_name = True
            else:
                print (
                    'The file you specified does not exists. Try again.', 
                    end="\n"
                )
        except:
            print ("An error ocurred, try again", end="\n")

    return name

"""
    Transforms the content of the PDF to text, so that its content can be 
    filtered later on.
    Inputs:
        - path: file's location.
        - name: name of the file.
    Outputs:
        - text: content of the PDF file on String format.
"""
def convert_to_text(path, name, pages=None):
    # Content of the PDF
    text = ""

    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    # Going to store the PDF
    output = StringIO()

    # Input Streams
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    # File and permissions
    infile = open(path + name, 'rb')

    # Reads pages of the PDF
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    
    # Transforms content to String
    text = output.getvalue()

    # Closes input streams
    infile.close()
    converter.close()
    output.close()
    
    '''
    try:
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        # Going to store the PDF
        output = StringIO()

        # Input Streams
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        # File and permissions
        infile = open(path + name, 'rb')

        # Reads pages of the PDF
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        
        # Transforms content to String
        text = output.getvalue()

        # Closes input streams
        infile.close()
        converter.close()
        output.close()
    
    except:
        print('An unexpected error ocurred!')
        sys.exit
    '''
    return text

"""
Main class execution
"""
if __name__ == "__main__":

    print('\n')
    print('Starting download!')
    print('============================================================\n\n')

    # Location for the file with the links to download
    path = ask_for_location()
    # File name
    name = ask_for_name_file(path)

    # Convert PDF to text to it can be filtered
    text = convert_to_text(path, name)

    