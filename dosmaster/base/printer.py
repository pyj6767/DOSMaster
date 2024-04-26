import numpy as np
import pandas as pd
import pickle
from os import path
from colorama import Fore, Back, Style

from dosmaster.main import __version__
from dosmaster.fileparser.procar_parser import PROCAR_Parser
from dosmaster.fileparser.doscar_split import split_dos


def ls_to_string_name(dos_element):
    if isinstance(dos_element, list) == False:
        return dos_element
    else:
        return ' and '.join(dos_element)

# Print Current DOS
def print_current_DOS(DOS_list, Labellist, graph_config):
    print(Style.BRIGHT + Fore.CYAN)
    print('=============================================[Current DOS List]===================================================')
    for i, d in enumerate(DOS_list):
        if isinstance(d, list)==True:
            labeled_d = [Labellist[int(d_temp.split('_')[0])-1]+'('+d_temp.split('_')[1]+')' if 'Total DOS' not in d_temp else d_temp.split('_')[0]+'('+d_temp.split('_')[1]+')' for d_temp in d ]
            if '_avg' in d[0]:
                print_element=' + '.join(labeled_d)+'(avg)'
            else:
                print_element=' + '.join(labeled_d)

        else:
            if d == 'Total DOS_all':
                print_element='Total DOS(all)'
                
            elif d.split('_')[0] == 'Total DOS' and d.split('_')[1] != 'all':
                print_element='Total DOS_{}'.format(d.split('_')[1])

            else:
                print_element=Labellist[int(d.split('_')[0])-1]+'('+d.split('_')[1]+')'
        
        print('{:<4} : {:<60} | Legend : {:<20} | color : {:<30}'.format(i+1, print_element, graph_config['legend_name'][i], graph_config['dos_color'][ls_to_string_name(d)]['color']))
    print('==================================================================================================================')
    print(Style.RESET_ALL)
    
# Print Orbital List
def print_orbital_list(orbital_list):
    for i, orbital in enumerate(orbital_list):
        print('{} : {}'.format(i+1, orbital))
        

# Create Dos Dataframe (Edit by Jaesun)
def Make_DOS_Dataframe():
    if path.isfile('./dos_data_total.pkl') == True:
        print(Fore.YELLOW)
        print('                             Existing dos data file exists. Loading the dos data.')
        print(Style.RESET_ALL)
        # Load dos_data_total.pkl, get dos_data_total and is_spin
        with open('./dos_data_total.pkl', 'rb') as f:
            dos_data_total = pickle.load(f)
            is_spin = pickle.load(f)
        dos_object_total_dos=dos_data_total[0]
        dos_object_list=dos_data_total[1]
        orbital_list=dos_data_total[2]
    else:
        print('                                                    ...                                                            ')
        #0. Run split_dos function
        dos_data_total, dos_data, is_spin = split_dos()
    
        if path.exists("PROCAR") == False:
            print('PROCAR file cannot be found. Now Dosmaster uses basic orbital list.')
            orbital_list = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'x2-y2', 'fxyz', 'fyz2', 'fz3', 'fxz2', 'fzx3', 'fx3']
    
        else:
            #1. Get orbital_list from PROCAR
            orbital_list = PROCAR_Parser('./PROCAR')

        #2. Convert to 2D list
        dos_data_total_list=[[dos_temp.e_f] + dos_temp.dos_values for dos_temp in dos_data_total]
        dos_object_list=[np.array(dos_object.dos_values) for dos_object in dos_data]

        column_names = []
        for ol in orbital_list:
            column_names.append(ol+'_up')
            column_names.append(ol+'_down')
        column_names.insert(0, 'Energy')

        #3. Convert dos_data[each] to table(df)
        dos_object_total_dos = pd.DataFrame(dos_data_total_list)
        dos_object_list=[pd.DataFrame(dos_object, columns=column_names) for dos_object in dos_object_list]
        
        dos_data_total=[dos_object_total_dos, dos_object_list, orbital_list]
        with open('./dos_data_total.pkl', 'wb') as f:
            pickle.dump(dos_data_total, f)
            pickle.dump(is_spin, f)
            
    return dos_object_total_dos, dos_object_list, orbital_list, is_spin

def Reading_Files():
    print(Style.BRIGHT, Fore.RED)
    print('                 DOG version {:>5} : Now, ISPIN = 2 & ISPIN = 1 both calculations are supported.            '.format(__version__))
    print(Style.RESET_ALL)
    print()
    print('========================================= Reading DOSCAR (Start) =================================================')
    if path.exists("DOSCAR") == False:
        print('DOSCAR file cannot be found.')
        exit()

    dos_object_total_dos, dos_object_list, orbital_list, is_spin = Make_DOS_Dataframe()
    print('========================================= Reading DOSCAR (Finish)=================================================')
    print(Style.BRIGHT, Fore.RED)
    if is_spin == True:
        is_spin_value = 2
    else:
        is_spin_value = 1
    print()
    print('                                    Your Calculation Setting : ISPIN = {}'.format(is_spin_value))
    print(Style.RESET_ALL)
    print(Style.BRIGHT + Fore.CYAN)
    print('Xshell에서 그림을 끌 때는 꼭 "q"를 눌러서 끄세요!!!!')
    print(Style.RESET_ALL)
    print()
    return dos_object_total_dos, dos_object_list, orbital_list, is_spin
