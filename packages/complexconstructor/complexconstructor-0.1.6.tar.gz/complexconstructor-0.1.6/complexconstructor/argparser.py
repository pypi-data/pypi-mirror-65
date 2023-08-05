import sys,os,argparse, gzip
from os.path import isfile, join


def readArgs():
    """ Read and organize the command line arguments and return the namespace"""
    parser = argparse.ArgumentParser(description="Build a protein complex from a set "
                                                 "of pdb files containing the paired "
                                                 "structures of its elements.")

    parser.add_argument('-fa', '--fasta', dest = "infasta", action = "store", default = None, 
                        help = """FASTA file with the sequences of the proteins
                               or DNA that will conform the complex.""")

    parser.add_argument('-pdb', '--pdbDir', dest = "inpdb", action = "store", default = None, 
                        help = """Diretory containing the PDB files with the 
                               structure of the pairs that will conform the complex.""")                        

    parser.add_argument('-o', '--output', dest = "outfile", action = "store", default = None, 
                        help = """Directory name where the complex results will be stored. 
                                """)

    parser.add_argument('-v', '--verbose', dest = "verbose", action = "store_true", default = False, 
                        help = """Show the detailed progression of the building process 
                                in a file called ComplexConstructor.log.""")

    parser.add_argument('-st', '--stoichiometry', dest = "stoich", action = "store", default = None, 
                        help = """File containing a determined stoichiometry to the complex. 
                               The information of the stoichiometry must be: the ID of the 
                               sequence chain (concordant with the FASTA file ID) followed by 
                               the number of times it has to be present in the complex after ':'
                               ID_as_FASTA_file : stoichiometry (one per line) in format .txt. """) 

    parser.add_argument('-gui', '--graphicInterface', dest="gui",action="store_true",default=False,
                        help="""To use ComplexConstructor with the graphical interface just use 
                              '-gui' argument in commandline.""") 

    return parser.parse_args()




