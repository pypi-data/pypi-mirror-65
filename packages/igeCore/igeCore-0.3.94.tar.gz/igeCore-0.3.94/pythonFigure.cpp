#include "pyxie.h"
#include "pythonResource.h"
#include "pyxieResourceCreator.h"
#include "pyxieTime.h"
#include "pyVectorMath.h"
#include "pythonFigure_doc_en.h"

namespace pyxie
{
	static int GetMaterialIndex(pyxieFigure* obj, PyObject* arg) {
		int index = -1;
		if (PyLong_Check(arg)) {
			index = PyLong_AsLong(arg);
		}
		else if (PyUnicode_Check(arg)) {
			Py_ssize_t data_len;
			const char* key_str = PyUnicode_AsUTF8AndSize(arg, &data_len);
			index = obj->GetMaterialIndex(GenerateNameHash(key_str));
		}
		if (index == -1) {
			char error[256] = { 0 };
			sprintf(error, "material not found: %s", obj->ResourceName());
			PyErr_SetString(PyExc_TypeError, (const char*)error);
		}
		return index;
	}
	static int GetMeshIndex(pyxieFigure* obj, PyObject* arg) {
		int index = -1;
		if (PyLong_Check(arg)) {
			index = PyLong_AsLong(arg);
		}
		else if (PyUnicode_Check(arg)) {
			Py_ssize_t data_len;
			const char* key_str = PyUnicode_AsUTF8AndSize(arg, &data_len);
			index = obj->GetMeshIndex(GenerateNameHash(key_str));
		}
		if (index == -1) {
			char error[256] = { 0 };
			sprintf(error, "mesh not found: %s", obj->ResourceName());
			PyErr_SetString(PyExc_TypeError, (const char*)error);
		}
		return index;
	}

	PyObject *figure_new(PyTypeObject *type, PyObject *args, PyObject *kw) {
		char* path;
		figure_obj * self = NULL;

		if (PyArg_ParseTuple(args, "s", &path)) {
			self = (figure_obj*)type->tp_alloc(type, 0);
			self->figure = pyxieResourceCreator::Instance().NewFigure(path);
		}
		return (PyObject *)self;
	}

	void  figure_dealloc(figure_obj *self)
	{
		if(!IsTerminate()) self->figure->DecReference();
		Py_TYPE(self)->tp_free(self);
	}

	PyObject *figure_str(figure_obj *self)
	{
		char buf[64];
		pyxie_snprintf(buf, 64, "figure object");
		return _PyUnicode_FromASCII(buf, strlen(buf));
	}

	PyObject* figure_getPosition(figure_obj* self)
	{
		vec_obj* v3robj = PyObject_New(vec_obj, _Vec3Type);
		if (!v3robj) return NULL;
		vmath_cpy(self->figure->GetPosition().P(), 3, v3robj->v);
		v3robj->d = 3;
		return (PyObject*)v3robj;
	}

	int figure_setPosition(figure_obj* self, PyObject* value)
	{
		int d1;
		float buff[4];
		float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
		if (!v1) return -1;
		self->figure->SetPosition(*((Vec3*)v1));
		return 0;
	}

	PyObject* figure_getRotation(figure_obj* self)
	{
		vec_obj* quatobj = PyObject_New(vec_obj, _QuatType);
		if (!quatobj) return NULL;
		vmath_cpy(self->figure->GetRotation().P(), 4, quatobj->v);
		quatobj->d = 4;
		return (PyObject*)quatobj;
	}
	int figure_setRotation(figure_obj* self, PyObject* value)
	{
		int d1;
		float buff[4];
		float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
		if (!v1) return -1;
		self->figure->SetRotation(*((Quat*)v1));
		return 0;
	}

	PyObject* figure_getScale(figure_obj* self)
	{
		vec_obj* v3robj = PyObject_New(vec_obj, _Vec3Type);
		if (!v3robj) return NULL;
		vmath_cpy(self->figure->GetScale().P(), 3, v3robj->v);
		v3robj->d = 3;
		return (PyObject*)v3robj;
	}
	int figure_setScale(figure_obj* self, PyObject* value)
	{
		int d1;
		float buff[4];
		float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
		if (!v1) return -1;
		self->figure->SetScale(*((Vec3*)v1));
		return 0;
	}

