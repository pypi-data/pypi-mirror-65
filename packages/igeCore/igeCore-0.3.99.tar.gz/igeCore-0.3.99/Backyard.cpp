#include "pyxie.h"
#include "Backyard.h"
#include "pyxieShowcase.h"
#include "pyxieFigure.h"
#include "pyxieCamera.h"
#include "pyxieRenderContext.h"
#include "pyxieRenderTarget.h"
#include "pyxieTime.h"
#include "pyxieProfiler.h"
#include "pyxieFios.h"

#include <map>
#include <queue>
#include <mutex>
#include <thread>
#include <vector>
#include <iostream>
#include <exception>
#include <Python.h>

#include "pythonResource.h"
#include "numpy/ndarrayobject.h"

#include "bitmapHelper.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include <stb_image_write.h>

namespace pyxie {
	std::vector<texture_obj*> imageUpdateList;
	void Backyard::UpdateImageRequest(void* tex) {
		if (((texture_obj*)tex)->subImage) {
			Py_INCREF(((texture_obj*)tex)->subImage);
		}
		Py_INCREF((texture_obj*)tex);
		imageUpdateList.push_back((texture_obj*)tex);
	}

	std::map<std::string, texture_obj*> captureUpdateList;
	void Backyard::UpdateCaptureRequest(void* tex, std::string captureName)
	{
		captureUpdateList[captureName] = (texture_obj*)tex;
	}

	struct RenderSet {
		pyxieCamera* camera;
		pyxieShowcase* showcas;
		pyxieRenderTarget* offscreen;
		bool clearColor;
		bool colearDepth;
		Vec4 color;
	};
	std::vector<RenderSet> renderSets;

	Backyard* Backyard::instance;
	Backyard& Backyard::Instance() { return *instance; }

	Backyard::~Backyard() {
		for (auto itr = renderSets.begin(); itr != renderSets.end(); ++itr) {
			(*itr).camera->DecReference();
			(*itr).showcas->DecReference();
		}
		renderSets.clear();
		PYXIE_SAFE_FREE(m_CaptureData);
	}

	void Backyard::Delete() {		
		PYXIE_SAFE_DELETE(instance); 
	}

	void Backyard::RenderRequest(pyxieCamera* camera, pyxieShowcase* showcase, pyxieRenderTarget* offscreen, bool clearColor, bool clearDepth, const float* color){
		camera->IncReference();
		showcase->IncReference();

		RenderSet rset;
		rset.camera = camera;
		rset.showcas = showcase;
		rset.offscreen = offscreen;
		rset.clearColor = clearColor;
		rset.colearDepth = clearDepth;
		rset.color = Vec4(color[0], color[1], color[2], color[3]);
		renderSets.push_back(rset);
	}

	void Backyard::Render() {
		PyxieZoneScoped;
		for (auto itr = imageUpdateList.begin(); itr != imageUpdateList.end(); ++itr) {
			if ((*itr)->subImage) {
				uint8_t* bmp = NULL;
				int w, h, x, y;
				if (PyBytes_Check((*itr)->subImage)) {
					bmp = (uint8_t*)PyBytes_AsString((*itr)->subImage);
					x = (*itr)->x;
					y = (*itr)->y;
					w = (*itr)->w;
					h = (*itr)->h;
				}
				else if ((*itr)->subImage->ob_type->tp_name && strcmp((*itr)->subImage->ob_type->tp_name, "numpy.ndarray") == 0) {
					PyArrayObject_fields* ndarray = (PyArrayObject_fields*)(*itr)->subImage;
					bmp = (uint8_t*)ndarray->data;
					x = (*itr)->x;
					y = (*itr)->y;
					h = *ndarray->dimensions;
					w = *ndarray->strides / ndarray->nd;
				}
				if(bmp) (*itr)->colortexture->UpdateSubImage(bmp, x, y, w, h);
				Py_DECREF((*itr)->subImage);
				Py_DECREF(*itr);
			}
		}
		imageUpdateList.clear();

		pyxieRenderContext& renderContext = pyxieRenderContext::Instance();

		for (auto itr = renderSets.begin(); itr != renderSets.end(); ++itr) {
			{
				PyxieZoneScopedN("BeginScene");
				renderContext.BeginScene((*itr).offscreen, (*itr).color, (*itr).clearColor, (*itr).colearDepth);
			}			
			{
				PyxieZoneScopedN("showcas Update");
				(*itr).showcas->Update(0.0f);
			}
			{
				PyxieZoneScopedN("camera Render");
				(*itr).camera->Render();
			}
			{
				PyxieZoneScopedN("showcas Render");
				(*itr).showcas->Render();
			}
			
			{
				PyxieZoneScopedN("EndScene");
				renderContext.EndScene();
			}
			
			(*itr).camera->DecReference();
			(*itr).showcas->DecReference();
		}
		renderSets.clear();
	}

	void Backyard::UpdateCapturing()
	{
		PyxieZoneScoped;		
		if (!captureUpdateList.empty())
		{
			m_Executor.wait_for_all();
			m_Taskflow.clear();
		}
		for (auto itr = captureUpdateList.begin(); itr != captureUpdateList.end(); ++itr) {
			int width, height;

			std::string path;
			path += pyxieFios::Instance().GetRoot();
			char name[256];
			
			sprintf(name, "%s.png", itr->first.c_str());
			path += name;
			
			if (itr->second->renderTarget)
			{
				int width = itr->second->renderTarget->GetWidth();
				int height = itr->second->renderTarget->GetHeight();

				uint8_t* rtData = (uint8_t*)PYXIE_MALLOC(width * height * 4 * sizeof(uint8_t));
				bool result = itr->second->renderTarget->ReadColorBufferImage(rtData);
				if (result == true)
				{
					m_Taskflow.emplace(
						[this, rtData, width, height, path]() {
							FlipRGBAY(rtData, width, height);
							int result = stbi_write_png(path.c_str(), width, height, 4, rtData, 0);
							PYXIE_FREE(rtData);
						}
					);
				}
			}
			else
			{
				pyxieTexture::ReadPixels(m_CaptureData, width, height);

				if (m_CaptureData)
				{
					itr->second->colortexture->UpdateWholeImage(m_CaptureData, 0, 0, width, height);					

					m_Taskflow.emplace(
						[this, width, height, path]() {
							PyxieZoneScopedN("Capturing");
							FlipRGBAY(m_CaptureData, width, height);
							int result = stbi_write_png(path.c_str(), width, height, 4, m_CaptureData, 0);
						}
					);
				}
			}			


			if (!m_Taskflow.empty())
			{
				m_Executor.run(m_Taskflow);
			}
			break;
		}
		captureUpdateList.clear();
	}
}
