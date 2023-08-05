///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#include "pyxie.h"
#include "bitmapHelper.h"
#include "pyxieResourceManager.h"
#include "pyxieSystemInfo.h"
#include "pyxieTexture.h"

#include <string> 
#include <locale> 
#include <codecvt> 
#include <map> 

#define STB_TRUETYPE_IMPLEMENTATION 
#include "stb_truetype.h"


#ifdef _WIN32
#define SHORT_CHAR wchar_t
#define SHORT_STRING wstring
#else
#define SHORT_CHAR char16_t
#define SHORT_STRING u16string
#endif

namespace pyxie
{
	void FlipY(uint8_t* inimg, uint8_t* outimg, int w, int h) {
		auto inp = inimg + (w * (h - 1));
		auto outp = outimg;
		for (int y = 0; y < h; y++) {
			memcpy(outp, inp, w);
			outp += w;
			inp -= w;
		}
	}

	void FlipRGBY(uint8_t* data, int width, int height)
	{
		uint8_t rgb[3];

		for (int y = 0; y < height / 2; ++y)
		{
			for (int x = 0; x < width; ++x)
			{
				int top = (x + y * width) * 3;
				int bottom = (x + (height - y - 1) * width) * 3;

				memcpy(rgb, data + top, sizeof(rgb));
				memcpy(data + top, data + bottom, sizeof(rgb));
				memcpy(data + bottom, rgb, sizeof(rgb));
			}
		}
	}

	void FlipRGBAY(uint8_t* data, int width, int height)
	{
		uint8_t rgb[4];

		for (int y = 0; y < height / 2; ++y)
		{
			for (int x = 0; x < width; ++x)
			{
				int top = (x + y * width) * 4;
				int bottom = (x + (height - y - 1) * width) * 4;

				memcpy(rgb, data + top, sizeof(rgb));
				memcpy(data + top, data + bottom, sizeof(rgb));
				memcpy(data + bottom, rgb, sizeof(rgb));
			}
		}
	}

	void renderText(const char* word, int fontsize, stbtt_fontinfo* info, uint8_t* bitmap, int& w, int& h) {

		/* calculate font scaling */
		float scale = stbtt_ScaleForPixelHeight(info, fontsize);

		int x = 0;
		int maxx = 0;

		int ascent, descent, lineGap;
		stbtt_GetFontVMetrics(info, &ascent, &descent, &lineGap);

		ascent *= scale;
		descent *= scale;


		int lineH = ascent - descent;
		int Y = 0;


		std::string source(word);
		std::wstring_convert<std::codecvt_utf8_utf16<SHORT_CHAR>, SHORT_CHAR> convert;
		std::SHORT_STRING dest = convert.from_bytes(source);

		int roop = dest.size();
		for (int i = 0; i < roop; i++) {

			if (dest[i] == '\n') {
				Y+=lineH+1;
				lineH = ascent - descent;
				if (maxx < x) maxx = x;
				x = 0;
				continue;
			}

			/* get bounding box for character (may be offset to account for chars that dip above or below the line */
			int c_x1, c_y1, c_x2, c_y2;
			stbtt_GetCodepointBitmapBox(info, dest[i], scale, scale, &c_x1, &c_y1, &c_x2, &c_y2);

			if (ascent + c_y2 > lineH) lineH = ascent + c_y2;

			/* compute y (different characters have different heights */
			int y = Y + ascent + c_y1;
			if (y < 0) y = 0;

			/* how wide is this character */
			int ax;
			stbtt_GetCodepointHMetrics(info, dest[i], &ax, 0);
			int w1 = ax * scale;
			int w2 = (c_x2 - c_x1);
			int ww = w1 > w2 ? w1 : w2;


			/* render character (stride and offset is important here) */
			if (bitmap) {

				if (x + ww < w && y < h) {
					int byteOffset = x + (y * w);
					stbtt_MakeCodepointBitmap(info, bitmap + byteOffset, c_x2 - c_x1, c_y2 - c_y1, w, scale, scale, dest[i]);
				}
			}

			
			//int ww = (c_x2 - c_x1);
			//if(ww ==0) ww = ax * scale;
			//x += ax * scale;
			x +=ww;

			/* add kerning */
			int kern;
			kern = stbtt_GetCodepointKernAdvance(info, dest[i], dest[i + 1]);
			x += kern * scale;
		}

		if (maxx < x) maxx = x;
		w = maxx+1;
		h = Y+ lineH+1;

	}



	/*Once loaded, the font data is cached.
      This is a temporary implementation and will eventually implement smart garbage collection.*/
	static std::map<uint32_t, stbtt_fontinfo*> fontbuffers;