	PyObject* figure_numJoints(figure_obj* self)
	{
		return PyLong_FromLong(self->figure->NumJoints());
	}
	PyObject* figure_numMeshes(figure_obj* self)
	{
		return PyLong_FromLong(self->figure->NumMeshes());
	}
	PyObject* figure_numMaterials(figure_obj* self)
	{
		return PyLong_FromLong(self->figure->NumMaterials());
	}
	PyObject* figure_numAnimations(figure_obj* self)
	{
		return PyLong_FromLong(self->figure->NumAnimations());
	}
	PyObject* figure_numEmbeddedAnimations(figure_obj* self)
	{
		return PyLong_FromLong(self->figure->NumEmbeddedAnimations());
	}
	PyObject* figure_numTextures(figure_obj* self)
	{
		return PyLong_FromLong(self->figure->NumTextures());
	}

	static PyObject *figure_BindAnimator(figure_obj *self, PyObject *args)
	{
		int slot = 0;
		PyObject* arg2=nullptr;

		if (PyArg_ParseTuple(args, "i|O", &slot, &arg2)){
			if (arg2) {
				if (PyUnicode_Check(arg2)) {
					const char* motionName = PyUnicode_AsUTF8(arg2);
					self->figure->BindAnimator((pyxieFigure::AnimatorSlot)slot, motionName);
				}
				else if (arg2->ob_type == &AnimatorType) {
					animator_obj* anime = (animator_obj*)arg2;
					self->figure->BindAnimator((pyxieFigure::AnimatorSlot)slot, anime->anime);
				}
				else{
					PyErr_SetString(PyExc_TypeError, "Argument of connectAnimator must be (integer, animator) or (integer) if unbind.");
					return NULL;
				}
			}
			else {
				self->figure->BindAnimator((pyxieFigure::AnimatorSlot)slot, (pyxieAnimator*)nullptr);
			}
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject *figure_GetCamera(figure_obj *self, PyObject *args)
	{
		char* name = NULL;
		if (!PyArg_ParseTuple(args, "|s", &name))
			return NULL;

		camera_obj *obj = PyObject_New(camera_obj, &CameraType);
		obj->camera = pyxieResourceCreator::Instance().NewCamera(name, self->figure);
		obj->parent = (PyObject*)self;
		Py_INCREF(self);
		return (PyObject *)obj;
	}

	static PyObject *figure_GetEnvironment(figure_obj *self)
	{
		environment_obj *obj = PyObject_New(environment_obj, &EnvironmentType);
		obj->envSet = pyxieResourceCreator::Instance().NewEnvironmentSet(self->figure);
		obj->parent = (PyObject*)self;
		Py_INCREF(self);
		return (PyObject *)obj;
	}

	static PyObject* figure_getEmbeddedAnimator(figure_obj* self, PyObject* args)
	{
		char* name;
		if (!PyArg_ParseTuple(args, "s", &name)) return NULL;

		pyxieAnimator* anim = self->figure->GetEmbeddedAnimator(GenerateNameHash(name));
		if (!anim) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		animator_obj* obj = PyObject_New(animator_obj, &AnimatorType);
		obj->anime = anim;
		obj->anime->IncReference(); // incref
		obj->parent = (PyObject*)self;
		Py_INCREF(self);

		return (PyObject*)obj;
	}


	static PyObject *figure_Step(figure_obj *self, PyObject *args){
		float s = FLT_MAX;
		if (!PyArg_ParseTuple(args, "|f", &s))return NULL;
		if (s == FLT_MAX) s = (float)pyxieTime::Instance().GetElapsedTime();
		self->figure->Step(s);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_SetTime(figure_obj* self, PyObject* args) {
		float s;
		if (!PyArg_ParseTuple(args, "f", &s))return NULL;
		self->figure->SetEvalTime(s);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_Dump(figure_obj* self, PyObject* args) {
		char* file;
		if (!PyArg_ParseTuple(args, "s", &file))return NULL;
		self->figure->Dump(file);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_setBlendingWeight(figure_obj* self, PyObject* args) {
		int slot;
		float value;
		if (!PyArg_ParseTuple(args, "if", &slot, &value))return NULL;
		self->figure->SetBlendingWeight(slot, value);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_getBlendingWeight(figure_obj* self, PyObject* args) {
		int slot;
		if (!PyArg_ParseTuple(args, "i", &slot))return NULL;
		float value  = self->figure->GetBlendingWeight(slot);
		return PyFloat_FromDouble(value);
	}


	static PyObject* figure_getJoint(figure_obj* self, PyObject* args) {

		PyObject* arg;
		Space space = WorldSpace;
		if (!PyArg_ParseTuple(args, "O|i", &arg, &space))return NULL;

		int index = GetJointIndex(self->figure, arg);
		if (index == -1) return NULL;
		Joint joint = self->figure->GetJoint(index, space);

		PyObject* joint_obj = PyTuple_New(3);

		vec_obj* pos = (vec_obj*)PyObject_New(vec_obj, _Vec3Type);
		vec_obj* rot = (vec_obj*)PyObject_New(vec_obj, _QuatType);
		vec_obj* scale = (vec_obj*)PyObject_New(vec_obj, _Vec3Type);
		for (int i = 0; i < 4; i++) {
			pos->v[i] = joint.translation[i];
			rot->v[i] = joint.rotation[i];
			scale->v[i] = joint.scale[i];
		}
		pos->d = 3;
		rot->d = 4;
		scale->d = 3;

		PyTuple_SetItem(joint_obj, 0, (PyObject*)pos);
		PyTuple_SetItem(joint_obj, 1, (PyObject*)rot);
		PyTuple_SetItem(joint_obj, 2, (PyObject*)scale);
		return joint_obj;
	}

	static PyObject* figure_setJoint(figure_obj* self, PyObject* args, PyObject* kwargs) {

		static char* kwlist[] = { "jointName","position","rotation","scale","space", NULL };

		PyObject* arg;
		PyObject* arg1 = nullptr;
		PyObject* arg2 = nullptr;
		PyObject* arg3 = nullptr;
		Space space = LocalSpace;
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOOi", kwlist, &arg, &arg1, &arg2, &arg3, &space))return NULL;

		int index = GetJointIndex(self->figure, arg);
		if (index == -1) return NULL;

		Joint joint = self->figure->GetJoint(index, space);
		float* v;
		int d;
		float buff[4];
		if (arg1) {
			v = pyObjToFloat(arg1, buff, d);
			for (int i = 0; i < d; i++) joint.translation[i] = v[i];
		}
		if (arg2) {
			v = pyObjToFloat(arg2, buff, d);
			for (int i = 0; i < d; i++) joint.rotation[i] = v[i];
		}
		if (arg3) {
			v = pyObjToFloat(arg3, buff, d);
			for (int i = 0; i < d; i++) joint.scale[i] = v[i];
		}
		self->figure->SetJoint(index, joint, space);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_jointNameToIndex(figure_obj* self, PyObject* args)
	{
		char* name;
		if (!PyArg_ParseTuple(args, "s", &name))return NULL;
		int index = self->figure->GetJointIndex(GenerateNameHash(name));
		return PyLong_FromLong(index);
	}
	
	static PyObject* figure_getJointParentIndex(figure_obj* self, PyObject* args)
	{
		PyObject* arg;
		if (!PyArg_ParseTuple(args, "O", &arg))return NULL;
		int index = GetJointIndex(self->figure, arg);
		if (index == -1) return NULL;
		int parentIndex = self->figure->GetJointParentIndex(index);
		return PyLong_FromLong(parentIndex);
	}


	static PyObject* figure_SetMaterialParam(figure_obj* self, PyObject* args)
	{
		//efig.setMaterialParam("mate01", "DiffuseColor", (1.0, 1.0, 1.0, 1.0));

		PyObject* materialNameOrIndex;
		char* paramName;
		PyObject* param;
		if (!PyArg_ParseTuple(args, "OsO", &materialNameOrIndex, &paramName, &param)) return NULL;

		int index = GetMaterialIndex(self->figure, materialNameOrIndex);
		if (index == -1) return NULL;

		float buff[4];
		int  d = 0;
		float* ret = pyObjToFloat(param, buff, d);
		if (d == 0) {
			PyErr_SetString(PyExc_TypeError, "parameter error.");
			return NULL;
		}
		if (!self->figure->SetMaterialParam(index, paramName, ret)) {
			PyErr_SetString(PyExc_TypeError, "parameter error.");
			return NULL;
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_SetMaterialParamTexture(figure_obj* self, PyObject* args, PyObject* kwargs)
	{
		static char* kwlist[] = { "materialName","samplerName","textureName","pixel","width","height","wrap_s","wrap_t","minfilter","magfilter","mipfilter", NULL };

		PyObject* materialNameOrIndex = nullptr;
		char* samplerName = nullptr;

		PyObject* textureName = nullptr;

		PyObject* pixel = nullptr;
		int w = 0;
		int h = 0;
		int wrap_s = SamplerState::WRAP;
		int wrap_t = SamplerState::WRAP;
		int minfilter = SamplerState::LINEAR_MIPMAP_LINEAR;
		int magfilter = SamplerState::LINEAR;
		int mipfilter = SamplerState::LINEAR_MIPMAP_LINEAR;

		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OsO|Oiiiiiii", kwlist,
			&materialNameOrIndex, &samplerName, &textureName,
			&pixel, &w, &h,
			&wrap_s, &wrap_t, &minfilter, &magfilter, &mipfilter)) return NULL;

		int index = GetMaterialIndex(self->figure, materialNameOrIndex);
		if (index == -1) return NULL;

		Sampler sampler;
		if (textureName->ob_type == &TextureType) {
			((texture_obj*)textureName)->colortexture->IncReference();
			sampler.tex = ((texture_obj*)textureName)->colortexture;
		}
		else {
			const char* nameText = PyUnicode_AsUTF8(textureName);
			if (pixel) {
				if (!PyBytes_Check(pixel) || w == 0 || h == 0) {
					PyErr_SetString(PyExc_TypeError, "parameter error");
					return NULL;
				}
				char* pix = PyBytes_AsString(pixel);
				sampler.tex = pyxieResourceCreator::Instance().NewTexture(nameText, pix, w, h, true);
			}
			else {
				sampler.tex = pyxieResourceCreator::Instance().NewTexture(nameText);
			}
		}
		sampler.samplerSlot = 0;
		sampler.samplerState.wrap_s = wrap_s;
		sampler.samplerState.wrap_t = wrap_t;
		sampler.samplerState.minfilter = minfilter;
		sampler.samplerState.magfilter = magfilter;
		sampler.samplerState.mipfilter = mipfilter;

		if (!self->figure->SetMaterialParam(index, samplerName, &sampler)) {
			if (sampler.tex)sampler.tex->DecReference();
			PyErr_SetString(PyExc_TypeError, "parameter error.");
			return NULL;
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_GetMaterialParam(figure_obj* self, PyObject* args) {

		PyObject* materialNameOrIndex;
		char* paramName;
		if (!PyArg_ParseTuple(args, "Os", &materialNameOrIndex, &paramName)) return NULL;
		int index = GetMaterialIndex(self->figure, materialNameOrIndex);
		if (index == -1) return NULL;
		auto param = self->figure->GetMaterialParam(index, paramName);
		if (param == nullptr) return NULL;

		switch (param->type) {
		case ParamTypeSampler: {
			texture_obj* tex_obj = PyObject_New(texture_obj, &TextureType);
			if (!tex_obj) return NULL;
			tex_obj->colortexture = param->sampler.tex;
			tex_obj->depth = 0;
			tex_obj->stencil = 0;
			tex_obj->renderTarget = nullptr;
			return (PyObject*)tex_obj;
		}
		case ParamTypeFloat: {
			return PyFloat_FromDouble(param->fValue[0]);
		}
		case ParamTypeFloat2: {
			vec_obj* v = PyObject_New(vec_obj, _Vec2Type);
			if (!v) return NULL;
			v->d = 2;
			v->v[0] = param->fValue[0];
			v->v[1] = param->fValue[1];
			return (PyObject*)v;
		}
		case ParamTypeFloat3: {
			vec_obj* v = PyObject_New(vec_obj, _Vec3Type);
			if (!v) return NULL;
			v->d = 3;
			v->v[0] = param->fValue[0];
			v->v[1] = param->fValue[1];
			v->v[2] = param->fValue[2];
			return (PyObject*)v;
		}
		case ParamTypeFloat4: {
			vec_obj* v = PyObject_New(vec_obj, _Vec4Type);
			if (!v) return NULL;
			v->d = 4;
			v->v[0] = param->fValue[0];
			v->v[1] = param->fValue[1];
			v->v[2] = param->fValue[2];
			v->v[3] = param->fValue[3];
			return (PyObject*)v;
		}
		}
		PyErr_SetString(PyExc_TypeError, "unsupported param type.");
		return NULL;
	}

	static PyObject* figure_SetMaterialRenderState(figure_obj* self, PyObject* args, PyObject* kwargs)
	{
		static char* kwlist[] = { "materialName","paramName","value1","value2","value3","value4", NULL };
		PyObject* mateNameOrindex = nullptr;
		char* paramName = nullptr;
		PyObject* values[4] = { 0,0,0,0 };
		if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OsO|OOO", kwlist,
			&mateNameOrindex, &paramName, &values[0], &values[1], &values[2], &values[3])) return NULL;

		int index = GetMaterialIndex(self->figure, mateNameOrindex);
		if (index == -1) return NULL;

		RenderStateInfo* stateInfo = nullptr;
		const ShaderParameterInfo* paramInfo = pyxieRenderContext::Instance().GetShaderParameterInfoByName(paramName);
		if (paramInfo) stateInfo = pyxieRenderContext::Instance().GetRenderStateInfo((ShaderParameterKey)paramInfo->key);
		if (!stateInfo) {
			PyErr_SetString(PyExc_ValueError, "unsupported render states");
			return NULL;
		}
		uint32_t val[4] = { 0,0,0,0 };
		for (int i = 0; i < 4; i++) {
			if (values) {
				if (stateInfo->valueTypes[i] == Int) val[i] = (uint32_t)PyLong_AsLong(values[i]);
				else if (stateInfo->valueTypes[i] == Float)  ((float*)val)[i] = (float)PyFloat_AsDouble(values[i]);
			}
		}
		self->figure->SetMaterialState(index, (ShaderParameterKey)paramInfo->key, val);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_SetMeshAlpha(figure_obj* self, PyObject* args)
	{
		PyObject* meshNameOrIndex;
		float alpha;
		if (!PyArg_ParseTuple(args, "Of", &meshNameOrIndex, &alpha)) return NULL;
		int index = GetMeshIndex(self->figure, meshNameOrIndex);
		if (index == -1) return NULL;
		self->figure->SetMeshAlpha(index, alpha);
		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* figure_GetMeshAlpha(figure_obj* self, PyObject* args)
	{
		PyObject* meshNameOrIndex;
		if (!PyArg_ParseTuple(args, "O", &meshNameOrIndex)) return NULL;
		int index = GetMeshIndex(self->figure, meshNameOrIndex);
		if (index == -1) return NULL;
		return PyFloat_FromDouble(self->figure->GetMeshAlpha(index));
	}


	static PyObject* figure_SetParentJoint(figure_obj* self, PyObject* args) {
		PyObject* parent;
		PyObject* joint;
		if (!PyArg_ParseTuple(args, "OO", &parent, &joint)) return NULL;
		auto drawable = ((pyxieDrawable*)(((drawable_obj*)parent)->res));
		int index = GetJointIndex(drawable, joint);
		if (index != -1) {
			self->figure->SetParentJoint(drawable, drawable->GetJointMatrix(index));
		}
		Py_INCREF(Py_None);
		return Py_None;
	}

	static int GetMeshIndex(figure_obj* self, PyObject* arg) {
		int index = -1;
		if (PyLong_Check(arg)) {
			index = PyLong_AsLong(arg);
		}
		else if (PyUnicode_Check(arg)) {
			Py_ssize_t data_len;
			const char* key_str = PyUnicode_AsUTF8AndSize(arg, &data_len);
			index = self->figure->GetMeshIndex(GenerateNameHash(key_str));
		}
		if (index == -1) {
			PyErr_SetString(PyExc_TypeError, "mesh not found.");
		}
		return index;
	}

	static PyObject* figure_getAABB(figure_obj* self, PyObject* args)
	{
		PyObject* arg = nullptr;
		if (!PyArg_ParseTuple(args, "|O", &arg)) return NULL;
		int index = -1;
		if (arg) {
			int index = GetMeshIndex(self, arg);
		}
		vec_obj* min = PyObject_New(vec_obj, _Vec3Type);
		vec_obj* max = PyObject_New(vec_obj, _Vec3Type);
		self->figure->CalcAABBox(index, min->v, max->v);
		min->d = 3;
		max->d = 3;
		PyObject* tuple = PyTuple_New(2);
		PyTuple_SetItem(tuple, 0, (PyObject*)min);
		PyTuple_SetItem(tuple, 1, (PyObject*)max);

		return tuple;
	}

	static PyObject* figure_getTextureName(figure_obj* self, PyObject* args)
	{
		int index;
		if (!PyArg_ParseTuple(args, "i", &index)) return NULL;
		const char* name = self->figure->GetTextureName(index);
		if (!name) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		return PyUnicode_FromString(name);
	}
	static PyObject* figure_getEmbeddedAnimationName(figure_obj* self, PyObject* args)
	{
		int index;
		if (!PyArg_ParseTuple(args, "i", &index)) return NULL;
		const char* name = self->figure->GetEmbeddedAnimationName(index);
		if (!name) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		return PyUnicode_FromString(name);
	}
	static PyObject* figure_getJointName(figure_obj* self, PyObject* args)
	{
		int index;
		if (!PyArg_ParseTuple(args, "i", &index)) return NULL;
		const char* name = self->figure->GetJointName(index);
		if (!name) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		return PyUnicode_FromString(name);
	}
	static PyObject* figure_getMeshName(figure_obj* self, PyObject* args)
	{
		int index;
		if (!PyArg_ParseTuple(args, "i", &index)) return NULL;
		const char* name = self->figure->GetMeshName(index);
		if (!name) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		return PyUnicode_FromString(name);
	}
	static PyObject* figure_getMaterialName(figure_obj* self, PyObject* args)
	{
		int index;
		if (!PyArg_ParseTuple(args, "i", &index)) return NULL;
		const char* name = self->figure->GetMaterialName(index);
		if (!name) {
			Py_INCREF(Py_None);
			return Py_None;
		}
		return PyUnicode_FromString(name);
	}



	PyMethodDef figure_methods[] = {
		{ "connectAnimator", (PyCFunction)figure_BindAnimator, METH_VARARGS, connectAnimator_doc},
		{ "getCamera", (PyCFunction)figure_GetCamera, METH_VARARGS, getCamera_doc},
		{ "getEnvironment", (PyCFunction)figure_GetEnvironment, METH_NOARGS, getEnvironment_doc},
		{ "getEmbeddedAnimator", (PyCFunction)figure_getEmbeddedAnimator,METH_VARARGS,getEmbeddedAnimator_doc},
		{ "step", (PyCFunction)figure_Step, METH_VARARGS, step_doc},
		{ "setTime", (PyCFunction)figure_SetTime, METH_VARARGS, setTime_doc},
		{ "setBlendingWeight", (PyCFunction)figure_setBlendingWeight, METH_VARARGS, setBlendingWeight_doc},
		{ "getBlendingWeight", (PyCFunction)figure_getBlendingWeight, METH_VARARGS, getBlendingWeight_doc},
		{ "getJoint", (PyCFunction)figure_getJoint, METH_VARARGS, getJoint_doc},
		{ "setJoint", (PyCFunction)figure_setJoint, METH_VARARGS | METH_KEYWORDS, setJoint_doc},
		{ "jointNameToIndex", (PyCFunction)figure_jointNameToIndex, METH_VARARGS, jointNameToIndex_doc},
		{ "getJointParentIndex", (PyCFunction)figure_getJointParentIndex, METH_VARARGS, getJointParentIndex_doc},
		{ "setParentJoint", (PyCFunction)figure_SetParentJoint, METH_VARARGS, setParentJoint_doc},
		{ "getMaterialParam", (PyCFunction)figure_GetMaterialParam, METH_VARARGS, getMaterialParam_doc},
		{ "setMaterialParam", (PyCFunction)figure_SetMaterialParam, METH_VARARGS, setMaterialParam_doc},
		{ "setMaterialParamTexture", (PyCFunction)figure_SetMaterialParamTexture, METH_VARARGS | METH_KEYWORDS, setMaterialParamTexture_doc},
		{ "setMaterialRenderState", (PyCFunction)figure_SetMaterialRenderState, METH_VARARGS | METH_KEYWORDS,setMaterialRenderState_doc},
		{ "getAABB", (PyCFunction)figure_getAABB, METH_VARARGS, getAABB_doc},
		{ "getTextureName",(PyCFunction)figure_getTextureName,METH_VARARGS, getTextureName_doc},
		{ "getEmbeddedAnimationName",(PyCFunction)figure_getEmbeddedAnimationName,METH_VARARGS,getEmbeddedAnimationName_doc},
		{ "getJointName",(PyCFunction)figure_getJointName,METH_VARARGS,getJointName_doc},
		{ "getMeshName",(PyCFunction)figure_getMeshName,METH_VARARGS,getMeshName_doc},
		{ "getMaterialName",(PyCFunction)figure_getMaterialName,METH_VARARGS,getMaterialName_doc},
		{ "setMeshAlpha",(PyCFunction)figure_SetMeshAlpha,METH_VARARGS,setMeshAlpha_doc},
		{ "getMeshAlpha",(PyCFunction)figure_GetMeshAlpha,METH_VARARGS,getMeshAlpha_doc},

		//{ "dump", (PyCFunction)figure_Dump, METH_VARARGS },
		{ NULL,	NULL }
	};

	PyGetSetDef figure_getsets[] = {
		{ const_cast<char*>("position"), (getter)figure_getPosition, (setter)figure_setPosition,position_doc, NULL },
		{ const_cast<char*>("rotation"), (getter)figure_getRotation, (setter)figure_setRotation,rotation_doc, NULL },
		{ const_cast<char*>("scale"),    (getter)figure_getScale,    (setter)figure_setScale,scale_doc, NULL },
		{ const_cast<char*>("numJoints"),(getter)figure_numJoints,    (setter)NULL,numJoints_doc, NULL },
		{ const_cast<char*>("numMeshes"),(getter)figure_numMeshes,    (setter)NULL,numMeshes_doc, NULL },
		{ const_cast<char*>("numMaterials"),(getter)figure_numMaterials,    (setter)NULL,numMaterials_doc, NULL },
		{ const_cast<char*>("numAnimations"),(getter)figure_numAnimations,    (setter)NULL,numAnimationss_doc, NULL },
		{ const_cast<char*>("numEmbeddedAnimations"),(getter)figure_numEmbeddedAnimations,    (setter)NULL,numEmbeddedAnimations_doc, NULL },
		{ const_cast<char*>("numTextures"),(getter)figure_numTextures,    (setter)NULL,numTextures_doc, NULL },

	{ NULL, NULL }
	};

	PyTypeObject FigureType = {
		PyVarObject_HEAD_INIT(NULL, 0)
		"igeCore.figure",						/* tp_name */
		sizeof(figure_obj),                 /* tp_basicsize */
		0,                                  /* tp_itemsize */
		(destructor)figure_dealloc,			/* tp_dealloc */
		0,                                  /* tp_print */
		0,							        /* tp_getattr */
		0,                                  /* tp_setattr */
		0,                                  /* tp_reserved */
		0,                                  /* tp_repr */
		0,					                /* tp_as_number */
		0,                                  /* tp_as_sequence */
		0,                                  /* tp_as_mapping */
		0,                                  /* tp_hash */
		0,                                  /* tp_call */
		(reprfunc)figure_str,               /* tp_str */
		0,                                  /* tp_getattro */
		0,                                  /* tp_setattro */
		0,                                  /* tp_as_buffer */
		Py_TPFLAGS_DEFAULT,					/* tp_flags */
		0,									/* tp_doc */
		0,									/* tp_traverse */
		0,                                  /* tp_clear */
		0,                                  /* tp_richcompare */
		0,                                  /* tp_weaklistoffset */
		0,									/* tp_iter */
		0,									/* tp_iternext */
		figure_methods,						/* tp_methods */
		0,                                  /* tp_members */
		figure_getsets,                     /* tp_getset */
		0,                                  /* tp_base */
		0,                                  /* tp_dict */
		0,                                  /* tp_descr_get */
		0,                                  /* tp_descr_set */
		0,                                  /* tp_dictoffset */
		0,                                  /* tp_init */
		0,                                  /* tp_alloc */
		figure_new,							/* tp_new */
		0,									/* tp_free */
	};

}