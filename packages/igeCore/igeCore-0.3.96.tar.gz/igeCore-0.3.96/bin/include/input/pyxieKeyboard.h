///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include <memory>

#include "pyxieEvent.h"

namespace pyxie
{
    enum class KeyCode 
    {
        KEY_NOKEY = -1,

        KEY_0, KEY_1, KEY_2, KEY_3, KEY_4, 
        KEY_5, KEY_6, KEY_7, KEY_8, KEY_9,

        KEY_A, KEY_B, KEY_C, KEY_D, KEY_E,
        KEY_F, KEY_G, KEY_H, KEY_I, KEY_J,
        KEY_K, KEY_L, KEY_M, KEY_N, KEY_O,
        KEY_P, KEY_Q, KEY_R, KEY_S, KEY_T,
        KEY_U, KEY_V, KEY_W, KEY_X, KEY_Y,
        KEY_Z, 

        KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_LEFT, 

        KEY_F1, KEY_F2, KEY_F3, KEY_F4, KEY_F5,
        KEY_F6, KEY_F7, KEY_F8, KEY_F9, KEY_F10,
        KEY_F11, KEY_F12,

        KEY_ESC, KEY_TAB, KEY_BACK, KEY_RETURN,

        KEY_KP0, KEY_KP1, KEY_KP2, KEY_KP3, KEY_KP4, 
        KEY_KP5, KEY_KP6, KEY_KP7, KEY_KP8, KEY_KP9,
        
        KEY_KPPLUS, KEY_KPMINUS, KEY_KPDIV, KEY_KPMULT, KEY_KPENTER,
        KEY_KPPERIOD,

        KEY_PAUSE, KEY_SPACE, KEY_PLUS, KEY_MINUS, KEY_PERIOD, KEY_SLASH, KEY_HASH, KEY_EQUAL, 
        KEY_QUOTE, KEY_BACKQUOTE, KEY_SEMICOLON, KEY_LEFTBRACKET, KEY_RIGHTBRACKET, KEY_BACKSLASH, 
        KEY_COMMA, 

        KEY_INSERT, KEY_DEL, 
        KEY_HOME, KEY_END, 
        KEY_PAGEUP, KEY_PAGEDOWN,
        
        KEY_LCTRL, KEY_RCTRL,
        KEY_LALT, KEY_RALT,
        KEY_LWIN, KEY_RWIN,
        KEY_LSHIFT, KEY_RSHIFT,
        KEY_CAPSLOCK, KEY_NUMLOCK,

        KEY_COUNT
    };
    
    enum class KeyModifier 
    {
        KEY_MOD_NONE	= 0,
        KEY_MOD_CTRL	= 1,
        KEY_MOD_ALT	    = 2,
        KEY_MOD_SHIFT	= 4
    };
    
    class PYXIE_EXPORT KeyboardEvent : public Event
    {
    public:
        enum class EventCode
        {
            PRESSED,
            RELEASED
        };

        KeyboardEvent(KeyCode keyCode, EventCode eventCode, wchar_t key, int keyModifier);        
        virtual ~KeyboardEvent();

        KeyCode getKeyCode() const;
        int getKeyModifier() const;
        EventCode getEventCode() const;
        wchar_t getKey() const;

    protected:
        KeyCode _keyCode;
        EventCode _eventCode;
        int _keyModifier;
        wchar_t _key;

        friend class KeyboardEventListener;
    };

    class PYXIE_EXPORT KeyboardEventListener : public EventListener
    {
    public:
        KeyboardEventListener();
        virtual ~KeyboardEventListener();
        virtual bool init();

        void setOnKeyPressedCallback(std::function<void(std::shared_ptr<Event>)> fn);
        void setOnKeyReleasedCallback(std::function<void(std::shared_ptr<Event>)> fn);

    protected:
        std::function<void(std::shared_ptr<Event>)> onKeyPressed;
        std::function<void(std::shared_ptr<Event>)> onKeyReleased;

        friend class KeyboardEvent;
    };

    class Key 
    {
    private:
        static const uint16_t IS_DOWN_MASK		= 0x8000;
        static const uint16_t WAS_DOWN_MASK		= 0x4000;            
        static const uint16_t DOWN_COUNT_MASK	= 0x3FFF;

    public:
        Key();
        virtual ~Key();

        bool isDown() const;
        bool isUp() const;
        bool isHold() const;

        bool wasPressed() const;
        bool wasReleased() const;

        int getDownCount() const;
        int getUpCount() const;

        uint16_t getValue() const;
        void setValue(uint16_t value);
        
        void reset();
        void update(bool isPressed);

    protected:
        uint16_t _state;
        uint16_t _value;

        bool wasDown() const;
        bool wasUp() const;
    };
    
    class PYXIE_EXPORT Keyboard
    {
    public:
        Keyboard();
        virtual ~Keyboard();
        
        void update();
		void setEventDispatcher(std::shared_ptr<EventDispatcher> dispatcher);
        void clearKeys();

        bool isKeyDown(KeyCode kc) const;
        bool isKeyUp(KeyCode kc) const;      
		bool isKeyHold(KeyCode kc) const;
        int getKeyModifier();

        wchar_t getChar(KeyCode kc) const;
        wchar_t getShiftChar(KeyCode kc) const;

        void dispatchKeyEvent(KeyCode keyCode, KeyboardEvent::EventCode eventCode, int modifiers);
        void dispatchKeyEvent(KeyCode keyCode, KeyboardEvent::EventCode eventCode);		

    protected:
        Key _keys[(int)KeyCode::KEY_COUNT];
        wchar_t _chars[(int)KeyCode::KEY_COUNT];
        wchar_t _shiftChars[(int)KeyCode::KEY_COUNT];
        std::shared_ptr<EventDispatcher> mEventDispatcher;
    };
}
