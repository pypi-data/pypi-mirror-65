///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include <Python.h>

#include "pyxieTypes.h"

namespace pyxie
{
    PyObject* pyxie_registerEventListener(PyObject* self, PyObject* args);

	PyObject* pyxie_isKeyPressed(PyObject* self, PyObject* args);

	PyObject* pyxie_isKeyReleased(PyObject* self, PyObject* args);

	PyObject* pyxie_isKeyHold(PyObject* self, PyObject* args);

	PyObject* pyxie_getKeyChar(PyObject* self, PyObject* args);

	PyObject* pyxie_getKeyModifier(PyObject* self, PyObject* args);

	PyObject* pyxie_getFingerPosition(PyObject* self, PyObject* args);

	PyObject* pyxie_getFingerPressure(PyObject* self, PyObject* args);

	PyObject* pyxie_isFingerPressed(PyObject* self, PyObject* args);

	PyObject* pyxie_isFingerMoved(PyObject* self, PyObject* args);

	PyObject* pyxie_isFingerReleased(PyObject* self, PyObject* args);

	PyObject* pyxie_isFingerScrolled(PyObject* self, PyObject* args);

	PyObject* pyxie_getFingerScrolledData(PyObject* self, PyObject* args);

	PyObject* pyxie_getFingersCount(PyObject* self, PyObject* args);

	PyObject* pyxie_getAllFingers(PyObject* self, PyObject* args);
}
