import csv

# Color list to csv
Default_Color_list = ['gray', 'red', 'blue', 'green', 'darkorange', 'magenta', 'lightcoral', 'khaki', 'forestgreen', 'darkslategray', 
                    'slategrey', 'navy', 'darkorchid', 'lightpink', 'darkgoldenrod', 'chartreuse', 'aqua', 'lightblue', 
                    'midnightblue', 'violet', 'darkred', 'coral', 'seagreen', 'paleturquoise', 'dodgerblue', 'cornflowerblue', 
                    'purple', 'pink', 'moccasin', 'lightgreen', 'darkcyan', 'powderblue', 'mediumblue', 'slateblue', 'crimson', 
                    'tan', 'mediumspringgreen', 'aquamarine', 'slategray', 'darkblue', 'indigo', 'indianred', 'darkkhaki', 'darkolivegreen', 
                    'turquoise', 'skyblue', 'royalblue', 'blueviolet', 'brown', 'blanchedalmond', 'mediumseagreen', 'darkslategrey', 'cadetblue', 
                    'hotpink', 'palevioletred', 'navajowhite', 'darkseagreen', 'mediumturquoise', 'deepskyblue', 'thistle', 'firebrick', 'chocolate', 
                    'lawngreen', 'teal', 'lightskyblue', 'mediumslateblue', 'maroon', 'goldenrod', 'limegreen', 'cyan', 'lightslategrey', 'mediumpurple', 
                    'rosybrown', 'saddlebrown', 'olivedrab', 'lightseagreen', 'lightsteelblue', 'deeppink', 'darksalmon', 'olive', 'darkturquoise', 
                    'steelblue', 'plum', 'gold', 'yellowgreen', 'mediumaquamarine', 'lightslategray', 'mediumvioletred', 'peachpuff', 'lime', 'orchid', 
                    'orangered', 'springgreen', 'darkviolet', 'papayawhip', 'yellow', 'darkslateblue', 'lemonchiffon', 'palegreen', 'darkmagenta', 
                    'antiquewhite', 'greenyellow', 'rebeccapurple', 'orange', 'mediumorchid', 'burlywood', 'palegoldenrod', 'cornsilk', 'sienna', 
                    'peru', 'wheat', 'lightsalmon', 'bisque', 'salmon', 'tomato', 'sandybrown']

with open('colors.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(Default_Color_list)