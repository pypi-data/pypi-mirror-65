import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


## ref

# https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa

# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python

def hex_to_rgb(value):
	value = value.lstrip('#')
	lv = len(value)
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
	return '#%02x%02x%02x' % rgb

def plot_colortable(colors, title="35 Unique Colors"):
	"""
	
	copy from https://matplotlib.org/3.1.0/gallery/color/named_colors.html
	
	colors: dict [name] = [hex]
	
	"""
	cell_width = 300
	cell_height = 50
	swatch_width = 48
	margin = 12
	topmargin = 40


	
	names = list(colors)

	n = len(names)
	ncols = 3 
	nrows = 11

	width = cell_width * 4 
	height = cell_height * nrows + margin + topmargin
	dpi = 100

	fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
	fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
	ax.set_xlim(0, cell_width * 4)
	ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
	ax.yaxis.set_visible(False)
	ax.xaxis.set_visible(False)
	ax.set_axis_off()
	ax.set_title(title, fontsize=24, loc="left")

	for i, name in enumerate(names):
		row = i % nrows
		col = i // nrows
		y = row * cell_height

		swatch_start_x = cell_width * col
		swatch_end_x = cell_width * col + swatch_width
		text_pos_x = cell_width * col + swatch_width + 7

		ax.text(text_pos_x, y, name, fontsize=14,
				horizontalalignment='left',
				verticalalignment='center')

		ax.hlines(y, swatch_start_x, swatch_end_x,
				  color=colors[name], linewidth=18)

	return fig

def unique_color():
	return ["#ffff00","#00ffff","#7fff00","#ad4545","#c06464","#379e7d","#1c7caf","#cfa345","#99aab5","#bbeaf8","#f19500","#87cefa","#6f1a52","#476aae","#e6521c","#e1609f","#149c98","#b3dd9e","#3b0056","#70867f","#fff2ec","#cae7e7","#daa520","#b6d4d0","#c39797","#660000","#faebd7","#bada55","#d0ad8d","#e8def6","#b90702","#ffcc00","#4d4238"]
	
def unique_color_hex():
	return unique_color()
	
def unique_color_rgb():
	return [hex_to_rgb(x) for x in unique_color_hex()]

def main():

	colors={x:x for x in unique_color()}
	print (len(colors))
	print (colors)
	fig = plot_colortable(colors, title="33 Unique Colors")
	plt.savefig("33_unique_colors.png")

if __name__ == "__main__":
	main()




