import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib._color_data import BASE_COLORS, TABLEAU_COLORS, CSS4_COLORS, XKCD_COLORS
from matplotlib.patches import Rectangle


#===============================================[get Color list]================================================
def get_color_list():
    colors = mcolors.CSS4_COLORS
    # Sort colors by hue, saturation, value and name.
    sort_colors=True
    
    if sort_colors is True:
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                         name)
                        for name, color in colors.items())
        names = [name for hsv, name in by_hsv]
    else:
        names = list(colors)
        
    new_color_dict={c:colors[c] for c in names}
        
    return new_color_dict

def python_color_list():
    def plot_colortable(colors, title, sort_colors=True, emptycols=0, shows=True):

        cell_width = 212
        cell_height = 22
        swatch_width = 48
        margin = 12
        topmargin = 40

        # Sort colors by hue, saturation, value and name.
        if sort_colors is True:
            by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                             name)
                            for name, color in colors.items())
            names = [name for hsv, name in by_hsv]
        else:
            names = list(colors)

        #Modify : color name list change => label : name
        #----------------------------------------------------------------------------
        label_names={i+1:j for i,j in zip(range(len(names)),names)}
        #print(label_names)
        #----------------------------------------------------------------------------

        n = len(names)
        ncols = 4 - emptycols
        nrows = n // ncols + int(n % ncols > 0)

        width = cell_width * 4 + 2 * margin
        height = cell_height * nrows + margin + topmargin
        dpi = 72

        fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
        fig.subplots_adjust(margin/width, margin/height,
                            (width-margin)/width, (height-topmargin)/height)
        ax.set_xlim(0, cell_width * 4)
        ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        ax.set_axis_off()
        ax.set_title(title, fontsize=24, loc="left", pad=10)

        for i, name in enumerate(names):
            row = i % nrows
            col = i // nrows
            y = row * cell_height

            swatch_start_x = cell_width * col
            text_pos_x = cell_width * col + swatch_width + 7
            outputname = '{} : {}'.format(i, name)

            ax.text(text_pos_x, y, outputname, fontsize=14,
                    horizontalalignment='left',
                    verticalalignment='center')

            ax.add_patch(
                Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                          height=18, facecolor=colors[name], edgecolor='0.7')
            )

        
        return fig, label_names, colors, names

    fig,names, colors, color_names=plot_colortable(mcolors.CSS4_COLORS, "CSS Colors")
    
    plt.show()
        
#===============================================[get Color list]================================================