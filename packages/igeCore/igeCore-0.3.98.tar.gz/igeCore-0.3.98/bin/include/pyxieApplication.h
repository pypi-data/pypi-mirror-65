///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include <thread>
#include <mutex>

#include "pyxieObject.h"

struct SDL_Window;
typedef void *SDL_GLContext;

namespace pyxie
{
    class InputHandler;

	class PYXIE_EXPORT pyxieApplication : public pyxieObject
	{
	public:
		pyxieApplication();
		virtual ~pyxieApplication();

		virtual bool onInit(DeviceHandle dh);
		virtual void onShutdown();
		virtual bool onUpdate();
		virtual void onSize(int scrW, int scrH);
		virtual void onRender();

		bool isInitialized() const;
        bool isRunning() const;
        std::shared_ptr<InputHandler> getInputHandler();

        virtual void createAppWindow();
        virtual void showAppWindow(bool show = true, int width = -1, int height = -1, bool resizable = true);
	
        virtual bool initialize();
        virtual void update();
        virtual void handleEvents();
        virtual void destroy();
        bool swap();
        void* getAppWindow();

    protected:
        SDL_Window* mWindow;
        SDL_GLContext mContext;
        std::shared_ptr<InputHandler> mInputHandler;

        int mScreenWidth;
        int mScreenHeight;
        bool mSizeChanged;

        bool mShowWindow;
        bool mWindowResizable;
        bool mWindowChanged;

        bool mIsRunning;
        bool mIsInitialized;        
	};
}
