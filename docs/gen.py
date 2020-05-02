#! /bin/python3
# (C) 2020 Nic Anderson
# Script for generating the FRACTALLOOT website.

import sys, os, shutil, getopt, string
# string is imported for string.ascii_lowercase

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
		self.flames_path = "../"
		self.images_path = "../images"
		self.thumbs_path = "../thumbs"

class Image:
	def __init__(self, name, truename):
		self.name = name
		self.truename = truename
		self.flame = truename + ".flame" # Assume there exists a flame file
		self.has_thumb = False


# The following deliberately run over several lines for formatting purposes.
site_header = """<!DOCTYPE html>
<html><head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<script type="text/javascript" src="highslide/highslide-with-gallery.js"></script>
	<link rel="stylesheet" type="text/css" href="highslide/highslide.css" />

	<script type="text/javascript">
	hs.graphicsDir = 'highslide/graphics/';
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
"""

site_index_body = """
<div class="titlebar">
Fractal LOOT
</div>
<div class="infobar">
All fractals (and images) here are FREE to download, share, and modify! Credit is appreciated but not required. These fractals are created by Nic Anderson (Chronologicaldot/ABlipinTime, <a href="https://www.chronologicaldot.com">website</a>, <a href="https://ablipintime.deviantart.com">fractal art</a>). Special thanks to Michael (TheAudioMonk) for rendering the fractal previews.
<p>
PLEASE NOTE: The parameters were designed in JWildfire but the vast majority of the renders are from Chaotica. Chaotica doesn't have all the same transform variations, so some fractals may appear messed up. Also note that some parameters require custom transforms, which may require minimum versions of JWildfire. Versions of JWF 2.5 and up should suffice to render most parameters. Note further that, beginning with JWF 3, brightness calculations changed, resulting in many parameters designed in older JWF versions as appearing dark in these images, so just increase the brightness.</p>
<p>
PLEASE NOTE: Most of the fractals were rendered with their perspectives widened, causing round shapes to appear elliptical. Most of the fractals were rendered at only moderate resolution, so they may appear dusty.
</p>
<p>
PLEASE NOTE: This is a fractal DUMP. It includes nearly every fractal parameter created over the course of 10 years, so the quality ranges from newb to boss. None of the fractals are sorted. Many appear to be duplicates but are actually progressions in the development of a final fractal form. These may be useful in tutorials.
</p>
<p>More fractal flame parameters can be found in <a href="https://github.com/chronologicaldot/chronologicaldot/FRACTALLOOT">the huge repository</a>.
</p>
</div>
"""

site_gallery_body = """
<div class="titlebar">
Fractal LOOT
</div>
<div class="highslide-gallery">
"""

site_gallery_footer = """
</div> <!-- end highslide gallery -->"""

site_footer = """
</body></html>"""

# Create the gallery
def createGalleryPage( page, pageprefix, siteroot, options, images ):
	page.write(site_header)
	page.write(site_gallery_body)
	for image in images:
		if len(pageprefix) > 0 and image.name[0:len(pageprefix)].lower() != pageprefix:
			#print("Page prefix no match: ", image.name[0:len(pageprefix)].lower(), " : Seek: ", pageprefix)
			continue

		#print("Writing image: {image}".format(image=image.name))
		flame_path = siteroot + image.flame
		thumb_path = os.path.join("thumbs", image.name)
		if image.has_thumb:
			thumb_path = "images/" + image.name
		page.write("""
<a href="{root}images/{image_name}" class="highslide" onclick="return hs.expand(this)">
<img style="height:10em; width:10em;" src="{root}{thumb_path}" alt="Fractal Image" title="Click to enlarge" />
</a>
<div class="highslide-caption">
{image_truename} |
<a href="{params}">Download Parameters</a>
</div>
""".format(root=siteroot, image_name=image.name, thumb_path=thumb_path, params=flame_path, image_truename=image.truename))

	page.write(site_gallery_footer)
	page.write(site_footer)


# Create the website
def create( options, images ):
	if options.simulate:
		siteroot = "../"
	else:
		#siteroot = "https://github.com/chronologicaldot/chronologicaldot/FRACTALLOOT/master/"
		siteroot = "https://raw.githubusercontent.com/chronologicaldot/FRACTALLOOT/master/"

	mainpage = open("index.html", "w+") # Opens the file, creating it if it does not exist
	mainpage.write(site_header)
	mainpage.write(site_index_body)

	# Should include here a page for premium fractals, labeled with a star

	for x in string.ascii_lowercase:
		pagelink = "{pagename}.html".format(pagename=x)
		page = open( pagelink, "w+" )
		createGalleryPage(page, x, siteroot, options, images)
		# Page link
		mainpage.write( '<a style="font-size:2em" href="https://chronologicaldot.github.io/FRACTALLOOT/{pagelink}">{pagename}</a> '.format(siteroot=siteroot, pagelink=pagelink, pagename=x) )

	mainpage.write(site_footer)


# Process the imagenails list
def process( options ):
	# Collect a list of all of the imagenail files.
	# They should be in the directory in the directory parenting the one with this script.
	# To be downloadable, each imagenail needs a corresponding .flame file.
	# The imagenails will be either .png or .jpg or .gif.
	#images = dict() # or {}
	images = list() # or []

	images_list = os.listdir( options.images_path )
	for image_name in images_list:
		image_path = os.path.normpath( os.path.join( options.images_path, image_name ) )
		#print("File: {name}, {path}".format(name=image_name, path=image_path)) # debug
		if not os.path.isfile(image_path):
			continue
		image_truename, image_ext = os.path.splitext(image_name)
		if image_ext == ".png" or image_ext == ".jpg" or image_ext == ".gif":
			if options.verbose:
				print("Found image file: {name}".format(name=image_name))
			#images[image_truename] = Image(image_name)
			images.append(Image(image_name, image_truename))

	for image in images:
		thumb_path = os.path.normpath( os.path.join( options.thumbs_path, image.name ) )
		if not os.path.isfile(thumb_path):
			continue
		thumb_truename, thumb_ext = os.path.splitext(thumb_path)
		if thumb_ext == ".png" or thumb_ext == ".jpg" or thumb_ext == ".gif":
			if options.verbose:
				print("Found thumbnail file: {name}".format(name=thumb_truename))
			image.has_thumb = True

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
	#		# Find matching image file
	#		# ... not necessary

	create( options, images )
	

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
	options.images_path = os.path.join(os.path.normpath(cwd), options.images_path)

	process(options)


if __name__ == "__main__":
	main( sys.argv )
else:
	print("This program is intended to be used from the command line.")
