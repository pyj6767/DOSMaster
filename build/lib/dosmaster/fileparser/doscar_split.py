import numpy as np
from ase.io import read

#==========================================================================================[split_dos]===============================================================================
### Class to store DOS data ###
class DOSData:
    def __init__(self, e_f, dos_values):
        self.e_f = e_f
        self.dos_values = dos_values

### READ DOSCAR ###
def read_dosfile():
    f = open("DOSCAR", 'r')
    lines = f.readlines()
    f.close()
    index = 0
    natoms = int(lines[index].strip().split()[0])
    index = 5
    nedos = int(lines[index].strip().split()[2])
    efermi = float(lines[index].strip().split()[3])
    #print(natoms, nedos, efermi)

    return lines, index, natoms, nedos, efermi

### READ POSCAR or CONTCAR and save position ###
def read_posfile():
    try:
        atoms = read('CONTCAR')
    except IOError:
        print("[__main__]: Couldn't open input file CONTCAR, atomic positions will not be written...\n")
        atoms = []

    return atoms

### WRITE DOS0 CONTAINING TOTAL DOS ###
def write_dos0(lines, index, nedos, efermi):
    dos_data = []

    line = lines[index+1].strip().split()
    ncols = int(len(line))

    if ncols == 3:
        for n in range(nedos):
            index += 1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi

            dos_up = float(lines[index].strip().split()[1])
            dos_down = float(lines[index].strip().split()[1]) * 1
            dos_entry = DOSData(e_f, [dos_up, dos_down]) # added a list of zeros for spin down
            dos_data.append(dos_entry)

    elif ncols == 5:
        for n in range(nedos):
            index += 1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi

            dos_values = []
            for col in range(1, ncols):
                dos = float(lines[index].strip().split()[col])
                dos_values.append(dos)

            dos_entry = DOSData(e_f, dos_values)
            dos_data.append(dos_entry)

    return index, dos_data

### LOOP OVER SETS OF DOS, NATOMS ###
def write_nospin(lines, index, nedos, natoms, ncols, efermi):
    dos_data = []
    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    nsites = ncols - 1

    for i in range(1, natoms+1):
        si = str(i)

        index += 1
        ia = i - 1
        dos_values = []

        for n in range(nedos):
            index +=1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi

            dos_entries = [e_f]
            for site in range(nsites):
                dos_up = float(lines[index].strip().split()[site + 1])
                dos_down = float(lines[index].strip().split()[site + 1]) * (-1)
                dos_entries.extend([dos_up, dos_down])

            dos_values.append(dos_entries)
            
        dos_entry = DOSData(e_f, dos_values)
        dos_data.append(dos_entry)

    return index, dos_data

def write_spin(lines, index, nedos, natoms, ncols, efermi):
    dos_data = []
    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    nsites = int((ncols - 1) / 2)

    for i in range(1, natoms+1):
        si = str(i)

        index += 1
        ia = i - 1
        dos_values = []

        for n in range(nedos):
            index +=1
            e = float(lines[index].strip().split()[0])
            e_f = e - efermi

            dos_entries = [e_f]
            for site in range(nsites):
                dos_up = float(lines[index].strip().split()[site * 2 + 1])
                dos_down = float(lines[index].strip().split()[site * 2 + 2]) * -1
                dos_entries.extend([dos_up, dos_down])

            dos_values.append(dos_entries)
            
        dos_entry = DOSData(e_f, dos_values)
        dos_data.append(dos_entry)

    return index, dos_data

def split_dos():
    lines, index, natoms, nedos, efermi = read_dosfile()
    index, dos_data_total = write_dos0(lines, index, nedos, efermi)
    ## Test if a spin polarized calculation was performed ##
    line = lines[index+2].strip().split()
    ncols = int(len(line))

    if ncols == 7 or ncols == 19 or ncols == 9 or ncols == 33:
        index, dos_data = write_spin(lines, index, nedos, natoms, ncols, efermi)
        is_spin = True
    else:
        index, dos_data = write_nospin(lines, index, nedos, natoms, ncols, efermi)
        is_spin = False

    return dos_data_total, dos_data, is_spin

#==========================================================================================[split_dos]===============================================================================