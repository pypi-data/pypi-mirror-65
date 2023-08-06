#include "pythonResource.h"
#include "pythonProfiler_doc_en.h"



namespace pyxie
{
	PyObject* profiler_new(PyTypeObject* type, PyObject* args, PyObject* kw)
	{
		profiler_obj* self = NULL;

		self = (profiler_obj*)type->tp_alloc(type, 0);

		PyObject* parameter = nullptr;

		if (!PyArg_ParseTuple(args, "|O", &parameter)) return NULL;
		if (parameter)
		{
			if (PyLong_Check(parameter))
			{
				bool enable = PyLong_AsLong(parameter);

				self->profiler = new Profiler("PIXIE PROFILER");				
				Profiler::EnableProfiler(enable);
			}
			else
			{
				const char* name = PyUnicode_AsUTF8(parameter);
				self->profiler = new Profiler(name);
			}
		}

		return (PyObject*)self;
	}

	void profiler_dealloc(profiler_obj* self)
	{
		//self->profiler->Release();
		delete self->profiler;
		Py_TYPE(self)->tp_free(self);
	}

	PyObject* profiler_str(profiler_obj* self)
	{
		char buf[64];
		snprintf(buf, 64, "profiler object");
		return _PyUnicode_FromASCII(buf, strlen(buf));
	}

	PyMethodDef profiler_methods[] = {
		//{ "init", (PyCFunction)profiler_Init, METH_NOARGS, profilerInit_doc },
		//{ "release", (PyCFunction)profiler_Release, METH_NOARGS, profilerRelease_doc },
		//{ "scopeStart", (PyCFunction)profiler_ScopeStart, METH_VARARGS, profilerScopeStart_doc },
		//{ "scopeEnd", (PyCFunction)profiler_ScopeEnd, METH_VARARGS, profilerScopeEnd_doc },
		{ NULL,	NULL }
	};

	PyGetSetDef profiler_getsets[] = {
		{ NULL, NULL }
	};

	PyTypeObject ProfilerType = {
		PyVarObject_HEAD_INIT(NULL, 0)
		"igeCore.profiler",					/* tp_name */
		sizeof(profiler_obj),				/* tp_basicsize */
		0,                                  /* tp_itemsize */
		(destructor)profiler_dealloc,		/* tp_dealloc */
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
		(reprfunc)profiler_str,				/* tp_str */
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
		profiler_methods,					/* tp_methods */
		0,                                  /* tp_members */
		profiler_getsets,					/* tp_getset */
		0,                                  /* tp_base */
		0,                                  /* tp_dict */
		0,                                  /* tp_descr_get */
		0,                                  /* tp_descr_set */
		0,                                  /* tp_dictoffset */
		0,                                  /* tp_init */
		0,                                  /* tp_alloc */
		profiler_new,						/* tp_new */
		0,									/* tp_free */
	};
}