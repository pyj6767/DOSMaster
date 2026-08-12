import os
import yaml

def Import_DOSMaster_Data(data_dict, graph_config):
    current_path = './'
    yaml_files = [file for file in os.listdir(current_path) if file.endswith('.yaml') and file.startswith('DOSMaster_plot')]
    yaml_files = sorted(yaml_files, key=lambda x: os.path.getmtime(os.path.join(current_path, x)))
    yaml_files = {index+1:file for index, file in enumerate(yaml_files)}
    print('==========DOSMaster Data File List==========')
    for index, file in yaml_files.items():
        with open(current_path+file, 'r') as f:
            imported_dict = yaml.load(f, Loader=yaml.FullLoader)
        print('{} : {} | Description : {}'.format(index, file, imported_dict['Description']))
    print('============================================')

    Input_Work = input('Which file do you want to import? (q : quit) : ')
    if Input_Work == 'q':
        return data_dict, graph_config
    elif Input_Work.isdigit() == True:
        if int(Input_Work) in yaml_files.keys():
            Input_Work2 = input('If import dos plot, then current dos will be removed. Do you want to continue? (1 : yes / 2 : no(default)) : ')
            if Input_Work2 == '1':
                with open(os.path.join(current_path, yaml_files[int(Input_Work)]), 'r') as f:
                    imported_dict = yaml.load(f, Loader=yaml.FullLoader)
                    graph_config_initial = {'figuresize' : [8, 6],
                                    'axis_label_fontsize' : 13,
                                    'legend_fontsize' : 13,
                                    'ticks_fontsize' : 13,
                                    'title_fontsize' : 13,
                                    'legend_display' : True,
                                    'legend_name' : None,
                                    'legend_name_user' : [False],
                                    'legend_location' : 'best',
                                    'bbox_to_anchor' : None,
                                    'line_width' : 1,
                                    'xlim' : None,
                                    'ylim' : None,
                                    'positive_plot' : True,
                                    'negative_plot' : True,
                                    'save_filename' : 'DOS',
                                    'save_format' : 'pdf',
                                    'save_dpi' : 200,
                                    'dos_color' : None,
                                    'ylim_optimization' : False,
                                    'shift_x_axis' : 0,
                                    }

                print('Imported {}'.format(yaml_files[int(Input_Work)]))
                data_dict['DOS_list'] = imported_dict['data_dict']['DOS_list']
                data_dict['legend_name_list'] = imported_dict['data_dict']['legend_name_list']
                for key, value in imported_dict['graph_config'].items():
                    graph_config[key]=value

                return data_dict, graph_config
            else:
                print('Canceled')
                return data_dict, graph_config
        else:
            print('Invalid Input')
            return data_dict, graph_config

    else:
        print('Invalid Input')
        return data_dict, graph_config
