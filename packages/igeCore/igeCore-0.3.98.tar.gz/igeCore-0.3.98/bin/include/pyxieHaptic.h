#pragma once

struct _SDL_Haptic;

namespace pyxie
{
	class PYXIE_EXPORT Haptic
	{
	public:
		Haptic();
		~Haptic();
		void Init();
		void Release();
		void RumblePlay(float strength, uint32_t length);
		void EffectPlay();
		void HapticPlay(int type, int repeat);
		void HapticStop();

	private:
		_SDL_Haptic* m_haptic;
		int  m_effectID;
			
	};
}