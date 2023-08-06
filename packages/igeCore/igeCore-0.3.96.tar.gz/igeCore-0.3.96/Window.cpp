#include "pyxie.h"
#include "Window.h"
#include <python.h>
#include <thread>
#include <mutex>

#include "pyxieApplication.h"
#include "pyxieFios.h"
#include "pyxieTouchManager.h"
#include "pyxieResourceManager.h"
#include "pyxieRenderContext.h"
#include "pyxieShader.h"
#include "pyxieSystemInfo.h"

std::shared_ptr<pyxie::pyxieApplication> gApp;

PyMODINIT_FUNC _PyInit__igeCore();

PyMODINIT_FUNC PyInit__igeCore() {
	gApp = std::make_shared<pyxie::pyxieApplication>();
	gApp->createAppWindow();
	
	return _PyInit__igeCore();
}
