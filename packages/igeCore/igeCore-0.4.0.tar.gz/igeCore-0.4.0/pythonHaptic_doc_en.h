//haptic init
PyDoc_STRVAR(hapticInit_doc,
	"init the haptic system \n"\
	"\n"\
	"haptic.init()");

//haptic release
PyDoc_STRVAR(hapticRelease_doc,
	"release the profiler system\n"\
	"\n"\
	"haptic.release()");

//haptic rumble play
PyDoc_STRVAR(hapticRumblePlay_doc,
	"haptic rumble play\n"\
	"\n"\
	"haptic.rumblePlay(strength, length)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    strength : float\n"\
	"        strength of the rumble to play as a 0-1 float value\n"\
	"    length : unsigned int\n"\
	"        ength of the rumble to play in milliseconds");

//haptic effect play
PyDoc_STRVAR(hapticEffectPlay_doc,
	"haptic effect play\n"\
	"\n"\
	"haptic.effectPlay(strength, length)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    strength : float\n"\
	"        strength of the rumble to play as a 0-1 float value\n"\
	"    length : unsigned int\n"\
	"        ength of the rumble to play in milliseconds");

//haptic play
PyDoc_STRVAR(hapticPlay_doc,
	"Allow you to trigger vibrations and haptic feedbacks on both iOS and Android\n"\
	"\n"\
	"haptic.effectPlay(type, repeat)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    type : int\n"\
	"       type specify the following values \n"\
	"       pyxie.HAPTIC_SELECTION\n"\
	"       pyxie.HAPTIC_SUCCESS\n"\
	"       pyxie.HAPTIC_WARNING\n"\
	"       pyxie.HAPTIC_FAILURE\n"\
	"       pyxie.HAPTIC_LIGHT_IMPACT\n"\
	"       pyxie.HAPTIC_MEDIUM_IMPACT\n"\
	"       pyxie.HAPTIC_HEAVY_IMPACT\n"\
	"    repeat : bool\n"\
	"        pass the index into the timings array at which to start the repetition, or -1 to disable repeating.");

//haptic stop
PyDoc_STRVAR(hapticStop_doc,
	"haptic stop\n"\
	"\n"\
	"haptic.stop()");
