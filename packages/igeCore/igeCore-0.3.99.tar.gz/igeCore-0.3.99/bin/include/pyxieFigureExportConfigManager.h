#pragma once

#include "pyxieTypes.h"

namespace pyxie
{
	class PYXIE_EXPORT pyxieFigureExportConfigManager {
		float BASE_SCALE;
		union {
			struct {
				uint32_t EXPORT_NAMES : 1;
				uint32_t TRIANGLE_STRIP : 1;
				uint32_t INHERIT_JOINT_NAME : 1;
				uint32_t CLOP_JOINT : 1;
				uint32_t GEN_MIPMAP : 1;
				uint32_t KILL_MIPMAP : 1;
				uint32_t FREEZE_GEOMETORY : 1;
				uint32_t COMPUTE_PERIOD : 1;
			};
			uint32_t buff;
		};
		pyxieFigureExportConfigManager();
	public:
		static pyxieFigureExportConfigManager& Instance();
		void SetOptionInt(const char* name, int value);
		void SetOptionFloat(const char* name, float value);
		float BaseScale() { return BASE_SCALE; }
		bool ExportNames() { return EXPORT_NAMES; }
		bool TriangleStrip() { return TRIANGLE_STRIP; }
		bool InheritJointName() { return INHERIT_JOINT_NAME; }
		bool ClopJoint() { return CLOP_JOINT; }
		bool FreezeGeometory() { return FREEZE_GEOMETORY; }
		bool ComputePeriod() { return COMPUTE_PERIOD; }
	};

/*
	class PYXIE_EXPORT pyxieFigureExportConfigManager {
		bool	TriangleStrip;				//Convert vertices to triangle strip format
		bool	FreezeGeometoryTransform;	//ジオメトリのトランスフォームをフリーズする
		bool	FullPathName;				//ノード名をルートからの親の名前を'/'でつなげた名前に変更する
		bool	OutputNameList;				//jointsとmaterialのノード名を出力する
		bool	OutputNotes;				//jointsとmaterialのノード名を出力する
		bool	GenMipmap;					//テクスチャのミップマップを生成する
		bool	ClopTransform;				//スキンウェイトを持ったオブジェクトノードのトランスフォームは削除する
		bool	ComputePeriod;
		float	BaseScale;
		float	Tolerance;
		pyxieFigureExportConfigManager();
	public:
		static pyxieFigureExportConfigManager& Instance();

		void ReadConfigFiles(const char* filePath);

		bool	IsTriangleStrip() { return TriangleStrip; }
		bool	IsFreezeGeometoryTransform() { return FreezeGeometoryTransform; }
		bool	IsFullPathName() { return FullPathName; }
		bool	IsOutputNameList() { return OutputNameList; }
		bool	IsOutputNotes() { return OutputNotes; }
		bool	IsGenMipmap() { return GenMipmap; }
		bool	IsClopTransform() { return ClopTransform; }
		bool	IsComputePeriod() { return ComputePeriod; }
		float	GetBaseScale() { return BaseScale; }
		float	GetTolerance() { return Tolerance; }
		void	SetBaseScale(float v) { BaseScale = v; }
	};
*/
}
