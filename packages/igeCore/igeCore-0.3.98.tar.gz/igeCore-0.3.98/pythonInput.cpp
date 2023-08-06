///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#include "pythonInput.h"

#include <Python.h>

#include "input/pyxieEvent.h"
#include "input/pyxieKeyboard.h"
#include "input/pyxieTouch.h"
#include "input/pyxieInputHandler.h"

#include "pyxieApplication.h"
extern std::shared_ptr<pyxie::pyxieApplication> gApp;

namespace pyxie
{
    static PyObject *onKeyPressedCB = nullptr;
    static PyObject *onKeyReleasedCB = nullptr;

    static PyObject *onTouchBeganCB = nullptr;
    static PyObject *onTouchEndedCB = nullptr;
    static PyObject *onTouchMovedCB = nullptr;
    static PyObject *onTouchScrolledCB = nullptr;

	static PyObject *onEventCB = nullptr;

    void pyxieProcessEventCallbackHandler(const void* args)
    {
        // Ensure python has initialized
        if(!Py_IsInitialized())
            return;
        
        Py_BEGIN_ALLOW_THREADS
        PyGILState_STATE gState = PyGILState_Ensure();
        
        PyObject *caller = nullptr;
        PyObject *arglist = nullptr;
        const pyxie::Event* event = (const pyxie::Event*)args;
		
        if(event->getType() == pyxie::Event::Type::TOUCH) {
            auto touchEvent = (const pyxie::TouchEvent*)event;
            auto finger = touchEvent->getFinger();
            if(touchEvent->getEventCode() == pyxie::TouchEvent::EventCode::SCROLLED) {
                arglist = Py_BuildValue("(Lffi)", finger->getFingerId(), finger->getScrollX(), finger->getScrollY(), finger->isScrollFlipped() ? 1 : 0);
                caller = onTouchScrolledCB;
            }
            else
            {                
                arglist = Py_BuildValue("(Lfff)", finger->getFingerId(), finger->getCurrentPosX(), finger->getCurrentPosY(), finger->getPressure());
                if(touchEvent->getEventCode() == pyxie::TouchEvent::EventCode::BEGAN) {
                    caller = onTouchBeganCB;
                }
                else if(touchEvent->getEventCode() == pyxie::TouchEvent::EventCode::MOVED) {
                    caller = onTouchMovedCB;
                }
                else if(touchEvent->getEventCode() == pyxie::TouchEvent::EventCode::ENDED) {
                    caller = onTouchEndedCB;
                }
            }
        }
        else if(event->getType() == pyxie::Event::Type::KEYBOARD) {
            auto keyEvent = (const pyxie::KeyboardEvent*)event;
            arglist = Py_BuildValue("(iiii)", (int)keyEvent->getKeyCode(), (int)keyEvent->getEventCode(), (int)keyEvent->getKey(), keyEvent->getKeyModifier());
            caller = (keyEvent->getEventCode() == pyxie::KeyboardEvent::EventCode::PRESSED) ? onKeyPressedCB : onKeyReleasedCB;
        }

        if(caller && arglist) {
            PyObject *result = PyEval_CallObject(caller, arglist);
            Py_DECREF(arglist);
            Py_XDECREF(result);
        }

        PyGILState_Release( gState );
        Py_END_ALLOW_THREADS
    }

	void pyxieProcessRawEventCallbackHandler(const void* event)
	{
		// Ensure python has initialized
        if(!Py_IsInitialized())
            return;
        
        Py_BEGIN_ALLOW_THREADS
        PyGILState_STATE gState = PyGILState_Ensure();

		if(onEventCB) {
			PyObject *arglist = Py_BuildValue("(O)", PyCapsule_New((void*)event, "SDL_Event", NULL));
			PyObject *result = PyEval_CallObject(onEventCB, arglist);
            Py_DECREF(arglist);
            Py_XDECREF(result);
		}

		PyGILState_Release( gState );
        Py_END_ALLOW_THREADS
	}

    PYXIE_EXPORT void pyxieRegisterEventListener(int eventType, int eventCode, const void* handler)
    {
		if(eventType == (int)pyxie::Event::Type::KEYBOARD) {
            if(eventCode == (int)pyxie::KeyboardEvent::EventCode::PRESSED) {
                Py_XDECREF(onKeyPressedCB);
                onKeyPressedCB = (PyObject*)handler;
            }
            else if(eventCode == (int)pyxie::KeyboardEvent::EventCode::RELEASED) {
                Py_XDECREF(onKeyReleasedCB);
                onKeyReleasedCB = (PyObject*)handler;;
            }
        }
        else if(eventType == (int)pyxie::Event::Type::TOUCH) {
            if(eventCode == (int)pyxie::TouchEvent::EventCode::BEGAN) {
                Py_XDECREF(onTouchBeganCB);
                onTouchBeganCB = (PyObject*)handler;;
            }
            else if(eventCode == (int)pyxie::TouchEvent::EventCode::MOVED) {
                Py_XDECREF(onTouchMovedCB);
                onTouchMovedCB = (PyObject*)handler;;
            }
            else if(eventCode == (int)pyxie::TouchEvent::EventCode::ENDED) {
                Py_XDECREF(onTouchEndedCB);
                onTouchEndedCB = (PyObject*)handler;;
            }
            else if(eventCode == (int)pyxie::TouchEvent::EventCode::SCROLLED) {
                Py_XDECREF(onTouchScrolledCB);
                onTouchScrolledCB = (PyObject*)handler;;
            }
        }

        static bool isRegistered = false;
        if(gApp && !isRegistered)
        {
            gApp->getInputHandler()->setInputHandlerFunc(pyxieProcessEventCallbackHandler);
            isRegistered = true;
        }

		static bool isRawHandlerRegistered = false;
		if(eventType == -1) { // All events
			Py_XDECREF(onEventCB);
            onEventCB = (PyObject*)handler;
			if(gApp) {
				gApp->getInputHandler()->setRawInputHandlerFunc(pyxieProcessRawEventCallbackHandler);
				isRawHandlerRegistered = true;
			}
		}        
    }

