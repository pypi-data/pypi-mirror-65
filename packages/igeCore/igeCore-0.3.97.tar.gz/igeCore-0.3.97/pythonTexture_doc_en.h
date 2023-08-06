//texture
PyDoc_STRVAR(texture_doc,
	"Textures are RGBA bitmap image objects \n"\
	"\n"\
	"Formula\n"\
	"----------\n"\
	"    tex = igeCore.texture(name)\n"\
	"        Create texture from image file.\n"\
	"    tex = igeCore.texture(name,width,height,format,depth,stencil,pixel)\n"\
	"        Create texture from parameters.\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string\n"\
	"        If there are no parameters other than name, \n"\
	"        name is assumed to be the image file name.\n"\
	"        When combined with other parameters such as width and height, \n"\
	"        name is considered a unique name for the texture.\n"\
	"    width : int\n"\
	"        width of texture pixels.\n"\
	"    height : int\n"\
	"        height of texture pixels.\n"\
	"    format : int\n"\
	"        enable texture format\n"\
	"        GL_RED : 1 channel format (n,0,0,0)\n"\
	"        GL_RGB : 3 channel format (n,m,l,0)\n"\
	"        GL_RGBA : 4 channel format (n,m,l,o)\n"\
	"    depth : bool\n"\
	"        At the same time, a depth buffer is generated.\n"\
	"        This option is for use as a render target.\n"\
	"    stencil : bool\n"\
	"        At the same time, a stencil buffer is generated.\n"\
	"        This option is for use as a render target.\n"\
	"    pixel : numpy.ndarray or byte object\n"\
	"        array for bitmap image.\n");

//setImage
PyDoc_STRVAR(setImage_doc,
	"Set byte image to texture object\n"\
	"\n"\
	"texture.setImage(image, x, y, width,height)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    image : Bytes or numpy.ndarray\n"\
	"        array of rgb or rgba image\n"\
	"    x : int (optional)\n"\
	"        x offset of destination\n"\
	"    y : int (optional)\n"\
	"        y offset of destination\n"\
	"    width : int (optional)\n"\
	"        copy image width\n"\
	"    height : int (optional)\n"\
	"        copy image height\n");


//setCheckeredImage
PyDoc_STRVAR(setCheckeredImage_doc,
	"Set checkerd image to texture object\n"\
	"\n"\
	"texture.setCheckeredImage(r, g, b, a)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    r,g,b,a : int (optional)\n"\
	"        checker color (0 - 1)\n"\
	"        default color is red");


//setText
PyDoc_STRVAR(setText_doc,
	"Render text to texture object\n"\
	"\n"\
	"texture.setText(word, fontpath, size)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    word : string\n"\
	"        word to render.\n"\
	"    fontpath : string\n"\
	"        font file path.\n"\
	"    size : int\n"\
	"        size of render text");

//clear
PyDoc_STRVAR(clear_doc,
	"Clear the texture with the specified color \n"\
	"\n"\
	"texture.clear(r, g, b, a)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    r, g, b, a : float\n"\
	"        clear color(0-1).\n"\
	"        size of render text");

//capture
PyDoc_STRVAR(captureScreenshot_doc,
	"capture the screen \n"\
	"\n"\
	"texture.captureScreenshot(name)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string (optional)\n"\
	"        capture name");

//capture
PyDoc_STRVAR(saveToGallery_doc,
    "save image captured to gallery \n"\
    "\n"\
    "texture.saveToGallery()");

//get render target data
PyDoc_STRVAR(getData_doc,
	"Get the render target data\n"\
	"\n"\
	"texture.getData(x,y,w,h)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    x,y,w,h : int (optional)\n"\
	"        default color is (0, 0, -1, -1)\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result : list(unsigned char)");