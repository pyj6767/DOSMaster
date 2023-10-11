from colorama import Fore, Back, Style
from dosmaster.base.printer import print_current_DOS

def DOS_Sum(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    print(Style.BRIGHT + Fore.RED)
    print('Input method 1 : Select the DOS to sum one by one. (ex : 2)')
    print('Input method 2 : Number-Number : Select multiple consecutive DOS (ex : 2-4)')
    print(Style.RESET_ALL)
    print('---------Input example---------')
    print('2-3 (enter)')
    print('4 (enter)')
    print('6 (enter)')
    print('...')
    print('[q] (enter) : selection completed')
    print('-------------------------------')
    print_current_DOS(DOS_list, Labellist, graph_config)
    dos_sum_list = []
    while True:
        group_select = input('DOS sum selection (Finish : q) : ')
        
        if group_select == 'q':
            break

        elif group_select.isdigit() == True:
            group_select = int(group_select)
            group_select = group_select - 1
            dos_sum_list.append(group_select)

        elif '-' in group_select and group_select.split('-')[0].isdigit() == True:
            start, end = group_select.split('-')
            start, end = int(start), int(end)
            for i in range(start, end+1):
                dos_sum_list.append(i-1)
        
        else:
            print('Please enter again')
    
    if len(dos_sum_list) == 0:
        print('Returning to the main screen.')
        return DOS_list, graph_config
    
    elif len(dos_sum_list) == 1:
        print('Only one DOS was selected. Returning to the main screen.')
        
    else:
        #new_DOS_list = [dos for index, dos in enumerate(DOS_list) if index not in dos_sum_list]
        new_DOS_list = [dos for dos in DOS_list]
        new_dos_sum_list = []
        for index in dos_sum_list:
            if isinstance(DOS_list[index], list) == True:
                new_dos_sum_list += DOS_list[index]
            else:
                new_dos_sum_list.append(DOS_list[index])
        new_DOS_list.append(new_dos_sum_list)
            
    return new_DOS_list, graph_config

