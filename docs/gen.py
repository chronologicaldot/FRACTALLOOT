#! /bin/python3
# (C) 2020 Nic Anderson
# Script for generating the FRACTALLOOT website.

import sys, os, shutil, getopt

def usage():
	print("""Generate the website

Options:
	-h      Display this help message.
	-v      Print the file names as they are copied.
	--sim   Simulate the copy but do not perform it. (Useful with -v)
""")

class Options:
	def __init__(self):
		self.verbose = False
		self.simulate = False
		self.flames_path = ".."
		self.thumbs_path = "../thumbs"

class Thumb:
	def __init__(self, name, truename):
		self.name = name
		self.truename = truename
		self.flame = name + ".flame" # Assume there exists a flame file
		self.has_thumb = False


# The following deliberately run over several lines for formatting purposes.
site_header = """<!DOCTYPE html>
<html><head>
	<script type="text/javascript" src="highslide/highslide-with-gallery.js"></script>
	<link rel="stylesheet" type="text/css" href="highslide/highslide.css" />

	<!--
		2) Optionally override the settings defined at the top
		of the highslide.js file. The parameter hs.graphicsDir is important!
	-->

	<script type="text/javascript">
	hs.graphicsDir = '../highslide/graphics/';
	hs.align = 'center';
	hs.transitions = ['expand', 'crossfade'];
	hs.outlineType = 'glossy-dark';
	hs.wrapperClassName = 'dark';
	hs.fadeInOut = true;
	//hs.dimmingOpacity = 0.75;

	// Add the controlbar
	if (hs.addSlideshow) hs.addSlideshow({
		//slideshowGroup: 'group1',
		interval: 5000,
		repeat: false,
		useControls: true,
		fixedControls: 'fit',
		overlayOptions: {
			opacity: .6,
			position: 'bottom center',
			hideOnMouseOut: true
		}
	});

	</script>

	<link rel="stylesheet" type="text/css" href="site.css" />
</head><body>

<div class="titlebar">
Fractal LOOT
</div>
<div class="infobar">
All fractals here are FREE to download, share, and modify! Credit is appreciated but not required. These fractals are created by Nic Anderson.
</div>

<div class="highslide-gallery">
"""

site_footer = """
</div> <!-- end highslide gallery -->
</body></html>"""


# Create the website
def create( options, thumbs ):
	if options.simulate:
		siteroot = "../"
	else:
		#siteroot = "https://github.com/chronologicaldot/chronologicaldot/FRACTALLOOT/master/"
		siteroot = "https://raw.githubusercontent.com/chronologicaldot/FRACTALLOOT/master/"
	mainpage = open("index.html", "w+") # Opens the file, creating it if it does not exist
	mainpage.write(site_header)
	for thumb in thumbs:
		#print("Writing thumb: {thumb}".format(thumb=thumb.name))
		flame_path = siteroot + thumb.flame
		mainpage.write("""
<a href="{root}thumbs/{image_path}" class="highslide" onclick="return hs.expand(this)">
	<img style="height:10em; width:10em;" src="{root}thumbs/{thumb_path}" alt="Highslide JS" title="Click to enlarge" />
</a>
<div class="highslide-caption">
	<a href="{params}">Download Parameters</a>
</div>
""".format(root=siteroot, image_path=thumb.name, thumb_path=thumb.name, params=flame_path))

	mainpage.write(site_footer)


# Process the thumbnails list
def process( options ):
	# Collect a list of all of the .flame files.
	# They should be in the directory parenting the one with this script.
	# To be downloadable, each flame needs a corresponding thumbnail file.
	# The thumbnails will be either .png or .jpg or .gif.
	#thumbs = dict() # or {}
	thumbs = list() # or []

	thumbs_list = os.listdir( options.thumbs_path )
	for thumb_name in thumbs_list:
		thumb_path = os.path.normpath( os.path.join( options.thumbs_path, thumb_name ) )
		#print("File: {name}, {path}".format(name=thumb_name, path=thumb_path)) # debug
		if not os.path.isfile(thumb_path):
			continue
		thumb_truename, thumb_ext = os.path.splitext(thumb_name)
		if thumb_ext == ".png" or thumb_ext == ".jpg" or thumb_ext == ".gif":
			if options.verbose:
				print("Found thumb file: {name}".format(name=thumb_name))
			#thumbs[thumb_truename] = Thumb(thumb_name)
			thumbs.append(Thumb(thumb_name, thumb_truename))
	
	#file_list = os.listdir( options.flames_path )
	#for file_name in file_list:
	#	file_path = os.path.join( options.flames_path, file_name )
	#	if not os.path.isfile(file_path):
	#		continue
	#	file_truename, file_ext = os.path.splitext(file_name)
	#	if file_ext == "flame":
	#		if options.verbose:
	#			print("Found flame file: {name}".format(name=file_name))
	#		#f = Flame()
	#		#f.name = file_truename
	#		#flames.append(f)
	#		# Find matching thumb file
	#		# ... not necessary

	create( options, thumbs )
	

def main( argv ):
	for a in argv:
		print("Arg = %s" % a)

	options = Options()

	if len(argv) > 1:
		long_options = ["sim"]
		try:
			opts, args = getopt.getopt(argv[1:], "hv", long_options )
		except getopt.GetoptError:
			usage()
			sys.exit(2)
		for opt, arg in opts:
			#print("Opt({opt}), Arg({arg})".format(opt=opt, arg=arg))
			if opt == "-h":
				usage()
				sys.exit(0)
			elif opt == "-v":
				options.verbose = True
				print("Verbosity enabled")
			elif opt == "--sim":
				options.simulate = True
				print("Simulation")

	cwd = os.getcwd()
	options.flames_path = os.path.join(os.path.normpath(cwd), options.flames_path)
	options.thumbs_path = os.path.join(os.path.normpath(cwd), options.thumbs_path)

	process(options)


if __name__ == "__main__":
	main( sys.argv )
else:
	print("This program is intended to be used from the command line.")
