from colorama import Fore, Back, Style
from base.printer import print_current_DOS

def DOS_Sum(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    print('Select the DOS to sum one by one.')
    print('---------Input example---------')
    print('4 (enter)')
    print('6 (enter)')
    print('...')
    print('[q] (enter) : selection completed')
    print('-------------------------------')
    print_current_DOS(DOS_list, Labellist, graph_config)
    dos_sum_list = []
    while True:
        group_select = input('DOS sum selection : ')
        
        if group_select == 'q':
            break

        elif group_select.isdigit() == True:
            group_select = int(group_select)
            group_select = group_select - 1
            dos_sum_list.append(group_select)
        
        else:
            print('Please enter again')
    
    if len(dos_sum_list) == 0:
        print('Returning to the main screen.')
        return DOS_list, graph_config
    
    elif len(dos_sum_list) == 1:
        print('Only one DOS was selected. Returning to the main screen.')
        
    else:
        new_DOS_list = [dos for index, dos in enumerate(DOS_list) if index not in dos_sum_list]
        dos_sum_list = [DOS_list[index] for index in dos_sum_list]
        new_DOS_list.append(dos_sum_list)
            
    return new_DOS_list, graph_config
