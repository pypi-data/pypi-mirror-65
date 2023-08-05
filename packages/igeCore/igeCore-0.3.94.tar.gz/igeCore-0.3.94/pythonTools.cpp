#include "pyxie.h"
#include "pythonResource.h"
#include "pyxieResourceCreator.h"
#include "pyxieImageConv.h"
#include "pyxieDatabaseBuilder.h"
#include "pyxieFigureExportConfigManager.h"
#include "pyxieColladaLoader.h"
#include "pythonTools_doc_en.h"

namespace pyxie
{
	typedef struct {
		PyObject_HEAD
	} pyxietools_obj;

	PyTypeObject* _EditableFigureType = nullptr;

	bool ImportPyxie() {
		PyObject* mod = PyImport_ImportModule("igeCore");
		if (!mod) return false;
		_EditableFigureType = (PyTypeObject*)PyObject_GetAttrString(mod, "editableFigure");
		Py_DECREF(mod);
		return true;
	}


	static void DictToOption(PyObject* dict) {
		PyObject* key_obj;
		PyObject* value_obj;
		Py_ssize_t pos = 0;
		while (PyDict_Next(dict, &pos, &key_obj, &value_obj))
		{
			if (!PyUnicode_Check(key_obj)) continue;

			Py_ssize_t data_len;
			const char* key_str = PyUnicode_AsUTF8AndSize(key_obj, &data_len);
			if (PyLong_Check(value_obj)) {
				int value = (int)PyLong_AsLong(value_obj);
				pyxieFigureExportConfigManager::Instance().SetOptionInt(key_str, value);
			}
			if (PyFloat_Check(value_obj)) {
				float value = (float)PyFloat_AsDouble(value_obj);
				pyxieFigureExportConfigManager::Instance().SetOptionFloat(key_str, value);
			}
		}
	}


	static PyObject* tools_loadCollada(pyxietools_obj* self, PyObject* args, PyObject* kwargs) {

		static char* kwlist[] = { "filePath", "editableFigure", "options", NULL };

		const char* path;
		editablefigure_obj* efig;
		PyObject* options = nullptr;

		if (PyArg_ParseTupleAndKeywords(args, kwargs, "sO|O", kwlist, &path, &efig, &options)) {
			if (Py_TYPE(efig) != _EditableFigureType) {
				PyErr_SetString(PyExc_TypeError, "Argument of loadCollada must be (string, editableFigure (options)).");
				return NULL;
			}
		}
		else return NULL;

		if (options && PyDict_Check(options))
			DictToOption(options);

		pyxieColladaLoader loader;
		auto rv = loader.LoadCollada(path, efig->editablefigure);
		if (!rv) {
			pyxie_printf("Failed to load %s", path);
			//PyErr_SetString(PyExc_TypeError, "Failer to load file.");
			//return NULL;
		}

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* tools_loadColladaAnimation(pyxietools_obj* self, PyObject* args, PyObject* kwargs) {

		static char* kwlist[] = { "filePath", "editableFigure","options", NULL };
		const char* path;
		editablefigure_obj* efig;
		PyObject* options = nullptr;

		if (PyArg_ParseTupleAndKeywords(args, kwargs,"sO|O", kwlist,  &path, &efig, &options)) {
			if (Py_TYPE(efig) != _EditableFigureType) {
				PyErr_SetString(PyExc_TypeError, "Argument of loadCollada must be (string, editableFigure (options)).");
				return NULL;
			}
		}
		else return NULL;

		if (options && PyDict_Check(options))
			DictToOption(options);
		//pyxieFigureExportConfigManager::Instance().SetBaseScale(baseScale);
		pyxieColladaLoader loader;
		auto rv = loader.LoadColladaAnimation(path, efig->editablefigure);
		if (!rv) {
			pyxie_printf("Failed to load %s", path);
			//PyErr_SetString(PyExc_TypeError, "Failer to load file.");
			//return NULL;
		}

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* tools_convertTextureToPlatform(pyxietools_obj* self, PyObject* args) {

		char* inFile;
		char* outFile;
		int platform;
		int normal, wrap;
		int quality = 1;	//0,1,2,3  fast, normal, product, best

		if (PyArg_ParseTuple(args, "ssiii|i", &inFile, &outFile, &platform, &normal, &wrap, &quality)) {

			char EXT[MAX_PATH];
			char OUT_PATH[MAX_PATH];
			pyxie_strncpy(OUT_PATH, outFile, MAX_PATH);
			GetPartOfFilePath(OUT_PATH, ExtentionToGetFromPath, EXT);
			if (*EXT == 0) pyxie_strncat(OUT_PATH, ".pyxi", MAX_PATH);

			pyxie::ImageConv imgConv;
			imgConv.SetInputFile(inFile);
			imgConv.SetOutputFile(OUT_PATH);
			imgConv.SetIsNormalmap(normal);
			imgConv.SetWrapRepeat(wrap);
			imgConv.SetTargetPlatform(platform);
			imgConv.SetAutoDetectAlpha();
			imgConv.SetQuality(quality);
			imgConv.DoConvert();
		}
		Py_INCREF(Py_None);
		return Py_None;

	}

	static PyObject* tools_compressFolder(pyxietools_obj* self, PyObject* args) {
		char* src;
		char* dst=nullptr;
		if (PyArg_ParseTuple(args, "s|s", &src,&dst)) {
			pyxie::ContractDatabase(src, dst?dst:src);
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	PyMethodDef tools_methods[] = {
		{ "loadCollada", (PyCFunction)tools_loadCollada, METH_VARARGS | METH_KEYWORDS, loadCollada_doc},
		{ "loadColladaAnimation", (PyCFunction)tools_loadColladaAnimation, METH_VARARGS | METH_KEYWORDS, loadColladaAnimation_doc},
		{ "convertTextureToPlatform", (PyCFunction)tools_convertTextureToPlatform, METH_VARARGS, convertTextureToPlatform_doc},
		{ "compressFolder", (PyCFunction)tools_compressFolder, METH_VARARGS, compressFolder_doc },
		{ NULL,	NULL }
	};

	static PyModuleDef tools_module = {
		PyModuleDef_HEAD_INIT,
		"igeTools",								// Module name to use with Python import statements
		"ige deverop tool",		// Module description
		0,
		tools_methods								// Structure that defines the methods of the module
	};

	PyMODINIT_FUNC PyInit__igeTools() {
		PyObject* module = PyModule_Create(&tools_module);

		if (!ImportPyxie()) {
			PyErr_SetString(PyExc_TypeError, "pyvmath isn't installed. please  pip install pyvmath before.");
			return NULL;
		}
		return module;
	}
}




