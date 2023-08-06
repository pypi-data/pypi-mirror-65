///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once
#include "Python.h"
namespace pyxie
{
	PyObject* createTextImage(const char* word, const char* fontpath, int fontsize, int texw, int texh);
	PyObject* calcTextSize(const char* word, const char* fontpath, int fontsize);
	PyObject* createCheckeredTexture(uint8_t red, uint8_t green, uint8_t blue, uint8_t alpha, int texWidth, int texHeight, int format);
	PyObject* createColorTexture(uint8_t red, uint8_t green, uint8_t blue, uint8_t alpha, int texWidth, int texHeight, int format);
	void FlipRGBY(uint8_t* data, int width, int height);
	void FlipRGBAY(uint8_t* data, int width, int height);
}