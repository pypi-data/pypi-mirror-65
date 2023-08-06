///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include "pyxieResource.h"
#include "pyxieFigurestruct.h"

#ifndef GL_RED
#define GL_RED 0x1903
#define GL_RGB 0x1907
#define GL_RGBA 0x1908
#endif

namespace pyxie
{
	constexpr uint8_t KtxIdentifier[12] = { 0xAB, 0x4B, 0x54, 0x58, 0x20, 0x31, 0x31, 0xBB, 0x0D, 0x0A, 0x1A, 0x0A };

	typedef unsigned int TextureHandle;

	struct ktxheader {
		char identifier[12];
		uint32_t endianness;
		uint32_t glType;
		uint32_t glTypeSize;
		uint32_t glFormat;
		uint32_t glInternalFormat;
		uint32_t glBaseInternalFormat;
		uint32_t pixelWidth;
		uint32_t pixelHeight;
		uint32_t pixelDepth;
		uint32_t numberOfArrayElements;
		uint32_t numberOfFaces;
		uint32_t numberOfMipmapLevels;
		uint32_t bytesOfKeyValueData;
	};

	class PYXIE_EXPORT pyxieTexture : public pyxieResource{
		TextureHandle		texHandle;
		uint8_t*			image;

		uint32_t			textureType;
		uint32_t			width;
		uint32_t			height;
		uint32_t			color;
		uint32_t			numMips;
		uint32_t			format;
		//bool				useAlphaChannel;
		SamplerState		currentState;
		bool				fromFile;

	public:
		pyxieTexture(const char* path);
		pyxieTexture(uint32_t w, uint32_t h, int format, uint32_t col, const char* name);
		pyxieTexture(uint8_t* img, const char* name);
		pyxieTexture(pyxieTexture* org);
		~pyxieTexture();

		void Build();
		void Initialize();
		void Clone(bool afterFinishBuild);
		RESOURCETYPE ResourceType() { return TEXTURETYPE; }

		inline TextureHandle GetTextureHandle(){
			WaitInitialize();
			return texHandle;
		}
		inline uint32_t GetTextureType(){
			WaitInitialize();
			return textureType;
		}
		inline uint32_t GetTextureWidth() {
			WaitBuild();
			return width;
		}
		inline uint32_t GetTextureHeight() { 
			WaitBuild();
			return height;
		}
		inline uint32_t GetNumMips() {
			WaitBuild();
			return numMips;
		}
		inline int GetFormat() {
			WaitBuild();
			return format;
		}
		void SetSamplerState(SamplerState state);

		void UpdateSubImage(uint8_t* bmp, int x, int y, int w, int h);
		void UpdateWholeImage(uint8_t* bmp, int x, int y, int w, int h);

		static int GetBitSize(int texFormat);
		static void ReadPixels(uint8_t* &output, int& width, int& height);
		void ReadPixels(char* outbuffer);

#if defined __ENABLE_SUSPEND_RECOVER__
		virtual bool Restore();
		virtual bool Release();
#endif
	private:
		void ClearMember();
		
	};
}
