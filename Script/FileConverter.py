# File name: FileConvert.py
# Author: L&T
# Date created: 02/24/2017
# Date last modified: 02/24/2017
# Python Version: 2.7


import os
import sys
import csv
import ConfigParser

###################################################################################################
# read_desc_files(descDirectoryPath)
# This function reads the vehicle descriptor files
# input: Descriptor files path
# returns: All the descriptor file names in the directory
###################################################################################################

def read_desc_files(descDirectoryPath):
    fileName = []
    for root, subFolders, files in os.walk(descDirectoryPath):
        for folder in subFolders:
            for file in os.listdir(descDirectoryPath + folder):
                if file.endswith(".txt"):
                    fileName.append(file)
                else:
                    pass
    return fileName

###################################################################################################
# convert_to_dbc(descDirectoryPath, masterDbc, canMatrixPath, outputDirectoryPath)
# This function Generates the vehicle specific dbc from master dbc
# input: Descriptor files path, master dbc file, can matrix path and output files directory path
# returns: None
###################################################################################################

def convert_to_dbc(descDirectoryPath, masterDbc, canMatrixPath, outputDirectoryPath):
    for file in os.listdir(descDirectoryPath):
        if file.endswith(".txt"):
            Messages = []
            with open(descDirectoryPath + "/" + file) as file1:
                for line in file1:
                    line = line.strip() 
                    Messages.append(line)
                    frames = ','.join(Messages)
                vehicleDbcFileName = str(file).split(".txt")[0]
                cmd = "canconvert.exe --frames=" + frames + " " + masterDbc \
                      + " " + outputDirectoryPath + "\\dbc\\" + \
                      vehicleDbcFileName + ".dbc"
                print cmd
                os.chdir(canMatrixPath)
                print os.system(cmd)
    return

###################################################################################################
# convert_to_csv(canMatrixPath, outputDirectoryPath)
# This function Generates the vehicle specific csv files from vehicle specific dbc files
# input: can matrix path and output files directory path
# returns: None
###################################################################################################
                
def convert_to_csv(canMatrixPath, outputDirectoryPath):
    dbcFilesPath = outputDirectoryPath + "\\dbc\\"
    csvFilesPath = outputDirectoryPath + "\\csv\\"
    htmlFilesPath = outputDirectoryPath + "\\html\\"
    for file in os.listdir(dbcFilesPath):
        if file.endswith(".dbc"):
            csvFileName = str(file).split(".dbc")[0]+".csv"
            cmd = "canconvert.exe " + dbcFilesPath + "\\" + str(file) + " " + \
                  csvFilesPath + csvFileName
            print cmd
            os.chdir(canMatrixPath)
            print os.system(cmd)
            htmlFileName = str(file).split(".dbc")[0]+".html"
            convert_to_html(csvFilesPath + csvFileName, htmlFilesPath + \
                            htmlFileName)
            
###################################################################################################
# convert_to_html(csvFile, outputfile)
# This function Generates the vehicle specific html files from vehicle specific csv files
# input: csv file name and output file name
# returns: None
###################################################################################################

def convert_to_html(csvFile, outputfile):
    reader = csv.reader(open(csvFile))
    # Create the HTML file for output
    htmlfile = open(outputfile,"w")
    rownum = 0
    # write <table> tag
    htmlfile.write('<table border=1>')
    # generate table contents
    for row in reader: # Read a single row from the CSV file
         # write header row. assumes first row in csv contains header
           if rownum == 0:
              htmlfile.write('<tr>') # write <tr> tag
              for column in row:
                  htmlfile.write('<th bgcolor="orange">' + column + '</th>')
              htmlfile.write('</tr>')
          #write all other rows 
           else:
               htmlfile.write('<tr>')    
               for column in row:
                  if not column:
                     column = "  ----  "
                  htmlfile.write('<td style="border:1px solid blue;">' + column \
                                 + '</td>')
               htmlfile.write('</tr>')
       #increment row count 
           rownum += 1
          # write </table> tag
    htmlfile.write('</table>')
    # print results to shell
    print "Created " + str(rownum) + " row table."
    #       exit(0)

###################################################################################################
# main()
# This function is the entry point to files convertion, which internally calls other functions
# input: None
# returns: None
###################################################################################################

def main():
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'Config.txt')
    descDirectoryPath = configParser.get('Config', 'descDirectoryPath')
    masterDbc = configParser.get('Config', 'masterDbc')
    outputDirectoryPath = configParser.get('Config', 'outputDirectoryPath')
    canMatrixPath = configParser.get('Config', 'canMatrixPath')
    descFileNames = read_desc_files(descDirectoryPath)
    convert_to_dbc(descDirectoryPath, masterDbc, canMatrixPath, \
                   outputDirectoryPath)
    convert_to_csv(canMatrixPath, outputDirectoryPath)


if __name__ == '__main__':
    sys.exit(main())

