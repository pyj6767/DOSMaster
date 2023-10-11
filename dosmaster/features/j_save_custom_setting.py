import pkg_resources
import yaml

def Save_Custom_Setting(graph_config):
    resource_path = pkg_resources.resource_filename('dosmaster', 'custom_setting')
    file_name = input('Enter the setting file name : ')
    if file_name == 'q':
        return graph_config
    file_name = file_name + '.yaml'

    config_key_list = ['figuresize',
                    'axis_label_fontsize',
                    'legend_fontsize',
                    'ticks_fontsize',
                    'title_fontsize',
                    'legend_display',
                    'legend_location',
                    'bbox_to_anchor',
                    'line_width',
                    'positive_plot',
                    'negative_plot',
                    'save_filename',
                    'save_format',
                    'save_dpi',
                    'shift_x_axis']
    
    graph_config_for_save = {key:graph_config[key] for key in config_key_list}
    for g in graph_config_for_save.keys():
        print("{} : {}".format(g, graph_config_for_save[g]))

    with open(resource_path + '/' + file_name, 'w') as f:
        yaml.dump(graph_config_for_save, f, default_flow_style=False)

    print('Saved {}'.format(file_name))
    return graph_config