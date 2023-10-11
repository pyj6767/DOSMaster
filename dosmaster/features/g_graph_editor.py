from colorama import Fore, Back, Style

from dosmaster.subplotter.colortable import python_color_list
from dosmaster.base.printer import print_current_DOS
from dosmaster.base.data_generation import list_to_string_name

def color_selection_old(DOS_list, Labellist, graph_config, color_dict):
    color_list=list(color_dict.keys())
    while True:
        print_current_DOS(DOS_list, Labellist, graph_config)
        print('Press q when all settings are complete.')
        dos_choice = input('Which DOS color would you like to change? (Enter number) (Back : q) : ')
        if dos_choice.isdigit() == True:
            python_color_list()
            color_choice = input('Please write the color number : ')
            if color_choice.isdigit() == True:
                Color_list_save.append(Color_list_save[int(dos_choice)-1])
                Color_list_save.remove(color_list[int(color_choice)])
                Color_list_save[int(dos_choice)-1] = color_list[int(color_choice)]
                graph_config['Color_list'] = Color_list_save
                #graph_config['Color_list'][int(dos_choice)]=color_list[int(color_choice)]
            else:
                print('You have entered incorrectly.')
                
        elif dos_choice == 'q':
            return graph_config
        else:
            print('Please reselect the DOS')
            
def color_selection(DOS_list, Labellist, graph_config, color_dict):
    color_list=list(color_dict.keys())
    while True:
        print_current_DOS(DOS_list, Labellist, graph_config)
        print('Press q when all settings are complete.')
        dos_choice = input('Which DOS color would you like to change? (Enter number) (Back : [q]) : ')
        if dos_choice.isdigit() == True:
            python_color_list()
            color_choice = input('Please write the color number : ')
            if color_choice.isdigit() == True:
                graph_config['dos_color'][list_to_string_name(DOS_list[int(dos_choice)-1])]['color'] = color_list[int(color_choice)]
                graph_config['dos_color'][list_to_string_name(DOS_list[int(dos_choice)-1])]['User_Edit'] = 'Yes'
            else:
                print('You have entered incorrectly.')
                
        elif dos_choice == 'q':
            return graph_config
        else:
            print('Please reselect the DOS')
            
    
