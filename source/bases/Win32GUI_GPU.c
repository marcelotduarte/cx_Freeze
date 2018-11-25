//-----------------------------------------------------------------------------
// Win32GUI.c
//   Main routine for frozen GPU intensive programs for the Win32 GUI subsystem.
//-----------------------------------------------------------------------------
#include <windows.h>

// This export will be picked up by nvidia drivers >= 302
// https://docs.nvidia.com/gameworks/content/technologies/desktop/optimus.htm
__declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;


// This export will be picked up by AMD drivers >= 13.35
// https://gpuopen.com/amdpowerxpressrequesthighperformance/
__declspec(dllexport) DWORD AmdPowerXpressRequestHighPerformance = 0x00000001;


// We want the same program as the Win32GUI base, so let's just include that
#include "Win32GUI.c"
