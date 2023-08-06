
//position
PyDoc_STRVAR(position_doc,
	"3D position of object \n"\
	"\n"\
	"type :  pyvmath.vec3 : (x,y,z)");

//rotation
PyDoc_STRVAR(rotation_doc,
	"3D rotation of object \n"\
	"\n"\
	"type :  pyvmath.quat : (x,y,z,w)");

//scale
PyDoc_STRVAR(scale_doc,
	"3D scale of object \n"\
	"\n"\
	"type :  pyvmath.vec3 : (x,y,z)");


//numJoints
PyDoc_STRVAR(numJoints_doc,
	"Number of joints \n"\
	"\n"\
	"    type :  int (read only)");

//numMeshes
PyDoc_STRVAR(numMeshes_doc,
	"Number of meshes \n"\
	"\n"\
	"    type :  int (read only)");

//numMaterials
PyDoc_STRVAR(numMaterials_doc,
	"Number of materials \n"\
	"\n"\
	"    type :  int (read only)");

//numAnimations
PyDoc_STRVAR(numAnimationss_doc,
	"Number of registered animations \n"\
	"\n"\
	"    type :  int (read only)");

//numEmbeddedAnimations
PyDoc_STRVAR(numEmbeddedAnimations_doc,
	"The number of animation embedded in the file \n"\
	"\n"\
	"    type :  int (read only)");

//numTextures
PyDoc_STRVAR(numTextures_doc,
	"The number of textures linked in the file \n"\
	"\n"\
	"    type :  int (read only)");


//connectAnimator
PyDoc_STRVAR(connectAnimator_doc,
	"Apply animation data to the model.\n"\
	"\n"\
	"figure.connectAnimator(slot, anime)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    slot : int\n"\
	"        There are 6 slots, and the final motion is output by the following calculation.\n"\
	"\n"\
	"        A0* A1 + B0 * B1 + C0 * C1\n"\
	"       (* :weighted average , + : Additive synthesis)\n"\
	"\n"\
	"       Slots specify the following values \n"\
	"       igeCore.ANIMETION_SLOT_A0\n"\
	"       igeCore.ANIMETION_SLOT_A1\n"\
	"       igeCore.ANIMETION_SLOT_B0\n"\
	"       igeCore.ANIMETION_SLOT_B1\n"\
	"       igeCore.ANIMETION_SLOT_C0\n"\
	"       igeCore.ANIMETION_SLOT_C1\n"\
	"\n"\
	"    anime : string or igeCore.animator\n"\
	"        Animation name or igeCore.animator object\n"\
	"\n"\
	"        File name of the underlying motion data\n"\
	"\n"\
	"Examples\n"\
	"--------\n"\
	"figure.connectAnimator(igeCore.ANIMETION_SLOT_A0, 'animationA')\n"\
	"figure.connectAnimator(igeCore.ANIMETION_SLOT_A1, 'animationB')\n"\
	"figure.setBlendingWeight(igeCore.ANIMETION_PART_A), 0.5)\n"\
	"\n"\
	"It becomes the middle posture of animationA and animationB");

//getCamera
PyDoc_STRVAR(getCamera_doc,
	"Get camera information included in the scene\n"\
	"\n"\
	"camera = figure.getCamera(cameraName)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    cameraName : string\n"\
	"        Name of camea node\n"\
	"        If omitted, the first camera found is returned.\n"\
	"        It is not necessary to specify a name if the scene contains only one camera\n"\
	"Returns\n"\
	"-------\n"\
	"    camera : igeCore.camera\n"\
	"        camera object");
	
	
//getEnvironment
PyDoc_STRVAR(getEnvironment_doc,
	"Get environmental information included in the scene\n"\
	"Environmental information is information such as lightingand fog.\n"\
	"\n"\
	"env = figure.getEnvironment()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    env : igeCore.environment\n"\
	"        enbironment object\n"\
	"\n"\
	" environment object\n"\
	"\n"\
	"Specification of environment is still under construction");

//getEmbeddedAnimator
PyDoc_STRVAR(getEmbeddedAnimator_doc,
	"Get animator embedded in the scene\n"\
	"\n"\
	"animator = figure.getEmbeddedAnimator(animeName)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    animeName : string\n"\
	"        Name of anine file\n"\
	"Returns\n"\
	"-------\n"\
	"    animator : igeCore.animator\n"\
	"        animator object  or None if not found.");