	PyObject* createTextImage(const char* word, const char* fontpath, int fontsize, int texw, int texh) {

		//pyxie::pyxieSystemInfo& sysinfo = pyxie::pyxieSystemInfo::Instance();
		//fontsize = sysinfo.GameToDevH(fontsize);

		stbtt_fontinfo* info = nullptr;
		uint32_t hash = pyxie::GenerateNameHash(fontpath);
		auto it = fontbuffers.find(hash);
		if (it == fontbuffers.end()) {
			void* fontBuffer;
			int fontBufferSize;
			pyxie::pyxieResourceManager::Instance().ReadFile(fontpath, fontBuffer, fontBufferSize);
			info = (stbtt_fontinfo*)pyxie::PYXIE_MALLOC(sizeof(stbtt_fontinfo));
			stbtt_InitFont(info, (uint8_t*)fontBuffer, 0);
			fontbuffers[hash] = info;
		}
		else {
			info = fontbuffers[hash];
		}

		int b_w = texw;
		int b_h = texh;
		int l_h = fontsize;

		/* create a bitmap for the phrase */
		unsigned char* bitmap = (unsigned char*)pyxie::PYXIE_MALLOC(texw * texh);
		memset(bitmap, 0, texw * texh);

		renderText(word, fontsize, info, bitmap, b_w, b_h);

		unsigned char* bitmap2 = (unsigned char*)pyxie::PYXIE_MALLOC(texw * texh);
		FlipY(bitmap, bitmap2, texw, texh);

		PyObject* obj = PyBytes_FromStringAndSize((char*)bitmap2, texw * texh);
		pyxie::PYXIE_FREE(bitmap);
		pyxie::PYXIE_FREE(bitmap2);
		//PYXIE_FREE(fontBuffer);

		return obj;
	}

	PyObject* calcTextSize(const char* word, const char* fontpath, int fontsize) {

		//pyxie::pyxieSystemInfo& sysinfo = pyxie::pyxieSystemInfo::Instance();
		//fontsize = sysinfo.GameToDevH(fontsize);

		stbtt_fontinfo* info = nullptr;
		uint32_t hash = pyxie::GenerateNameHash(fontpath);
		auto it = fontbuffers.find(hash);
		if (it == fontbuffers.end()) {
			void* fontBuffer;
			int fontBufferSize;
			pyxie::pyxieResourceManager::Instance().ReadFile(fontpath, fontBuffer, fontBufferSize);
			if (fontBufferSize == 0) {
				PyErr_SetString(PyExc_FileNotFoundError, fontpath);
				return nullptr;
			}
			info = (stbtt_fontinfo*)pyxie::PYXIE_MALLOC(sizeof(stbtt_fontinfo));
			stbtt_InitFont(info, (uint8_t*)fontBuffer, 0);
			fontbuffers[hash] = info;
		}
		else {
			info = fontbuffers[hash];
		}
		int w = -1;
		int h = -1;
		renderText(word, fontsize, info, nullptr, w, h);

		w = (w / 8) * 8 + ((w % 8) ? 8 : 0);
		//h = 128;

		PyObject* wh = PyTuple_New(2);
		PyTuple_SetItem(wh, 0, PyLong_FromLong(w));
		PyTuple_SetItem(wh, 1, PyLong_FromLong(h));
		return wh;
	}

	PyObject* createCheckeredTexture(uint8_t red, uint8_t green, uint8_t blue, uint8_t alpha, int texWidth, int texHeight, int format)

	{
		int bitSize = pyxie::pyxieTexture::GetBitSize(format);
		if (bitSize == 0) return nullptr;

		char colorbuff[4];
		switch (format) {
		case GL_RED: colorbuff[0] = red; break;
		case GL_RGB: colorbuff[0] = red; colorbuff[1] = green; colorbuff[2] = blue; break;
		case GL_RGBA: colorbuff[0] = red; colorbuff[1] = green; colorbuff[2] = blue; colorbuff[3] = alpha; break;
		}

		uint8_t* image = (uint8_t*)PYXIE_MALLOC(texWidth * texHeight * bitSize);
		for (int i = 0; i < texWidth; i++) {
			for (int j = 0; j < texHeight; j++) {
				int a = i < texWidth / 2 ? 1 : 0;
				int b = j < texWidth / 2 ? 1 : 0;
				if (a == b) {
					for (int k = 0; k < bitSize; k++)
						image[(i + j * texWidth) * bitSize + k] = colorbuff[k];
				}
				else {
					for (int k = 0; k < bitSize; k++)
						image[(i + j * texWidth) * bitSize + k] = 255;
				}
			}
		}
		PyObject* obj = PyBytes_FromStringAndSize((char*)image, texWidth * texHeight * bitSize);
		PYXIE_FREE(image);
		return obj;
	}
	PyObject* createColorTexture(uint8_t red, uint8_t green, uint8_t blue, uint8_t alpha, int texWidth, int texHeight, int format)
	{
		int bitSize = pyxieTexture::GetBitSize(format);
		if (bitSize == 0) return nullptr;

		char colorbuff[4];
		switch (format) {
		case GL_RED: colorbuff[0] = red; break;
		case GL_RGB: colorbuff[0] = red; colorbuff[1] = green; colorbuff[2] = blue; break;
		case GL_RGBA: colorbuff[0] = red; colorbuff[1] = green; colorbuff[2] = blue; colorbuff[3] = alpha; break;
		}

		uint8_t* image = (uint8_t*)PYXIE_MALLOC(texWidth * texHeight * bitSize);
		for (int i = 0; i < texWidth; i++) {
			for (int j = 0; j < texHeight; j++) {
				for (int k = 0; k < bitSize; k++)
					image[(i + j * texWidth) * bitSize + k] = colorbuff[k];
			}
		}
		PyObject* obj = PyBytes_FromStringAndSize((char*)image, texWidth * texHeight * bitSize);
		PYXIE_FREE(image);
		return obj;
	}
}
