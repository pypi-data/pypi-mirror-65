import sys
import os
import re
from datetime import datetime

def simpleName(inputPath):
   """Return the last element of a path to display just the input name"""
   justInput=re.search('([^/]+)/?$', inputPath)   
   return justInput.group(0)  

def logStart(inputList, dataList):
   """Creates the log file 'ComplexConstructorLog' and writes initial message in log file
      with the date and the input files"""
   now = datetime.now() 
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   sys.stderr = open("./"+dataList[2]+"/ComplexConstructor.log", "w")
   sys.stderr.write("\n                              ComplexConstructor\n")
   sys.stderr.write("     BUILDING OF COMPLEXES USING THE PAIRED INTERACTION OF ITS ELEMENTS\n")
   sys.stderr.write("Written by Paula Gomis Rosa, Arturo González Vilanova and Marta López Balastegui\n\n")
   print("Job starting time: ", dt_string, file=sys.stderr)
   sys.stderr.write("\nInput files:\n\t - FASTA sequences in file:\n\t ")   
   fas=inputList[-1]
   print('\t',simpleName(fas), file=sys.stderr)
   sys.stderr.write("\n\t - PDB files:\n")  
   pdbs=list( inputList[i] for i in range(len(inputList)-1) )
   for element in pdbs:
      print('\t\t',simpleName(element), file=sys.stderr)
   return None

def progress(outDir,dic,stValues):
   """Write in the log file the progression information"""
   sys.stderr = open("./"+outDir+"/ComplexConstructor.log", "a")

   keyList=[]
   for element in dic:
      keyList.append(element)

   print("\nNumber of chains found: ", len(keyList), file=sys.stderr) 
   print("IDs of the chains: ", (', '.join(keyList)), file=sys.stderr)

   if stValues is not None:
      print("\nThe stoichiometry for those chains is: ", file=sys.stderr)
      for element in stValues:
         print(element,": ",stValues[element], file=sys.stderr)
   print("\n", file=sys.stderr)
   return None

def end(outDir, outFile):
   """ Final message in logFile """
   cwd = os.getcwd()
   resultDir=cwd+'/'+outDir
   print("\nProcess completed correctly, macrocomplex structure in file '%s'" %outFile,file=sys.stderr)
   print("\nThe result is stored in directory '%s'." %resultDir, file=sys.stderr)
   return None