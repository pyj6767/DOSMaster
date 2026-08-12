import pkg_resources
import os
import yaml

def Import_Custom_Setting(graph_config):
    resource_path = pkg_resources.resource_filename('dosmaster', 'custom_setting')
    yaml_files = [file for file in os.listdir(resource_path) if file.endswith('.yaml')]
    yaml_files = sorted(yaml_files, key=lambda x: os.path.getmtime(os.path.join(resource_path, x)))
    yaml_files = {index+1:file for index, file in enumerate(yaml_files)}
    print('==========Setting File List==========')
    for index, file in yaml_files.items():
        print('{} : {}'.format(index, file))
    print('=====================================')

    Input_Work = input('Which file do you want to import? (d : delete setting file, q : quit) : ')
    if Input_Work == 'q':
        return graph_config
    elif Input_Work == 'd':
        Input_Work2 = input('Which file do you want to delete? (q : quit) : ')
        if Input_Work2 == 'q':
            return graph_config
        elif Input_Work2.isdigit() == True:
            if int(Input_Work2) in yaml_files.keys():
                os.remove(os.path.join(resource_path, yaml_files[int(Input_Work2)]))
                print('Deleted {}'.format(yaml_files[int(Input_Work2)]))
                return graph_config
            else:
                print('Invalid Input')
                return graph_config
        else:
            print('Invalid Input')
            return graph_config
        
    elif Input_Work.isdigit() == True:
        if int(Input_Work) in yaml_files.keys():
            with open(os.path.join(resource_path, yaml_files[int(Input_Work)]), 'r') as f:
                imported_graph_config = yaml.load(f, Loader=yaml.FullLoader)
            print('Imported {}'.format(yaml_files[int(Input_Work)]))
            for key, value in imported_graph_config.items():
                print(key, value)
                graph_config[key] = value
            return graph_config
        else:
            print('Invalid Input')
            return graph_config
    else:
        print('Invalid Input')
        return graph_config