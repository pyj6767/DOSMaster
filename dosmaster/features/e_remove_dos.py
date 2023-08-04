from colorama import Fore, Back, Style

from dosmaster.base.printer import print_current_DOS

def Remove_DOS(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    
    print_current_DOS(DOS_list, Labellist, graph_config)
    group_index = input('Which DOS do you want to remove? (Enter index) : ')
    
    if isinstance(DOS_list[int(group_index)-1], list) == False:
        individual_index = 'all'
    else:
        for index, element in enumerate(DOS_list[int(group_index)-1]):
            print('{} : {}'.format(index+1, element))
        individual_index = input('This is a bundled DOS. Which element do you want to remove? (Enter index) (To remove the entire bundle: all) : ')

    new_DOS_list = []
    for index, DOS_temp in enumerate(DOS_list):
        if index == int(group_index)-1:
            if individual_index == 'all':
                pass
            else:
                new_group=[g for i, g in enumerate(DOS_list[index]) if i != int(individual_index)-1]
                new_DOS_list.append(new_group)
        else:
            new_DOS_list.append(DOS_list[index])
            
    graph_config['legend_name'] = [i for j, i in enumerate(graph_config['legend_name']) if j != int(group_index)-1]
        
    return new_DOS_list, graph_config
