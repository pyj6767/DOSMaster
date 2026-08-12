from colorama import Fore, Back, Style

from dosmaster.base.printer import print_current_DOS
from dosmaster.base.data_generation import list_to_string_name
from dosmaster.subplotter.dosplot_manager import get_atom_count

def Divide_By_Atom_Number(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']

    # Store which DOS lines are divided by their own number of atoms.
    graph_config.setdefault('divide_by_atom', {})

    print_current_DOS(DOS_list, Labellist, graph_config)
    print(Style.BRIGHT + Fore.RED)
    print('Each DOS line can be divided by the number of atoms that compose it.')
    print('(The number of atoms can be different for each DOS line.)')
    print(Style.RESET_ALL)
    print('Input method 1 : DOS index to toggle (ex : 2)')
    print('Input method 2 : Number-Number : several consecutive DOS (ex : 2-4)')
    print('Input method 3 : all : select every DOS line')
    print('-------------------------------')

    while True:
        # Show the atom count and current divide status of each DOS line.
        print('----------------------------------[Divide Status]---------------------------------')
        for i, d in enumerate(DOS_list):
            dos_name = list_to_string_name(d)
            atom_count = get_atom_count(d, Labellist)
            if graph_config['divide_by_atom'].get(dos_name, False) == True:
                status = 'ON  (/{})'.format(atom_count)
            else:
                status = 'OFF'
            print('{:<4} : {:<45} | atoms : {:<5} | divide : {}'.format(i+1, dos_name, atom_count, status))
        print('----------------------------------------------------------------------------------')

        group_select = input('DOS selection to toggle (Finish : q) : ')

        if group_select == 'q':
            break

        select_index_list = []
        if group_select == 'all':
            select_index_list = [i for i in range(1, len(DOS_list)+1)]

        elif group_select.isdigit() == True:
            select_index_list.append(int(group_select))

        elif '-' in group_select and group_select.split('-')[0].isdigit() == True:
            start, end = group_select.split('-')
            start, end = int(start), int(end)
            for i in range(start, end+1):
                select_index_list.append(i)

        else:
            print('Please enter again')
            continue

        for index in select_index_list:
            if index < 1 or index > len(DOS_list):
                continue
            dos_name = list_to_string_name(DOS_list[index-1])
            current = graph_config['divide_by_atom'].get(dos_name, False)
            graph_config['divide_by_atom'][dos_name] = not current

    return graph_config
