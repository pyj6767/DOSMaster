import os
import yaml

def Save_DOSMaster_Data(data_dict, graph_config):
    new_data_dict = {key:value for key, value in data_dict.items() if key == 'DOS_list' or key == 'legend_name_list'}
    total_dict= {'data_dict':new_data_dict, 'graph_config':graph_config}

    Input_Work = input('Please Enter the Description of the DOSMaster Data : ')
    total_dict['Description'] = Input_Work
    number = 1
    file_name = './DOSMaster_plot_{}.yaml'.format(number)
    while os.path.exists(file_name) == True:
        if Input_Work == 'q':
            return data_dict, graph_config
        else:
            if os.path.exists(file_name):
                number += 1
                file_name = './DOSMaster_plot_{}.yaml'.format(number)
            else:
                break

    with open(file_name, 'w') as f:
        yaml.dump(total_dict, f, default_flow_style=False)

    print('Saved {} : {}'.format(file_name, Input_Work))
    return data_dict, graph_config