def Graph_Editor(data_dict, graph_config):
    DOS_list = data_dict['DOS_list']
    Labellist = data_dict['Labellist']
    color_dict = data_dict['color_dict']
    
    key_list=list(graph_config.keys())
    while True:
        print(Style.BRIGHT + Fore.YELLOW)
        print('===========================================[Graph Configuration]==================================================')
        for index, key in enumerate(key_list):
            if key == 'Color_list':
                print('{:<5} : {:<30} -- {}'.format(index+1, key, graph_config[key][:len(DOS_list)]))

            elif key == 'dos_color':
                iteration=0
                for k,v in graph_config[key].items():
                    if iteration == 0:
                        print('{:<5} : {:<30} -- {:<5}  :  {:<5}'.format(index+1, key, k, graph_config[key][k]['color']))
                    else:
                        print('{:>41} {:<5}  :  {:<5}'.format('--', k, graph_config[key][k]['color']))
                    iteration += 1

            else:
                print ('{:<5} : {:<30} -- {}'.format(index+1, key, graph_config[key]))
        print('==================================================================================================================')
        print(Style.RESET_ALL)
        graph_index_input = input('What would you like to modify? (Enter index , [q]: back) : ')
        if graph_index_input == 'q':
            break
        elif graph_index_input.isdigit() == False:
            print('Please enter again')
            
        elif key_list[int(graph_index_input)-1] == 'dos_color':
            graph_config = color_selection(DOS_list, Labellist, graph_config, color_dict)
            return graph_config
        
        elif key_list[int(graph_index_input)-1] == 'positive_plot' or key_list[int(graph_index_input)-1] == 'negative_plot':
            graph_value_input = input('True(1, default) or False(2) : ')
            if graph_value_input == '2':
                graph_config[key_list[int(graph_index_input)-1]] = False
            else:
                graph_config[key_list[int(graph_index_input)-1]] = True
            return graph_config
        
        elif key_list[int(graph_index_input)-1] == 'figuresize':
            while True:
                a_input = input('Enter horizontal Size : ')
                if a_input == 'q':
                    break
                b_input = input('Enter vertical Size : ')
                if b_input == 'q':
                    break
                
                try:
                    a=float(a_input)
                    b=float(b_input)
                    graph_config[key_list[int(graph_index_input)-1]] = [a,b]
                    return graph_config
                except:
                    print('Please enter again')
        
        elif key_list[int(graph_index_input)-1] == 'xlim' or key_list[int(graph_index_input)-1] == 'ylim':
            while True:
                a_input = input('{} Min value : '.format(key_list[int(graph_index_input)-1]))
                if a_input == 'q':
                    break
                b_input = input('{} Max value : '.format(key_list[int(graph_index_input)-1]))
                if b_input == 'q':
                    break
                
                try:
                    a=float(a_input)
                    b=float(b_input)
                    graph_config[key_list[int(graph_index_input)-1]] = [a,b]
                    return graph_config
                except:
                    print('Please enter again')

        elif key_list[int(graph_index_input)-1] == 'legend_display':
            while True:
                a_input = input('True(1, default) or False(2) : ')
                if a_input == 'q':
                    break
                elif a_input == '2':
                    graph_config[key_list[int(graph_index_input)-1]] = False
                    return graph_config
                else:
                    graph_config[key_list[int(graph_index_input)-1]] = True
                    return graph_config
                
        elif key_list[int(graph_index_input)-1] == 'legend_name':
            while True:
                print_current_DOS(DOS_list, Labellist, graph_config)
                print(Style.BRIGHT+Fore.RED+'Press [qq] when all settings are complete. ([q] 2 times)'+Style.RESET_ALL)
                print(Style.BRIGHT+Fore.RED+'Press [q] to go back.'+Style.RESET_ALL)
                a_input = input('Which DOS Legend would you like to modify? : ')
                if a_input == 'q':
                    break
                elif a_input == 'qq':
                    return graph_config
                b_input = input('Enter a new Legend name : ')
                if b_input == 'q':
                    break
                elif b_input == 'qq':
                    return graph_config

                try:
                    dos_index=int(a_input)
                    legend_list=graph_config[key_list[int(graph_index_input)-1]]
                    legend_list[dos_index-1] = b_input
                    graph_config[key_list[int(graph_index_input)-1]] = legend_list

                    new_legend_name_user = []
                    for i in range(len(graph_config['legend_name'])):
                        try:
                            if graph_config['legend_name_user'][i] == True:
                                new_legend_name_user.append(True)
                            else:
                                if i == dos_index-1:
                                    new_legend_name_user.append(True)
                                else:
                                    new_legend_name_user.append(False)
                        
                        except:
                            if i == dos_index-1:
                                new_legend_name_user.append(True)
                            else:
                                new_legend_name_user.append(False)

                    graph_config['legend_name_user'] = new_legend_name_user
                
                except:
                    print('Please enter again')
                    
        elif key_list[int(graph_index_input)-1] == 'legend_location':
            while True:
                loc_list=['[1] upper right', '[2] upper left', '[3] lower left', '[4] lower right', '[5] right', '[6] center left', '[7] center right', '[8] lower center', '[9] upper center', '[10] center', '[11] best']
                print('==================================================[Location List]=================================================')
                for loc in loc_list:
                    print(loc)
                print('==================================================================================================================')
                print(Style.BRIGHT+Fore.RED+'Press [qq] when all settings are complete. ([q] 2 times)'+Style.RESET_ALL)
                print(Style.BRIGHT+Fore.RED+'Press [q] to go back.'+Style.RESET_ALL)
                print(Style.BRIGHT+Fore.CYAN+"If you want to place the Legend outside, type 'outside'."+Style.RESET_ALL)
                a_input = input('Select a new Legend Location : ')
                if a_input == 'q':
                    break
                elif a_input == 'qq':
                    return graph_config
                elif a_input == 'outside':
                    graph_config['legend_location'] = 'upper left'
                    graph_config['bbox_to_anchor'] = (1.05, 1.0)
                    return graph_config
                elif a_input.isdigit() == True:
                    graph_config['legend_location'] = loc_list[int(a_input)-1].split('] ')[1]
                    return graph_config
                else:
                    print('Please enter again')
            
                
        elif key_list[int(graph_index_input)-1] == 'save_format':
            format_list=['pdf', 'png', 'jpg', 'svg', 'eps', 'tif']
            for index, formats in enumerate(format_list):
                print('{} : {}'.format(index+1, formats))
                
            while True:
                a_input = input('Would you like to choose a format? : ')
                if a_input == 'q':
                    break
                
                try:
                    graph_config[key_list[int(graph_index_input)-1]] = format_list[int(a_input)-1]
                    return graph_config
                except:
                    print('Please enter again')

        elif key_list[int(graph_index_input)-1] == 'shift_x_axis':
            while True:
                print('Current shift value : {}'.format(graph_config[key_list[int(graph_index_input)-1]]))
                print(Style.BRIGHT+Fore.RED+'Press [qq] when all settings are complete. ([q] 2 times)'+Style.RESET_ALL)
                print(Style.BRIGHT+Fore.RED+'Press [q] to go back.'+Style.RESET_ALL)
                a_input = input('x-axis shift value : ')
                if a_input == 'q':
                    break
                elif a_input == 'qq':
                    return graph_config
                else:
                    try:
                        graph_config[key_list[int(graph_index_input)-1]] = float(a_input)
                        return graph_config
                    except:
                        print('Please enter again')
            
        else:
            graph_value_input = input('Enter a new value : ')
            try:
                graph_value=float(graph_value_input)
                graph_config[key_list[int(graph_index_input)-1]] = graph_value
                return graph_config
            except:
                print('Please enter again')
            
    return graph_config
