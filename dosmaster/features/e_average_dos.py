import re
from colorama import Fore, Back, Style

from dosmaster.fileparser.structure_parser import Coord_to_dict
from dosmaster.features.a_add_atom_dos import Is_Range

def Average_DOS(data_dict, graph_config):
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
        print('After averaging, Projection is also possible.')
        print(Style.RESET_ALL)
        Input_Work=input('Select the index of the atom (If the selection is all done, press [q]) : ')

        if Input_Work == 'q':
            break
        elif Input_Work.isdigit() == True:
            Selected_atoms.append(Input_Work+'_all_avg')

        elif re.match(r"^([A-Za-z]+\d+(-[A-Za-z]+\d+)?)+$", Input_Work):
            if '-' in Input_Work:
                try:
                    start, end = Input_Work.split('-')

                    Input_Work1 = start
                    Input_Work2 = end
                    Input_Work1 = Labellist.index(Input_Work1) + 1
                    Input_Work2 = Labellist.index(Input_Work2) + 1

                    for input_atom in range(Input_Work1, Input_Work2+1):
                        Selected_atoms.append(str(input_atom)+'_all_avg')
                except:
                    print('Please enter again.')
                    continue
            else:
                try:
                    Input_Work = Labellist.index(Input_Work) + 1
                    Selected_atoms.append(str(Input_Work)+'_all_avg')
                except:
                    print('Please enter again.')
                    continue
            
        elif Input_Work == 'all':
            print('All atoms are selected.')
            for atom_index in range(len(Coordi_dict.keys())):
                Selected_atoms.append(str(atom_index+1)+'_all_avg')
                
        elif Is_Range(Input_Work) == True:
            start, end = Input_Work.split('-')
            start, end = int(start), int(end)
            for i in range(start, end+1):
                Selected_atoms.append(str(i)+'_all_avg')
            
        else:
            print('Please enter again.')
    
    if len(Selected_atoms) != 0:
        print('-------------------------------------------------------------------------------')
        if len(Selected_atoms) == 1:
            print('Since there is only one atom to average, the averaging process is canceled and only the atom DOS is added.')
            for s in Selected_atoms:
                DOS_list.append(s.replace('_avg', ''))
            return DOS_list, graph_config
        
        else:
            DOS_list.append(Selected_atoms)
            return DOS_list, graph_config
    
    else:
        return DOS_list, graph_config