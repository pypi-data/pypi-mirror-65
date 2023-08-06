#pragma once

//#define TRACY_ENABLE	// used by game team where the define will be enabled from python script (igeCore.profiler(True))
//#define PYXIE_TRACY_ENABLE	//used by engine team. Add "PyxieZoneScoped;" at function you would like to profile

#  ifdef TRACY_ENABLE
#    include "Tracy.hpp"
#  endif

namespace pyxie
{
#ifdef TRACY_ENABLE
	#define PyxieFrameMark tracy::Profiler::SendFrameMark( nullptr )
#else
	#define PyxieFrameMark
#endif	//TRACY_ENABLE

#if defined (PYXIE_TRACY_ENABLE) && defined (TRACY_ENABLE)
	// CPU profiling
	#define PyxieZoneNamed( varname, active ) static const tracy::SourceLocationData TracyConcat(__tracy_source_location,__LINE__) { nullptr, __FUNCTION__,  __FILE__, (uint32_t)__LINE__, 0 }; tracy::ScopedZone varname( &TracyConcat(__tracy_source_location,__LINE__), active ) ;
	#define PyxieZoneNamedN( varname, name, active ) static const tracy::SourceLocationData TracyConcat(__tracy_source_location,__LINE__) { name, __FUNCTION__,  __FILE__, (uint32_t)__LINE__, 0 }; tracy::ScopedZone varname( &TracyConcat(__tracy_source_location,__LINE__), active ) ;
	#define PyxieZoneNamedC( varname, color, active ) static const tracy::SourceLocationData TracyConcat(__tracy_source_location,__LINE__) { nullptr, __FUNCTION__,  __FILE__, (uint32_t)__LINE__, color }; tracy::ScopedZone varname( &TracyConcat(__tracy_source_location,__LINE__), active ) ;
	#define PyxieZoneNamedNC( varname, name, color, active ) static const tracy::SourceLocationData TracyConcat(__tracy_source_location,__LINE__) { name, __FUNCTION__,  __FILE__, (uint32_t)__LINE__, color }; tracy::ScopedZone varname( &TracyConcat(__tracy_source_location,__LINE__), active ) ;

	#define PyxieZoneScoped PyxieZoneNamed( ___tracy_scoped_zone, true )
	#define PyxieZoneScopedN( name ) PyxieZoneNamedN( ___tracy_scoped_zone, name, true)
	#define PyxieZoneScopedC( color ) PyxieZoneNamedC( ___tracy_scoped_zone, color, true )
	#define PyxieZoneScopedNC( name, color ) PyxieZoneNamedNC( ___tracy_scoped_zone, name, color, true )

	// MEM profiling
	#define PyxieTracyAlloc( ptr, size ) tracy::Profiler::MemAlloc( ptr, size )
	#define PyxieTracyFree( ptr ) tracy::Profiler::MemFree( ptr )


#else
	// CPU profiling
	#define PyxieZoneNamed( varname, active )
	#define PyxieZoneNamedN( varname, name, active )
	#define PyxieZoneNamedC( varname, color, active )
	#define PyxieZoneNamedNC( varname, name, color, active )

	#define PyxieZoneScoped
	#define PyxieZoneScopedN( name )
	#define PyxieZoneScopedC( color )
	#define PyxieZoneScopedNC( name, color )

	// MEM profiling	
	#define PyxieTracyAlloc(ptr, size)
	#define PyxieTracyFree(ptr)
#endif	//PYXIE_TRACY_ENABLE

	class PYXIE_EXPORT Profiler
	{		
	public:
		Profiler(const char* name);
		~Profiler();
		void Release();

		static void EnableProfiler(bool enable);

	private:
		static bool isEnabled;
		bool isStartEventSent = false;
#ifdef TRACY_ENABLE
		tracy::ScopedZone* profile_scope;
#endif	//TRACY_ENABLE
	};
}