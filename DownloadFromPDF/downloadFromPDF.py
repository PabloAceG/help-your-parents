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
import requests # Make URL request
import wget # Download files

import configparser # Get configuration

from io import StringIO
# PDF to text
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout    import LAParams
from pdfminer.pdfpage   import PDFPage
from urlextract import URLExtract # Extract URL from Text

"""
    Uses the configuration.
    Inputs:
    Outputs:
        - path: files location.
        - files: name of each file.
"""
def use_conf_file():
    text = "Do you want to use the configuration file (parameters.conf)? (y/n) "
    use_it = input (text)

    valid_answer = False 
    
    path = ""
    files = ""

    while not valid_answer:
        try:
            if   ( use_it == "y" ):
                config = configparser.ConfigParser()
                config.read('./conf.ini')

                path  = config.get('Location', 'path')
                files = config.get('Location', 'files_to_read').split("\n")

                valid_answer = True

            elif ( use_it == "n" ):
                
                # Location for the file with the links to download
                path = ask_for_location()
                # File name
                files = ask_for_files_name(path)

                valid_answer = True
                
            else:
                print ("Not valid input", end="\n")
        except:
            print ("An error ocurred, try again", end="\n")

    return path + '/', files

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

    return path

"""
    Ask for the name of file, checking if they exist within a path.
    If it is not being executed from where the folder to be transformed are,
    it allows the user to insert a new path.
    Inputs:
        - path: files location.
    Outputs:
        - files: name of each file.
"""
def ask_for_files_name(path):

    name = ""

    num_files = 0
    files = [ ]

    # How many folders are going to be converted
    correct_number_folders = False

    # Ask for number of files to read
    while not correct_number_folders:
        try:
            question = 'How many files in the same path contain links to download? '
            num_files = input (question)
            num_files = int (num_files)

            correct_number_folders = True
        except:
            print ('Please write a number', end="\n")

    # Ask for the name of those files. Also check they exists.
    num_files_name = 0

    while num_files_name < num_files:
        try:
            question = 'What is the name of the file? '
            name = input(question)

            file_exists = os.path.isfile(path + name)

            if file_exists:
                num_files_name += 1

                files += [name]
            else:
                print (
                    'The file you specified does not exists. Try again.', 
                    end="\n"
                )
        except:
            print ("An error ocurred, try again", end="\n")

    return files

"""
    Transforms the content of the PDFs to text, so that its content can be 
    filtered later on.
    Inputs:
        - path: files location.
        - files: name of each file.
    Outputs:
        - files_conent: content of each PDF file on String format.
"""
def convert_to_text(path, files):
    # PDF content
    files_content = [ ]

    try:
        # Going to store the PDF
        output = StringIO()

        # Input Streams
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        # Extracts text from all files
        for name in files:
            try:
                # Number of pages    
                pagenums = set()

                # File and permissions
                infile = open(path + name, 'rb')

                # Reads pages of the PDF
                for page in PDFPage.get_pages(infile, pagenums):
                    interpreter.process_page(page)
                
                # Transforms content to String
                files_content += [output.getvalue()]
            except:
                print(
                    'An error ocurred parsing {}. Skipping to next file!'
                        .format(name)
                )

        # Closes input streams
        infile.close()
        converter.close()
        output.close()
    
    except:
        print('An unexpected error ocurred!')
        sys.exit

    return files_content

"""
    Extracts the URLS from the PDFs' text.
    Inputs:
        - files_content: content of the PDF file on String format.
    Outputs:
        - urls: Array containing the URLs from each text.
"""
def extract_urls(files_content):
    urls = [ ]

    # Extracts URLS for each file's content
    for text in files_content:
        extractor = URLExtract()
        urls += [extractor.find_urls(text)]

    return urls

"""
Main class execution
"""
if __name__ == "__main__":

    print('\n')
    print('Starting download!')
    print('============================================================\n\n')

    # Path and files with the links to download. Posibility of using 
    # configuration file instead of writing data.
    path, files = use_conf_file()

    # Convert PDF to text to it can be filtered
    files_content = convert_to_text(path, files)

    # Extrat URLs from text
    urls = extract_urls(files_content)

    
    