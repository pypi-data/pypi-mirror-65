//profiler init
PyDoc_STRVAR(profilerInit_doc,
	"init the profiler system \n"\
	"\n"\
	"profiler.init()");

//profiler release
PyDoc_STRVAR(profilerRelease_doc,
	"release the profiler system\n"\
	"\n"\
	"profiler.release()");

//profiler scope start
PyDoc_STRVAR(profilerScopeStart_doc,
	"profiler scope start\n"\
	"\n"\
	"profiler.scopeStart(name)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string\n"\
	"        event name");

//profiler scope end
PyDoc_STRVAR(profilerScopeEnd_doc,
	"profiler scope end\n"\
	"\n"\
	"profiler.scopeEnd()");