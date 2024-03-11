from dosmaster.fileparser.structure_parser import Coord_to_dict
from colorama import Fore, Back, Style
import re

def Is_Range(input_string):
    numbers = input_string.split('-')

    if len(numbers) != 2:
        return False

    start, end = numbers

    if not start.isdigit() or not end.isdigit():
        return False

    start, end = int(start), int(end)

    if start >= end:
        return False

    return True

def Add_Atom_DOS(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    coordi = data_dict['coordi']
    
    Coordi_dict=Coord_to_dict(Labellist, coordi)
    Selected_atoms=[]
    while True:
        print(Style.BRIGHT + Fore.RED)
        print('Input Method 1 : Atom index (ex: 11)')
        print('Input Method 2 : Number-Number: Select several consecutive atoms (ex: 13-24)')
        print('Input Method 3 : Atom name and index number (consecutive input also possible). (ex : Si32 / Si32-Si34 / O1-O2)')
        print('Input Method 4 : all: Select all atoms')
        print(Style.RESET_ALL)
        print('========Input Example=======')
        print('11 (enter)')
        print('13-24 (enter)')
        print('Si32 (enter)')
        print('O5-O9 (enter)')
        print('all (enter)')
        print('q (enter) : Selection complete')
        print('============================')
        
        if len(Selected_atoms) != 0:
            atom_indices = [int(atom_index.split('_')[0])-1 for atom_index in Selected_atoms]
            #Sorting
            print('Selected Atoms : ', [Labellist[atom_index] for atom_index in atom_indices])
        Input_Work=input('Please select the index of the Atom (If the selection is complete, enter q) : ')
        if Input_Work == 'q':
            break
        elif Input_Work.isdigit() == True:
            Selected_atoms.append(Input_Work+'_all')

        elif re.match(r"^([A-Za-z]+\d+(-[A-Za-z]+\d+)?)+$", Input_Work):
            if '-' in Input_Work:
                try:
                    start, end = Input_Work.split('-')

                    Input_Work1 = start
                    Input_Work2 = end
                    Input_Work1 = Labellist.index(Input_Work1) + 1
                    Input_Work2 = Labellist.index(Input_Work2) + 1

                    for input_atom in range(Input_Work1, Input_Work2+1):
                        Selected_atoms.append(str(input_atom)+'_all')
                except:
                    print('Please enter again.')
                    continue
            else:
                try:
                    Input_Work = Labellist.index(Input_Work) + 1
                    Selected_atoms.append(str(Input_Work)+'_all')
                except:
                    print('Please enter again.')
                    continue
            
        elif Input_Work == 'all':
            print('All atoms are selected.')
            for atom_index in range(len(Coordi_dict.keys())):
                Selected_atoms.append(str(atom_index+1)+'_all')
                
        elif Is_Range(Input_Work) == True:
            start, end = Input_Work.split('-')
            start, end = int(start), int(end)
            for i in range(start, end+1):
                Selected_atoms.append(str(i)+'_all')
            
        else:
            print('Please enter again.')
    
    if len(Selected_atoms) != 0:
        print('-------------------------------------------------------------------------------')
        print('1: Draw these atoms separately')
        print('2: Combine the contributions of these atoms and draw them')
        print('-------------------------------------------------------------------------------')
        Input_Work2=input('Please select how to process the contribution. (default: 1) : ')
        if Input_Work2 != '2':
            for s in Selected_atoms:
                DOS_list.append(s)
        else:
            if len(Selected_atoms) == 1:
                print('There is only one atom to combine the contribution, so select to draw separately.')
                for s in Selected_atoms:
                    DOS_list.append(s)
            else:
                DOS_list.append(Selected_atoms)
                
        return DOS_list, graph_config
    
    else:
        return DOS_list, graph_config