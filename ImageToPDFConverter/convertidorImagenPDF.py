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

import os
import zipfile

from os       import listdir
from os.path  import isfile, join
from PIL      import Image
from datetime import date

"""
    Welcome message to guide the user and ask for when the file is being
    executed.
    Inputs:
    Outputs:
        - Call to function that collects necessary information for the program.
"""
def welcome_message ():
    print ("Hola buenaaaas!!", end="\n")
    print (
        "Imagino que querrás transformar unas cuantas imágenes para ", 
        "mandarlas por correo. Si es así necesito preguntarte lo siguiente:",
        end="\n\n"
    )

    return ask_for_location ()

"""
    Ask for where the file is being executed.
    If it is not being executed from where the folder to be transformed are,
    it allows the user to insert the path.
    Inputs:
    Outputs:
        - path: location from where the folder containing the files are.
"""
def ask_for_location ():
    text = "¿Está el archivo que estás ejecutando en el mismo lugar que \
las carpetas con los ficheros que quieres convertir a PDF? (s/n) "
    in_directory = input (text)

    valid_path = False 
    
    path = ""

    while not valid_path:
        try:
            if   ( in_directory == "s" ):
                print ("Perfecto!!", end="\n")

                valid_path = True

                path = os.getcwd().replace("\\", "/")
            elif ( in_directory == "n" ):
                correct_path = False
                
                while not correct_path:
                    # Logging message 
                    print ("Voy a tener que pedirte algo más...", end="\n\n")
                    # Ask for path to user
                    path = input (
                        "¿Dónde se encuentran las carpetas de las que vamos ",
                        "a transformar luego las imágenes a PDF?"
                    )
                    # Logging message
                    print (
                        "\nEstoy buscando si la ruta es correcta...", 
                        end="\n"
                    )
                    
                    # Valid path?
                    if (os.path.isdir (path)):
                        print ("Perfecto!!", end="\n")
                        correct_path = True
                
            else:
                print ("Not valid input", end="\n")
        except:
            print ("Ha ocurrido un error, vuelve a intentarlo", end="\n")

    return path + "/"

"""
    Folders that the user want to get as transformed.
    Inputs:
    Outputs:
"""
def folders_to_transform ():
    number_folders = 0
    folders = [ ]

    # How many folders are going to be converted
    correct_number_folders = False
    while not correct_number_folders:
        try:
            number_folders = input (
                "¿Cuántas carpetas contienen imágenes para transformar?\n"
            )

            number_folders = int (number_folders)
            correct_number_folders = True
        except:
            print ("Parece que no has escrito lo que deberías...", end="\n")


    # Ask for folders
    i = 0
    while i < number_folders:
        try:
            new_folder = input ( \
                "Dime el nombre de la {}º carpeta\n"
                    .format (i + 1)
            )

            folders.append(new_folder + "/")
            i += 1
        except:
            print (" No parece un nombre muy válido...")

    return folders

""" 
    Print the current working directory.
    Inputs:
        - path: where to find the files.
    Outputs:
"""
def print_directory (path):
    print(end="\n")
    print("==============================", end="\n")
    print("Directorio actual: ")
    print(path, end="\n")
    print("==============================", end="\n")
    print(end="\n")

"""
    Print the moving to dir
    Inputs:
        - path: where to find the files.
    Outputs:
"""
def print_move_to_path (path):
    print(end="\n")
    print("--------------------", end="\n")
    print("Moviendose al directorio ", path, end="\n")
    print("--------------------", end="\n")
    print(end="\n")

"""
    Retrieves and prints the name of the files for a given directory.
    Inputs:
        - path: where to find the files.
    Outputs:
        - files: Array containing the files in the specified path (non 
            recursive).
"""
def get_files_names_directory (path):
    # Retrive files from path
    files = [ f for f in listdir (path) 
                if isfile ( join (path, f) )
            ]

    # Print files
    print ("Se han encontrado los ficheros: ", end="\n\n")
    for f in files:
        print(f, end="\n")

    print ("##############################", end="\n\n")

    return files

"""
    Transforms Image files to a PDFs.
    Inputs:
        - path: where to find the files.
        - files: images to be converted to PDF files.
    Outputs:
"""
def transform_file_to_pdf (path, files):
    for f in files:
        file_format          = f[len (f) - 3 : ].lower ()
        file_format_extended = f[len (f) - 4 : ].lower ()
        if file_format in ( "bmp", "jpg", "gif", "png") or \
           file_format_extended in ( "jpeg", "jfif", "tiff" ):
            #Log message
            print ("Transformando fichero {}".format (f), end="\n")

            # Path to the file
            path_to_file = path + f
            # Transformation Image to PDF
            image     = Image.open (path_to_file)
            image_rgb = image.convert ('RGB')
            image_rgb.save (path_to_file[ 0 : len (path_to_file) - 3] + "pdf")
            
            # Remove image to only leave the PDF
            os.remove (path_to_file)
        else:
            print (
                "El fichero {} no ha sido incluido, no es una imagen."
                    .format (f),
                end="\n" 
            )
            print ("format: {}".format (file_format))
            print ("format: {}".format (file_format_extended))

    
    print (
        "Transformación completa de los ficheros en la ruta {}"
            .format (path)
    )

"""
    Comprosses the PDF files containing the images into a ZIP file named after
    the directory contining the files and the current date.
    Inputs:
        - path: where to find the files.
        - files: images to be converted to PDF files.
    Outputs:
"""
def compress_to_zip (path, files):
    directory = path.split("/")
    directory = directory [len (directory) - 2]
    filename = directory + "_" + str (date.today ()) + ".zip"
    zip_file = zipfile.ZipFile (filename, 'w')

    for f in files:
        file_format = f[len (f) - 3 : ].lower ()
        if file_format == "pdf":
            #Log message
            print ("Añadiendo {} al comprimido ".format (f), end="\n")

            # Path to the file
            path_to_file = directory + "/"+ f
            # Add file to ZIP file
            zip_file.write(path_to_file, compress_type=zipfile.ZIP_DEFLATED)

            # Remove image to only leave the PDF
            os.remove (path_to_file)

    # Write the contents of the file    
    zip_file.close ()

    # Move file to folder
    origin_path      = "./" + filename
    destination_path = path + filename
    os.rename (origin_path, destination_path)

    # Loggin message
    print ("Fichero comprimido {} creado".format (filename))
        
"""
    Main class execution.
"""
if __name__ == "__main__":
    father_directory = welcome_message ()
    folders = folders_to_transform ()

    print_directory (father_directory)

    ### Conversion from files in each directory
    for directory in folders:
        # Path in which conversion takes place
        current_directory = father_directory + directory
        print_move_to_path (current_directory)

        # Files to be converted
        files = get_files_names_directory (current_directory)
        # Transformation of files
        transform_file_to_pdf (current_directory, files)

        # Files to be converted
        files = get_files_names_directory (current_directory)
        # Create a compress file
        compress_to_zip (current_directory, files)