//step
PyDoc_STRVAR(step_doc,
	"Advances the animation applied with connectAnimator() by elapsedTime\n"\
	"\n"\
	"figure.step(elapsedTime)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    elapsedTime : float\n"\
	"        Specifies the delta animation time in seconds\n"\
	"        If omitted, it will be the value of igeCore.elapsedTime()");

//setTime
PyDoc_STRVAR(setTime_doc,
	"Specifies the animation time applied by connectAnimator\n"\
	"\n"\
	"figure.setTime(time)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    time : float\n"\
	"        Specifies the animation time in seconds");
	
//setBlendingWeight
PyDoc_STRVAR(setBlendingWeight_doc,
	"Specifies the weight of the weighted average of animation parts\n"\
	"\n"\
	"figure.setBlendingWeight(part, weight)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    part : int\n"\
	"        Animation part for which you want to specify weights\n"\
	"\n"\
	"		 Specify the following value\n"\
	"        igeCore.ANIMETION_PART_A\n"\
	"        igeCore.ANIMETION_PART_B\n"\
	"        igeCore.ANIMETION_PART_C\n"\
	"\n"\
	"    weight : float\n"\
	"        Specify the weight of weighted average in the range of 0.0 to 1.0");


//getBlendingWeight
PyDoc_STRVAR(getBlendingWeight_doc,
	"Get weight of weighted average of animation part\n"\
	"\n"\
	"weight = figure.getBlendingWeight(part)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    part : int\n"\
	"        Animation part for which you want to obtain a weighted average\n"\
	"\n"\
	"		 Specify the following value\n"\
	"        igeCore.ANIMETION_PART_A\n"\
	"        igeCore.ANIMETION_PART_B\n"\
	"        igeCore.ANIMETION_PART_C\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    weight\n"\
	"        Weighted average value specified for each part");


//getJoint
PyDoc_STRVAR(getJoint_doc,
	"Get the value of joint after animation calculation in world coordinate system\n"\
	"\n"\
	"position, rotation, scale = figure.getJoint(jointName or jointIndex, space)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    jointName : string\n"\
	"        The name of the joint you want to get\n"\
	"    jointIndex : int\n"\
	"        The index of the joint you want to get\n"\
	"	space : int (optional)	\n"\
	"		Coordinate system of the value to get\n	"\
	"       (core.WorldSpace or core.LocalSpace)\n	"\
	"Returns\n"\
	"-------\n"\
	"    position : igeVmath.Vec3\n"\
	"        position of joint\n"\
	"    rotation : igeVmath.Quat\n"\
	"        rotation of joint\n"\
	"    scale : igeVmath.Vec3\n"\
	"        scale of joint");


//setJoint
PyDoc_STRVAR(setJoint_doc,
	"Set the value of joint in world coordinate system\n"\
	"\n"\
	"figure.setJoint(jointName or jointIndex, position, rotation, scale, space)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    jointName : string\n"\
	"        The name of the joint you want to get\n"\
	"    jointIndex : int\n"\
	"        The index of the joint you want to get\n"\
	"    position : igeVmath.Vec3 (optional)\n"\
	"        position of joint\n"\
	"    rotation : igeVmath.Quat (optional)\n"\
	"        rotation of joint\n"\
	"    scale : igeVmath.Vec3 (optional)\n"\
	"        scale of joint\n"\
	"	space : int (optional)	\n"\
	"		Coordinate system of the value to get\n	"\
	"       (core.WorldSpace or core.LocalSpace)\n	");


//jointNameToIndex
PyDoc_STRVAR(jointNameToIndex_doc,
	"Get Joint index from Joint name\n"\
	"\n"\
	"index = figure.jointNameToIndex(jointName)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    jointName : string\n"\
	"        The name of the joint you want to get\n"\
	"Returns\n"\
	"-------\n"\
	"	index : int\n"\
	"		The index of joint\n"\
	"		If there is no parent joint (root joint), -1 is returned.");

