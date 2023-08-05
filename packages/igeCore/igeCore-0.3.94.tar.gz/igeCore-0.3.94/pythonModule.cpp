#include <Python.h>
//#include <Windows.h>
#include <cmath>
#include "pythonResource.h"
#include "pyxieFios.h"
#include "pyxieTime.h"

#include "pyxieTouchManager.h"
#include "pyxieSystemInfo.h"
#include "pyxieApplication.h"

#include "bitmapHelper.h"

#include <vector>
#include <algorithm>

#include "pythonModule_doc_en.h"
#include "pythonInput.h"

extern std::shared_ptr<pyxie::pyxieApplication> gApp;

namespace pyxie
{
	static PyObject* pyxie_getPlatform(PyObject* self) {
		return PyLong_FromLong(CURRENT_PLATFORM);
	}

	static PyObject* pyxie_elapsedTime(PyObject* self) {
		return PyFloat_FromDouble(pyxieTime::Instance().GetElapsedTime());
	}

	static PyObject* pyxie_setRoot(PyObject* self, PyObject* args) {
		char* path = nullptr;
		if (!PyArg_ParseTuple(args, "s", &path)) return NULL;
		pyxieFios::Instance().SetRoot(path);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_getRoot(PyObject* self) {
		const char* root = pyxieFios::Instance().GetRoot();
		return _PyUnicode_FromASCII(root, strlen(root));
	}

	static PyObject* pyxie_isRunning(PyObject* self, PyObject* args) {
		return PyBool_FromLong(gApp->isRunning());
	}

	static PyObject *pyxie_update(PyObject *self)
	{
		gApp->update();
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject *pyxie_sync(PyObject *self)
	{
		if (gApp->swap() == false) {
			PyErr_SetString(PyExc_TypeError, (const char*)"terminate ige");
			Terminate();
			return NULL;
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_startLog(PyObject* self)
	{
		pyxie_logg_start();
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_window(PyObject* self, PyObject* args) {
		int show = 0;
		int x = 480;
		int y = 640;
        	int resizable = 1;    
		if (PyArg_ParseTuple(args, "iii|i", &show, &x, &y, &resizable)) {			
			gApp->showAppWindow(show, x, y, resizable);
		}        
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_getWindow(PyObject* self) {
		if(gApp && gApp->getAppWindow()) {
			PyObject* res = Py_BuildValue("O", PyCapsule_New(gApp->getAppWindow(), "SDL_Window", NULL));
			return res;
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject *pyxie_singleTouch(PyObject *self, PyObject *args)
	{
		(void)self;

		int fingerNo = 0;
		if (!PyArg_ParseTuple(args, "|i", &fingerNo))
			return NULL;

		std::vector<uint32_t> ids;
		const SingleFingerEvent* fingerEvent = pyxieTouchManager::Instance().GetFirstSingleFingerEvent();
		while (fingerEvent != nullptr) {
			ids.push_back(fingerEvent->id);
			fingerEvent = fingerEvent->pNext;
		}
		if (ids.size() <= fingerNo) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		std::sort(ids.begin(), ids.end());
		uint32_t fingerID = ids[fingerNo];

		fingerEvent = pyxieTouchManager::Instance().GetFirstSingleFingerEvent();
		while (fingerEvent != nullptr) {
			if (fingerEvent->id == fingerID) {
				PyObject *_res =
					Py_BuildValue(
						"{s:i,s:b,s:h,s:h,s:h,s:h,s:h,s:h,s:L,s:L,s:b,s:b,s:b,s:b,s:b,s:b,s:b,s:b,s:b,s:b,s:b}",
						"state", fingerEvent->state,
						"id", fingerEvent->id,
						"org_x", fingerEvent->org_x,
						"org_y", fingerEvent->org_y,
						"cur_x", fingerEvent->cur_x,
						"cur_y", fingerEvent->cur_y,
						"delta_x", fingerEvent->delta_x,
						"delta_y", fingerEvent->delta_y,
						"delta_t", fingerEvent->delta_t,
						"elapsed_t", fingerEvent->elapsed_t,
						"fast_motion_t", fingerEvent->fast_motion_t,
						"num_tap", fingerEvent->num_tap,
						"is_pressed", fingerEvent->state& TOUCH_STATE_PRESS?1:0,
						"is_holded", fingerEvent->state& TOUCH_STATE_HOLD ? 1 : 0,
						"is_released", fingerEvent->state& TOUCH_STATE_RELEASE ? 1 : 0,
						"is_tapped", fingerEvent->is_tapped,
						"is_longpressed", fingerEvent->is_longpressed,
						"is_tap_candidate", fingerEvent->is_tap_candidate,
						"is_flicked", fingerEvent->is_flicked,
						"force", fingerEvent->force,
						"is_moved", fingerEvent->is_moved,
						"num_tap", fingerEvent->num_tap,
						"fast_motion_t", fingerEvent->fast_motion_t);
				return _res;
			}
			fingerEvent = fingerEvent->pNext;
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_viewSize(PyObject* self)
	{
		pyxieSystemInfo& sysinfo = pyxieSystemInfo::Instance();
		float w = sysinfo.GetGameW();
		float h = sysinfo.GetGameH();

		PyObject* retval = NULL;
		PyObject* v = NULL;
		retval = PyTuple_New(2);
		if (!retval)
			return NULL;

		v = PyFloat_FromDouble((double)w);
		if (v == NULL) {
			Py_DECREF(retval);
			return NULL;
		}
		PyTuple_SET_ITEM(retval, 0, v);

		v = PyFloat_FromDouble((double)h);
		if (v == NULL) {
			Py_DECREF(retval);
			return NULL;
		}
		PyTuple_SET_ITEM(retval, 1, v);

		return retval;
	}

	static PyObject* pyxie_setViewLength(PyObject* self, PyObject* args) {

		float length;
		if (!PyArg_ParseTuple(args, "f", &length))
			return NULL;
		pyxieSystemInfo& sysinfo = pyxieSystemInfo::Instance();
		sysinfo.SetGemeScreenSize(length);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_calcFontPixelSize(PyObject* self, PyObject* args, PyObject* kwargs) {

		static char* kwlist[] = { "text","fontpath","fontsize", NULL };
		char* text;
		char* fontpath;
		int fontsize;
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ssi", kwlist, &text, &fontpath, &fontsize)) return NULL;
		return calcTextSize(text, fontpath, fontsize);
	}
	
	static PyObject* pyxie_unique(PyObject* self, PyObject* args) {
		static int uniqueNumber = 0;
		char* str;
		if (!PyArg_ParseTuple(args, "s", &str))
			return NULL;
		char buff[MAX_PATH];
		pyxie_snprintf(buff, MAX_PATH, "%s%d", str, uniqueNumber);
		uniqueNumber++;
		pyxieSystemInfo& sysinfo = pyxieSystemInfo::Instance();
		return PyUnicode_FromString(buff);
	}

	static PyMethodDef pyxie_methods[] = {
		{"getElapsedTime", (PyCFunction)pyxie_elapsedTime, METH_NOARGS, getElapsedTime_doc },
		{ "isRunning", (PyCFunction)pyxie_isRunning, METH_VARARGS, isRunning_doc },
		{ "update", (PyCFunction)pyxie_update, METH_NOARGS, update_doc },
		{ "swap", (PyCFunction)pyxie_sync, METH_NOARGS, swap_doc },
		{ "window", (PyCFunction)pyxie_window, METH_VARARGS, window_doc},
		{ "getWindow", (PyCFunction)pyxie_getWindow, METH_VARARGS, getWindow_doc},
		{ "singleTouch", (PyCFunction)pyxie_singleTouch, METH_VARARGS,singleTouch_doc  },
		{ "viewSize", (PyCFunction)pyxie_viewSize, METH_NOARGS, viewSize_doc},
		{ "setViewLength", (PyCFunction)pyxie_setViewLength, METH_VARARGS, setViewLength_doc },
		{ "setRoot", (PyCFunction)pyxie_setRoot, METH_VARARGS,setRoot_doc },
		{ "getRoot", (PyCFunction)pyxie_getRoot, METH_NOARGS, getRoot_doc },
		{ "getPlatform", (PyCFunction)pyxie_getPlatform, METH_NOARGS, getPlatform_doc },		
		{ "startLog", (PyCFunction)pyxie_startLog, METH_NOARGS, startLog_doc },
		{ "calcFontPixelSize", (PyCFunction)pyxie_calcFontPixelSize, METH_VARARGS | METH_KEYWORDS, calcFontPixelSize_doc },
		{ "unique", (PyCFunction)pyxie_unique, METH_VARARGS, unique_doc },
		{ "registerEventListener", (PyCFunction)pyxie_registerEventListener, METH_VARARGS, NULL },
		{ "isKeyPressed", (PyCFunction)pyxie_isKeyPressed, METH_VARARGS, NULL },
		{ "isKeyReleased", (PyCFunction)pyxie_isKeyReleased, METH_VARARGS, NULL },
		{ "isKeyHold", (PyCFunction)pyxie_isKeyHold, METH_VARARGS, NULL },
		{ "getKeyChar", (PyCFunction)pyxie_getKeyChar, METH_VARARGS, NULL },
		{ "getKeyModifier", (PyCFunction)pyxie_getKeyModifier, METH_NOARGS, NULL },
		{ "isFingerPressed", (PyCFunction)pyxie_isFingerPressed, METH_VARARGS, NULL },
		{ "isFingerMoved", (PyCFunction)pyxie_isFingerMoved, METH_VARARGS, NULL },
		{ "isFingerReleased", (PyCFunction)pyxie_isFingerReleased, METH_VARARGS, NULL },
		{ "isFingerScrolled", (PyCFunction)pyxie_isFingerScrolled, METH_VARARGS, NULL },
		{ "getFingerScrolledData", (PyCFunction)pyxie_getFingerScrolledData, METH_VARARGS, NULL },		
		{ "getFingerPosition", (PyCFunction)pyxie_getFingerPosition, METH_VARARGS, NULL },
		{ "getFingerPressure", (PyCFunction)pyxie_getFingerPressure, METH_VARARGS, NULL },
		{ "getFingersCount", (PyCFunction)pyxie_getFingersCount, METH_NOARGS, NULL },
		{ "getAllFingers", (PyCFunction)pyxie_getAllFingers, METH_NOARGS, NULL },
        { nullptr, nullptr, 0, nullptr }
	};

	static PyModuleDef pyxie_module = {
		PyModuleDef_HEAD_INIT,
		"_igeCore",								// Module name to use with Python import statements
		"indi game endine core module",  // Module description
		0,
		pyxie_methods							// Structure that defines the methods of the module
	};

	PyMODINIT_FUNC _PyInit__igeCore() {
		PyObject *module = PyModule_Create(&pyxie_module);

		if (!ImportVMath()) {
			PyErr_SetString(PyExc_TypeError, "pyvmath isn't installed. please  pip install pyvmath before.");
			return NULL;
		}
		if (PyType_Ready(&FigureType) < 0) return NULL;
		if (PyType_Ready(&AnimatorType) < 0) return NULL;
		if (PyType_Ready(&CameraType) < 0) return NULL;
		if (PyType_Ready(&EnvironmentType) < 0) return NULL;
		if (PyType_Ready(&ShowcaseType) < 0) return NULL;
		if (PyType_Ready(&EditableFigureType) < 0) return NULL;
		if (PyType_Ready(&ShaderGeneratorType) < 0) return NULL;
		if (PyType_Ready(&TextureType) < 0) return NULL;
		if (PyType_Ready(&ParticleType) < 0) return NULL;
		if (PyType_Ready(&ProfilerType) < 0) return NULL;
		if (PyType_Ready(&HapticType) < 0) return NULL;

		Py_INCREF(&FigureType);
		PyModule_AddObject(module, "figure", (PyObject*)& FigureType);

		Py_INCREF(&EditableFigureType);
		PyModule_AddObject(module, "editableFigure", (PyObject*)& EditableFigureType);

		Py_INCREF(&AnimatorType);
		PyModule_AddObject(module, "animator", (PyObject *)&AnimatorType);

		Py_INCREF(&CameraType);
		PyModule_AddObject(module, "camera", (PyObject *)&CameraType);

		Py_INCREF(&EnvironmentType);
		PyModule_AddObject(module, "environment", (PyObject *)&EnvironmentType);

		Py_INCREF(&ShowcaseType);
		PyModule_AddObject(module, "showcase", (PyObject *)&ShowcaseType);

		Py_INCREF(&ShaderGeneratorType);
		PyModule_AddObject(module, "shaderGenerator", (PyObject*)& ShaderGeneratorType);

		Py_INCREF(&TextureType);
		PyModule_AddObject(module, "texture", (PyObject*)& TextureType);
		
		Py_INCREF(&ParticleType);
		PyModule_AddObject(module, "particle", (PyObject *)&ParticleType);

		Py_INCREF(&ProfilerType);
		PyModule_AddObject(module, "profiler", (PyObject*)&ProfilerType);

		Py_INCREF(&HapticType);
		PyModule_AddObject(module, "haptic", (PyObject*)&HapticType);

        return module;
	}
}
