#! /usr/bin/env python3

from sys import argv
import sys

def get_parameters():
    """
    Returns the parameters of the switching functions (n,m, and r0):
	These are tunable parameters
    """

    r0_data = {'OH': 1.4,
               'HO': 1.4,
               'HH': 1.2,
               'CH': 1.2,
               'HC': 1.2,
               'CC': 1.7,
               'OO': 1.6,
               'OC': 1.6,
               'CO': 1.6,
               'CN': 1.6,
               'NC': 1.6,
               'ON': 1.6,
               'NO': 1.6,
               'NH': 1.4,
               'HN': 1.4,
               'NN': 1.6,
               }   
    n = 6
    m = 10 

    nm = [n,m]

    return r0_data,nm 

def read_input():
    """
    Returns input file name
    """

    NARG=1+1
    if (len(argv) != NARG) :
       print (argv[0],": error in argument number")
       print ("USAGE :")
       print (argv[0],"index.txt")
       exit(33)
    else:
       filename = argv[1]

    return filename

def read_xyz(filename):
    """Read atom type and atom index  

    Args:
        filename:  Name of input file

    Returns:
        atom_types: Element symbols of all the atoms
        atom index: element index  
    """
    with open(filename, 'r') as f:
        for line in f:
            try:
                natm = int(line)  # Read number of atoms
                next(f)     # Skip over comments
                atom_type = []
                atom_index = []
                for i in range(natm):
                    line = next(f).split()
                    atom_type.append(line[0])
                    atom_index.append(line[1])
            except (TypeError, IOError, IndexError, StopIteration):
                raise ValueError('Incorrect file format')
    return atom_type,atom_index 


def cv(filename,nm,r0_data):
    """Write the plumed.dat input file  

    Args:
        filename:  Name of input file
        nm:  n and m parameters of the switching function
        r0:  r0 parameters of the switching function
    """

    atoms,index = read_xyz(filename)

    n = nm[0]
    m = nm[1]

    arg =[]

    with open('plumed.dat', 'w') as f:
       sys.stdout = f # Change the standard output to the file we created.
       print('UNITS LENGTH=A')
       for i,ii in enumerate(index):
         for j,jj in enumerate(index):
             r0 = r0_data[atoms[i]+atoms[j]]
             aij = "a_"+str((i+1))+"_"+str((j+1))
             aji = "a_"+str((j+1))+"_"+str((i+1))
             if (aji) in arg:
                print('{}: CUSTOM ARG={} FUNC=x PERIODIC=NO\t'.format(aij,aji))
             else:
                print('{}: COORDINATION GROUPA={} GROUPB={} R_0={} NN={} MM={}\t'.format(aij,ii,jj,r0,n,m))
             arg.append(aij)
         print()
       print()
       print("cv: PYTORCH_MODEL MODEL="+str(len(index)).zfill(2)+"_cv.pt ARG=",*arg,sep = ',')
       print()
       print("opes: OPES_METAD_EXPLORE ...")
       print("   ARG=cv.*")
       print("   PACE= WARNING: ADD VALUE!")
       print("   BARRIER= WARNING: ADD VALUE!")
       print("   TEMP= WARNING: ADD VALUE!")
       print("...")
       print()
       print("PRINT ARG=cv.*,opes.* FILE=COLVAR")
       print()
    f.close()

    return

def main():

    filename = read_input()         # read txt input files containg atom_symbol and atom_index  
    r0_data,nm = get_parameters()   # get parameters of the switching functions   
    cv(filename,nm,r0_data)         # write PLUMED input file


######################################################################################################################

if __name__ == '__main__':
   main()