//getJointParentIndex
PyDoc_STRVAR(getJointParentIndex_doc,
	"Set the value of joint in world coordinate system\n"\
	"\n"\
	"parentindex = figure.setJoint(jointName or index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"	jointName : string\n"\
	"		The name of the joint you want to get\n"\
	"	index : int\n"\
	"		The index of the joint you want to get\n"\
	"Returns\n"\
	"-------\n"\
	"	index : int\n"\
	"		The index of joint\n");




//setMeshAlpha
PyDoc_STRVAR(setMeshAlpha_doc,
	"Set mesh alpha value.\n"\
	"\n"\
	"if you set alpha valie is less than 1.0 mesh is going to transparent.\n	"\
	"you set alpha valie is 0, mesh rendaring is skipped.\n	"\
	"\n"\
	"figure.setMeshAlpha(meshName, alpha)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"	meshName : string (or int)\n"\
	"		string of mesh name or int of mesh index to set alpha value.\n	"\
	"	alpha : float\n"\
	"		alpha value.\n"\
	"\n");

//getMeshAlpha
PyDoc_STRVAR(getMeshAlpha_doc,
	"Get mesh alpha value.\n"\
	"\n"\
	"alpha = figure.setMeshAlpha(meshName)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"	meshName : string (or int)\n"\
	"		string of mesh name or int of mesh index to set alpha value.\n	"\
	"Returns\n"\
	"-------\n"\
	"	alpha : float\n"\
	"		alpha values.\n");

//setMaterialParam
PyDoc_STRVAR(setMaterialParam_doc,
	"Set material parameters\n"\
	"\n"\
	"figure.setMaterialParam(materialName, paramName, paramValue)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    materialName : string\n"\
	"        Name of the material for which you want to set parameters\n"\
	"    paramName : string\n"\
	"        Name of the parameter to pass to the shader\n"\
	"    paramValue\n"\
	"        Tuple of value pass to the shader");

//setMaterialParamTexture
PyDoc_STRVAR(setMaterialParamTexture_doc,
	"Set texture material parameters\n"\
	"\n"\
	"figure.setMaterialParam(materialName, samplerName, textureName, pixel, width, height, wrap_s, wrap_t, minfilter, magfilter, mipfilter)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    materialName : string\n"\
	"        Name of the material for which you want to set parameters\n"\
	"    samplerName : string\n"\
	"         Name of the sampler parameter to pass to the shader\n"\
	"    textureName : string (optional)\n"\
	"        Texture file path\n"\
	"    pixel : binary (optional)\n"\
	"        binary array of rgba 32bit format image\n"\
	"        textureName and pixel + width, height can not be specified at the same time, \n"\
	"        textureName takes precedence\n"\
	"    width : int (optional)\n"\
	"        pixel image width\n"\
	"    height : int  (optional)\n"\
	"        pixel image height\n"\
	"    wrap_s : int  (optional)\n"\
	"        Texture horizontal wrap mode of sampler state\n"\
	"        The following values are available\n"\
	"        igeCore.SAMPLERSTATE_WRAP <- (default)\n"\
	"        igeCore.SAMPLERSTATE_MIRROR\n"\
	"        igeCore.SAMPLERSTATE_CLAMP\n"\
	"        igeCore.SAMPLERSTATE_BORDER\n"\
	"    wrap_t : int  (optional)\n"\
	"        Texture vertical wrap mode of sampler state\n"\
	"        The content is the same as wrap_s\n"\
	"    minfilter : int  (optional)\n"\
	"        Sampling method when expanding the texture\n"\
	"        The following values are available\n"\
	"        igeCore.SAMPLERSTATE_LINEAR <- (default)\n"\
	"        igeCore.SAMPLERSTATE_NEAREST\n"\
	"    magfilter : int  (optional)\n"\
	"       Sampling method when reducing the texture\n"\
	"        The following values are available\n"\
	"        igeCore.SAMPLERSTATE_LINEAR\n"\
	"        igeCore.SAMPLERSTATE_NEAREST\n"\
	"        igeCore.SAMPLERSTATE_NEAREST_MIPMAP_NEAREST\n"\
	"        igeCore.SAMPLERSTATE_LINEAR_MIPMAP_NEAREST\n"\
	"        igeCore.SAMPLERSTATE_NEAREST_MIPMAP_LINEAR\n"\
	"        igeCore.SAMPLERSTATE_LINEAR_MIPMAP_LINEAR\n"\
	"    mipfilter : int  (optional)\n"\
	"        Not used now.");

//getMaterialParam
PyDoc_STRVAR(getMaterialParam_doc,
	"Get material parameters\n"\
	"\n"\
	"value = figure.getMaterialParam(materialName, paramName)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    materialName : string (or int)\n"\
	"        string of the material name or integer of material index value.for which you want to get parameters\n"\
	"    paramName : string\n"\
	"        parameter name you want to get value.\n"\
	"Returns\n"\
	"-------\n"\
	"	value : float or igeVmath.vec2 or igeVmath.vec3 or igeVmath.vec4 or igeCore.texture\n"\
	"		Gets the value corresponding to the specified parameter name from the shader..\n");

//setMaterialRenderState
PyDoc_STRVAR(setMaterialRenderState_doc,
	"Set render state for material\n"\
	"\n"\
	"editableFigure.setMaterialRenderState(materialName, paramName, value1, value2, value3, value4)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    materialName : string\n"\
	"        Name of the material to which you want to add RenderState\n"\
	"    paramName : string\n"\
	"        Render state name\n"\
	"        The following names are currently available\n"\
	"        alpha_func\n"\
	"        alpha_test_enable\n"\
	"        blend_func\n"\
	"        blend_equation\n"\
	"        blend_enable\n"\
	"        cull_face\n"\
	"        cull_face_enable\n"\
	"        depth_func\n"\
	"        depth_mask\n"\
	"        depth_test_enable\n"\
	"        polygon_offset\n"\
	"        polygon_offset_fill_enable\n"\
	"        color_mask\n"\
	"        stencil_func\n"\
	"        stencil_mask\n"\
	"        stencil_op\n"\
	"        stencil_test_enable\n"\
	"        scissor_test_enable\n"\
	"        scissor\n"\
	"    value1 : float or int or bool\n"\
	"        Render state parameter\n"\
	"    value2 : float or int or bool\n"\
	"        Render state parameter\n"\
	"    value3 : float or int or bool\n"\
	"        Render state parameter\n"\
	"    value4 : float or int or bool\n"\
	"        Render state parameter");




//setParentJoint
PyDoc_STRVAR(setParentJoint_doc,
	"Set the joint of another figure \n"\
	"(or EditableFigure) as the parent joint.\n"\
	"\n"\
	"figure.setParentJoint(figure, jointName)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    figure : figure\n"\
	"        Parent figure or EditableFigure\n"\
	"    jointName : string\n"\
	"        Parent joint name\n");


//getAABB
PyDoc_STRVAR(getAABB_doc,
	"Calclate axis aligned bounding box\n"\
	"\n"\
	"min, max, = figure.getMeshAABB(name or index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string  (optional)\n"\
	"        The name of the mesh to calclate AABB\n"\
	"    index : int  (optional)\n"\
	"        Index number of mesh to calclate AABB\n"\
	"        \n"\
	"        If the parameter is not specified or -1 is specified, \n"\
	"        the AABB of the entire figure is calculated. \n"\
	"Returns\n"\
	"-------\n"\
	"    min : vec3\n"\
	"        minimum edge of bounding box\n"\
	"    max : vec3\n"\
	"        maximum edge of bounding box");


PyDoc_STRVAR(getTextureName_doc, 
	"Get linked texture file name.\n"\
	"\n"\
	"name = figure.getTextureName(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int  (optional)\n"\
	"        Index number of texture\n"\
	"Returns\n"\
	"-------\n"\
	"    name : string\n"\
	"        texture file name	\n"\
	"        None if the index is out of range");

PyDoc_STRVAR(getEmbeddedAnimationName_doc,
	"Get embedded animation name.\n"\
	"\n"\
	"When converting from Collada, EXPORT_NAMES = 1 must be defined in figure.conf.\n"\
	"\n"\
	"name = figure.getEmbeddedAnimationName(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int  (optional)\n"\
	"        Index number of animation\n"\
	"Returns\n"\
	"-------\n"\
	"    name : string\n"\
	"        animnation file name	\n"\
	"        None if the index is out of range");
PyDoc_STRVAR(getJointName_doc,
	"Get joint name.\n"\
	"\n"\
	"When converting from Collada, EXPORT_NAMES = 1 must be defined in figure.conf.\n"\
	"\n"\
	"name = figure.getJointName(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int  (optional)\n"\
	"        Index number of joint\n"\
	"Returns\n"\
	"-------\n"\
	"    name : string\n"\
	"        joint name	\n"\
	"        None if the index is out of range");
PyDoc_STRVAR(getMeshName_doc,
	"Get mesh name.\n"\
	"\n"\
	"When converting from Collada, EXPORT_NAMES = 1 must be defined in figure.conf.\n"\
	"\n"\
	"name = figure.getMeshName(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int  (optional)\n"\
	"        Index number of mesh\n"\
	"Returns\n"\
	"-------\n"\
	"    name : string\n"\
	"        mesh name	\n"\
	"        None if the index is out of range");

PyDoc_STRVAR(getMaterialName_doc,
	"Get material name.\n"\
	"\n"\
	"When converting from Collada, EXPORT_NAMES = 1 must be defined in figure.conf.\n"\
	"\n"\
	"name = figure.getMaterialName(index)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    index : int  (optional)\n"\
	"        Index number of material\n"\
	"Returns\n"\
	"-------\n"\
	"    name : string\n"\
	"        material name	\n"\
	"        None if the index is out of range");

