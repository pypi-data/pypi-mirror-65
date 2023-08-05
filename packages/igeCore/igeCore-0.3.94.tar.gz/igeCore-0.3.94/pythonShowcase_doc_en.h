
//showcase
PyDoc_STRVAR(showcase_doc,
	"showcase is where you put the objects \n"\
	"you want to render.\n"\
	"You can add figure, editableFigure, environment, camera.\n"\
	"\n"\
	"case = igeCore.shocase()");

//add
PyDoc_STRVAR(add_doc,
	"Add object to showcase\n"\
	"\n"\
	"showcase.add(object, depth)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : igeCore.figure, igeCore.editableFigure, igeCore.environment\n"\
	"        Object to be added to showcase\n"\
	"	depth : float (optional)\n"\
	"		Higher values render later.\n"\
	"		If the values are the same, they will be rendered in the order in which they were added.\n"\
	"		If omitted, it is assumed to be 0");


//remove
PyDoc_STRVAR(remove_doc,
	"Remove object from showcase\n"\
	"\n"\
	"showcase.add(object)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    object : igeCore.figure, igeCore.editableFigure, igeCore.environment\n"\
	"        Object to be added to showcase");


//clear
PyDoc_STRVAR(clear_doc,
	"Remove all object from showcase\n"\
	"\n"\
	"showcase.clear()");


//changeDepth
PyDoc_STRVAR(changeDepth_doc,
	"Change depth of object in showcase\n"\
	"\n"\
	"showcase.changeDepth(object, depth)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"	object : igeCore.figure, igeCore.editableFigure, igeCore.environment\n"\
	"		Object to be added to showcase\n"\
	"	depth : float\n"\
	"		Higher values render later.\n"\
	"		If the values are the same, they will be rendered in the order in which they were added.\n");

