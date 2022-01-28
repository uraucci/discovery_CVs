make_plumed.py generates the PLUMED input file.

It takes as input a txt file of the following format:

"
Natm (Number of atoms included in the adjacency matrix)

Atom_Symbol   Atom_index 
...
...
... 
Atom_Symbol   Atom_index 
"

test1.txt and test2.txt are input examples.

According to the system you may need to change the parameters of the switching functions (r0,n and m): you can change them in the function get_parameters (at the top of the script).

The folder pytorch_models contains the pytorch model used to compute the maximum eigenvalue of the adjacency matrix and its derivatives. 
Files are named according to the dimension of the adjancency matrix. Use the file corresponding to the dimension of your matrix. 

USAGE:
python3 make_plumed.py test1.txt


