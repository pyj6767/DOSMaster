from colorama import Fore, Back, Style

from dosmaster.base.printer import print_current_DOS

def Remove_DOS(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    print_current_DOS(DOS_list, Labellist, graph_config)
    remove_index_list = []

    while True:
        print('Which DOS do you want to remove? (Enter index)')
        print('Number-Number : Select multiple consecutive DOS (ex : 2-4)')
        group_index = input('DOS selection to remove (Finish : q) : ')
        if group_index == 'q':
            break
        elif group_index.isdigit() == True:
            group_index = int(group_index)
            remove_index_list.append(group_index)

        elif '-' in group_index:
            start, end = group_index.split('-')
            start, end = int(start), int(end)
            group_index_list = [i for i in range(start, end+1)]
            remove_index_list += group_index_list
        else:
            print('enter again')

    if remove_index_list == []:
        return DOS_list, graph_config

    else:
        new_DOS_list = []
        
        for index, DOS_temp in enumerate(DOS_list):
            if index+1 in remove_index_list:
                group_index = index+1
                if isinstance(DOS_list[group_index-1], list) == False:
                    individual_index = 'all'
                else:
                    print('DOS : {}'.format(DOS_list[group_index-1]))
                    for index, element in enumerate(DOS_list[int(group_index)-1]):
                        print('{} : {}'.format(index+1, element))
                    individual_index = input('This is a bundled DOS. Which element do you want to remove? (Enter index) (To remove the entire bundle: all) : ')

                if individual_index == 'all':
                    pass
                else:
                    new_group=[g for i, g in enumerate(DOS_list[index]) if i != int(individual_index)-1]
                    new_DOS_list.append(new_group)
            else:
                new_DOS_list.append(DOS_list[index])

        graph_config['legend_name'] = [i for j, i in enumerate(graph_config['legend_name']) if j+1 not in remove_index_list]
        graph_config['legend_name_user'] = [i for j, i in enumerate(graph_config['legend_name_user']) if j+1 not in remove_index_list]
            
        return new_DOS_list, graph_config
