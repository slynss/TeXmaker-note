#!/usr/bin/python2.7
#                                                       TeXmaker-note                      
#                                                                  v0.1                                         
#                                                                                                    
#                                   To run, this script needs these packages :                
#	                 pdfcrop (part of TeXlive distribution) , xournal , python and its modules : 
#                           platform ,  os ,  sys ,  gzip ,  subprocess, pyperclip
#                   Please notice that pyperclip is provided in this archive and needs
#                                           to be in the current script directory
#                                                                          
#                                                   GNU Public License v3                           
#                                                                          
#                                        Copyright 2013 - Aurelien PIERRE                     
# https://aurelienpierre.com - aurelien@aurelienpierre.com          
#                                                                          
#                                                                          
# TeXmaker-note  is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by     
# the Free Software Foundation, either version 3 of the License, or          
# (at your option) any later version.                                      
#                                                                                                                               
# This program is distributed in the hope that it will be useful,            
# but WITHOUT ANY WARRANTY; without even the implied warranty of           
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            
# GNU General Public License for more details.                             
#                                                                          
# You should have received a copy of the GNU General Public License      
# along with this program.  If not, see <http://www.gnu.org/licenses/>    

## Loading modules ##
import platform ,  os ,  sys ,  gzip , pyperclip

## Functions ##

# Create img directory if not exists
def CreateDir():
    if not os.path.exists("img"):
        os.makedirs("img")
    
# Create or read index counter of files
def Index():
    while not os.path.isfile(os.path.abspath('img/index')):
        index = open(os.path.abspath("img/index"), "w")
        index.write("1")
        index.close()
    index = open(os.path.abspath("img/index"), "r")
    global i
    i = index.read().strip()
    index.close()
    
# Initial XML file initialization
def WriteXML(i):
    xml = open(os.path.abspath("img/img-%s.xml" % i), "w")
    init = """<?xml version="1.0" standalone="no"?>
    <xournal version="0.4.5">
    <title>Xournal document - see http://math.mit.edu/~auroux/software/xournal/</title>
    <page width="612.00" height="792.00">
    <background type="solid" color="white" style="graph" />
    <layer>
    </layer>
    </page>
    </xournal>"""
    xml.write(init)
    xml.close()

# Initial XML file gzip compression
def GzipXML(i):
    xml = open(os.path.abspath("img/img-%s.xml" % i), "rb")
    xmlgz = gzip.open(os.path.abspath("img/img-%s.xml.gz" % i), "wb")
    xmlgz.writelines(xml)
    xml.close()
    xmlgz.close()
    os.remove(os.path.abspath("img/img-%s.xml" % i))

# Initial xournal file creation
def CreateXOJ (i):
    path_source = os.path.abspath("img/img-%s.xml.gz" % i)
    path_destination = os.path.abspath("img/img-%s.xoj" % i)
    os.rename(path_source, path_destination)
    # Now, a blank initialized Xournal file has been created and is ready to work
    
# Open xournal with our file
def OpenXournal(i):
    path = os.path.abspath("img/img-%s.xoj" % i)
    os.popen("xournal %s" % path, )
    
# Save in PDF
# PDF saving from command line is not available in xournal for now
# You have to type Ctrl + E in Xournal to export in PDF, then Ctrl + S to save and Ctrl + Q to exit the software

# Crop PDF file
def PdfCrop(i):
    path_source = os.path.abspath("img/img-%s.pdf" % i)
    os.popen("pdfcrop --pdftexcmd=pdftex --hires %s" % path_source)
    path_cropped = os.path.abspath("img/img-%s-crop.pdf" % i)
    path_destination = os.path.abspath("img/img-%s.pdf" % i)
    os.rename(path_cropped, path_destination)
    
# Return LaTeX insertion code
def LatexInsert(i):
    # Creating temp file for debugging purpose
    # outpout = open("img/temp-%s.tmp" % i , "w")
    # outpout.write("\includegraphics[scale=1]{img/img-%s.pdf}" % i)
    # outpout.close()
    
    # Copying outpout to clipboard
    path = os.path.abspath("img/img-%s.pdf" % i)
    pyperclip.copy("\includegraphics[scale=1]{%s}" % path)
    # Now the outpout is in your clipboard. You just have to Ctrl + V to paste it where you want.
    # Try to paste automatically (doesn't work in every case)
    spam=pyperclip.paste()
    
# Increment index
def Increment(i):
    i = int(i) +1
    index = open(os.path.abspath("img/index"), "w")
    index.write("%s" %i)
    index.close()

## Programm sequence ##

if __name__ == "__main__":
    CreateDir()
    Index()
    WriteXML(i)
    GzipXML(i)
    CreateXOJ(i)
    OpenXournal(i)
    PdfCrop(i)
    LatexInsert(i)
    Increment(i)
