
PyDoc_STRVAR(loadCollada_doc,
	"Load collada file to editableFigure\n"\
	"\n"\
	"igeTools.loadCollada(filePath, editableFigure, options)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    filePath : string\n"\
	"        collada file path to read\n"\
	"    editableFigure : igeCore.editableFigure\n"\
	"        The editableFigure object to which the Collada file is read\n"\
	"    options : dict\n"\
	"        Various options to specify when converting data	\n"\
	"            {BASE_SCALE:1.0,	\n"\
	"             EXPORT_NAMES:1,	\n"\
	"             TRIANGLE_STRIP:1,	\n"\
	"             INHERIT_JOINT_NAME:1,	\n"\
	"             CLOP_JOINT:1,	\n"\
	"             GEN_MIPMAP:1,	\n"\
	"             KILL_MIPMAP:1,	\n"\
	"             FREEZE_GEOMETORY:1,	\n"\
	"             COMPUTE_PERIOD:1}\n");

PyDoc_STRVAR(loadColladaAnimation_doc, "");
PyDoc_STRVAR(convertTextureToPlatform_doc, "");
PyDoc_STRVAR(compressFolder_doc, "");