    PyObject* pyxie_registerEventListener(PyObject* self, PyObject* args) {
		int event_type;
		int event_code;
		PyObject* event_callback_fn;

		if (!PyArg_ParseTuple(args, "iiO", &event_type, &event_code, &event_callback_fn))
			return NULL;

		if (!PyCallable_Check(event_callback_fn)) {
			PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
			return NULL;
		}
		Py_XINCREF(event_callback_fn);

		// Call to pyxie module
		pyxieRegisterEventListener(event_type, event_code, (const void*)event_callback_fn);

		Py_INCREF(Py_None);
		return Py_None;
	}

	PyObject* pyxie_isKeyPressed(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;			
		return PyBool_FromLong(gApp->getInputHandler()->getKeyboard()->isKeyDown(static_cast<KeyCode>(keyCode)));
	}	

	PyObject* pyxie_isKeyReleased(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getKeyboard()->isKeyUp(static_cast<KeyCode>(keyCode)));
	}

	PyObject* pyxie_isKeyHold(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;		
		return PyBool_FromLong(gApp->getInputHandler()->getKeyboard()->isKeyHold(static_cast<KeyCode>(keyCode)));
	}

	PyObject* pyxie_getKeyChar(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;
		auto ch = gApp->getInputHandler()->getKeyboard()->getChar(static_cast<KeyCode>(keyCode));
		return PyUnicode_FromUnicode((const Py_UNICODE*)&ch, 1);
	}

	PyObject* pyxie_getKeyModifier(PyObject* self, PyObject* args) {		
		return PyLong_FromLong(gApp->getInputHandler()->getKeyboard()->getKeyModifier());
	}

	PyObject* pyxie_getFingerPosition(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;
		float posX, posY;
		gApp->getInputHandler()->getTouchDevice()->getFingerPosition(fingerIdx, posX, posY);
		PyObject *tuple = PyTuple_New(2);
		PyTuple_SET_ITEM(tuple, 0, PyLong_FromLong((int)posX));
		PyTuple_SET_ITEM(tuple, 1, PyLong_FromLong((int)posY));
		return tuple;
	}

	PyObject* pyxie_getFingerPressure(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->getFingerPressure(fingerIdx));
	}

	PyObject* pyxie_isFingerPressed(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerPressed(fingerIdx));
	}

	PyObject* pyxie_isFingerMoved(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerMoved(fingerIdx));
	}

	PyObject* pyxie_isFingerReleased(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerReleased(fingerIdx));
	}

	PyObject* pyxie_isFingerScrolled(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerScrolled(fingerIdx));
	}

	PyObject* pyxie_getFingerScrolledData(PyObject* self, PyObject* args) {
		int fingerIdx;
		if (!PyArg_ParseTuple(args, "i", &fingerIdx))
			return NULL;
		float scroll_x, scroll_y;
		bool isInverse;
		gApp->getInputHandler()->getTouchDevice()->getFingerScrolledData(fingerIdx, scroll_x, scroll_y, isInverse);

		PyObject *tuple = PyTuple_New(3);
		PyTuple_SET_ITEM(tuple, 0, PyFloat_FromDouble(scroll_x));
		PyTuple_SET_ITEM(tuple, 1, PyFloat_FromDouble(scroll_y));
		PyTuple_SET_ITEM(tuple, 2, PyBool_FromLong(isInverse));
		return tuple;		
	}

	PyObject* pyxie_getFingersCount(PyObject* self, PyObject* args) {		
		return PyLong_FromLong(gApp->getInputHandler()->getTouchDevice()->getFingersCount());
	}

	PyObject* pyxie_getAllFingers(PyObject* self, PyObject* args) {
		PyObject* list = PyList_New(0);

		auto fingers = gApp->getInputHandler()->getTouchDevice()->getAllFingers();
		for(int i = 0; i < fingers.size(); i++)
		{
			auto finger = fingers[i];
			PyObject* fingerObject = Py_BuildValue(
						"{s:L, s:d, s:d, s:d, s:b, s:b, s:b, s:b, s:d, s:d, s:b}",						
						"id", finger->getFingerId(),						
						"cur_x", finger->getCurrentPosX(),
						"cur_y", finger->getCurrentPosY(),
						"force", finger->getPressure(),					
						"is_pressed", finger->isPressed() ? 1 : 0,
						"is_moved", finger->isMoved() ? 1 : 0,
						"is_released", finger->isReleased() ? 1 : 0,
						"is_scrolled", finger->isScrolled() ? 1 : 0,
						"scroll_x", finger->getScrollX(),
						"scroll_y", finger->getScrollY(),
						"is_flipped", finger->isScrollFlipped() ? 1 : 0
					);
			PyList_Append(list, fingerObject);
		}
		return list;
	}
}
