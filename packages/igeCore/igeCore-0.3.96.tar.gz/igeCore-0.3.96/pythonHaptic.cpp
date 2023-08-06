#include "pythonResource.h"
#include "pythonHaptic_doc_en.h"

namespace pyxie
{
	PyObject* haptic_new(PyTypeObject* type, PyObject* args, PyObject* kw)
	{
		haptic_obj* self = NULL;

		self = (haptic_obj*)type->tp_alloc(type, 0);
		self->haptic = new Haptic();
		
		return (PyObject*)self;
	}

	void haptic_dealloc(haptic_obj* self)
	{
		self->haptic->Release();
		Py_TYPE(self)->tp_free(self);
	}

	PyObject* haptic_str(haptic_obj* self)
	{
		char buf[64];
		snprintf(buf, 64, "haptic object");
		return _PyUnicode_FromASCII(buf, strlen(buf));
	}

	static PyObject* haptic_Init(haptic_obj* self)
	{		
		self->haptic->Init();

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* haptic_Release(haptic_obj* self)
	{
		self->haptic->Release();

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* haptic_RumblePlay(haptic_obj* self, PyObject* args)
	{
		float strength = 0.0f;
		uint32_t length = 0;
		if (!PyArg_ParseTuple(args, "fI", &strength, &length))
			return NULL;

		self->haptic->RumblePlay(strength, length);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* haptic_EffectPlay(haptic_obj* self)
	{
		self->haptic->EffectPlay();

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* haptic_Play(haptic_obj* self, PyObject* args)
	{
		int hapticType = 0;
		int hapticRepeat = -1;
		if (!PyArg_ParseTuple(args, "II", &hapticType, &hapticRepeat))
			return NULL;

		self->haptic->HapticPlay(hapticType, hapticRepeat);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* haptic_Stop(haptic_obj* self)
	{
		self->haptic->HapticStop();

		Py_INCREF(Py_None);
		return Py_None;
	}

	PyMethodDef haptic_methods[] = {
		{ "init", (PyCFunction)haptic_Init, METH_NOARGS, hapticInit_doc },
		{ "release", (PyCFunction)haptic_Release, METH_NOARGS, hapticRelease_doc },
		{ "rumblePlay", (PyCFunction)haptic_RumblePlay, METH_VARARGS, hapticRumblePlay_doc },
		{ "effectPlay", (PyCFunction)haptic_EffectPlay, METH_NOARGS, hapticEffectPlay_doc },
		{ "play", (PyCFunction)haptic_Play, METH_VARARGS, hapticPlay_doc },
		{ "stop", (PyCFunction)haptic_Stop, METH_NOARGS, hapticStop_doc },
		{ NULL,	NULL }
	};

	PyGetSetDef haptic_getsets[] = {
		{ NULL, NULL }
	};

	PyTypeObject HapticType = {
		PyVarObject_HEAD_INIT(NULL, 0)
		"igeCore.haptic",					/* tp_name */
		sizeof(haptic_obj),					/* tp_basicsize */
		0,                                  /* tp_itemsize */
		(destructor)haptic_dealloc,			/* tp_dealloc */
		0,                                  /* tp_print */
		0,							        /* tp_getattr */
		0,                                  /* tp_setattr */
		0,                                  /* tp_reserved */
		0,                                  /* tp_repr */
		0,					                /* tp_as_number */
		0,                                  /* tp_as_sequence */
		0,                                  /* tp_as_mapping */
		0,                                  /* tp_hash */
		0,                                  /* tp_call */
		(reprfunc)haptic_str,				/* tp_str */
		0,                                  /* tp_getattro */
		0,                                  /* tp_setattro */
		0,                                  /* tp_as_buffer */
		Py_TPFLAGS_DEFAULT,					/* tp_flags */
		0,									/* tp_doc */
		0,									/* tp_traverse */
		0,                                  /* tp_clear */
		0,                                  /* tp_richcompare */
		0,                                  /* tp_weaklistoffset */
		0,									/* tp_iter */
		0,									/* tp_iternext */
		haptic_methods,						/* tp_methods */
		0,                                  /* tp_members */
		haptic_getsets,						/* tp_getset */
		0,                                  /* tp_base */
		0,                                  /* tp_dict */
		0,                                  /* tp_descr_get */
		0,                                  /* tp_descr_set */
		0,                                  /* tp_dictoffset */
		0,                                  /* tp_init */
		0,                                  /* tp_alloc */
		haptic_new,							/* tp_new */
		0,									/* tp_free */
	};
}