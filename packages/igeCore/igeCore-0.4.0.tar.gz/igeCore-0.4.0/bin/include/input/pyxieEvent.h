///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include <memory>
#include <string>
#include <functional>
#include <unordered_map>
#include <atomic>

#include "pyxieThread.h"

namespace pyxie
{
    class EventListener;
    class EventDispatcher;

    class PYXIE_EXPORT Event
    {
    public:
        enum class Type 
        {
            SYSTEM,            
            TOUCH,
            KEYBOARD,
            CUSTOM
        };

        Event(Type type);
        virtual ~Event();

        Type getType() const;
        bool isStopped() const;

        // call stop to stop spreading event to further listeners
        void stop();

    protected:
        Type _type;
        bool _isStopped; 

        friend class EventDispatcher;
    };

    class PYXIE_EXPORT EventListener
    {
    public:
        enum class Type 
        {
            SYSTEM,            
            TOUCH,
            KEYBOARD,
            CUSTOM
        };

        enum class Priority 
        {
            LOW,
            MEDIUM,
            HIGH
        };

        EventListener(Type type, const std::string& listenerID);
        virtual ~EventListener();

        virtual bool init();
        void setCallback(const std::function<void(std::shared_ptr<Event>)>& callback);
        EventListener::Type getType() const;
        const std::string& getListenerID() const;

        void setPriority(EventListener::Priority prio);
        EventListener::Priority getPriority() const;

    protected:
        Type _type;
        std::string _id;
        std::function<void(std::shared_ptr<Event>)> _onEvent;
        Priority _priority;

        friend class EventDispatcher;
    };

    class PYXIE_EXPORT EventDispatcher
    {
    public:
        EventDispatcher();
        virtual ~EventDispatcher();

        void addEventListener(std::shared_ptr<EventListener> listener, EventListener::Priority prio);
        void removeEventListener(std::shared_ptr<EventListener> listener);
        void removeAllEventListeners();
        bool hasEventListener(const std::string& listenerID) const;

        void SetEnable(bool isEnable = true);
        bool IsEnabled() const;

        void dispatchEvent(std::shared_ptr<Event> event);

    protected:
        std::string getEventListenerID(std::shared_ptr<Event> event) const;
        void sortEventListeners(const std::string& listenerID);
        void setPriorityDirty(std::string listenerID, bool isPriorityDirty);

        std::unordered_map<std::string, std::shared_ptr<std::vector<std::shared_ptr<EventListener>>>> _listenerMap;
        std::unordered_map<std::string, bool> _priorityDirtyMap;

        bool _isEnabled;
        std::shared_ptr<Semaphore> _semaphore;

        friend class EventListener;
    };
}
