///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include "pyxieEvent.h"

union SDL_Event;

namespace pyxie
{
    class Keyboard;
    class KeyboardEvent;
    class KeyboardEventListener;

    class TouchDevice;
    class TouchEvent;
    class TouchEventListener;	

    typedef void (*InputHandlerFunc)(const void* event);

    class PYXIE_EXPORT InputHandler
    {
    public:
        InputHandler();
        virtual ~InputHandler();

        void update();
        bool handleEvent(const SDL_Event& event);

        virtual void onInputEvent(std::shared_ptr<Event> event);
        void setInputHandlerFunc(InputHandlerFunc func);
        void setRawInputHandlerFunc(InputHandlerFunc func);

        std::shared_ptr<EventDispatcher> getEventDispatcher();
        std::shared_ptr<KeyboardEventListener> getKeyEventListener();
        std::shared_ptr<TouchEventListener> getTouchEventListener();

		std::shared_ptr<Keyboard> getKeyboard();
        std::shared_ptr<TouchDevice> getTouchDevice();

    protected:
        std::shared_ptr<KeyboardEventListener> mKeyEventListener;
        std::shared_ptr<TouchEventListener> mTouchEventListener;
        std::shared_ptr<EventDispatcher> mEventDispatcher;
        std::shared_ptr<Keyboard> mKeyboard;
        std::shared_ptr<TouchDevice> mTouchDevice;
        InputHandlerFunc mInputHandlerFunc;
        InputHandlerFunc mRawInputHandlerFunc;
    };
}