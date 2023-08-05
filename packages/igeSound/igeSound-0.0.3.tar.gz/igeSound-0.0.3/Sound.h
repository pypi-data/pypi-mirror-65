#pragma once

#include <stdio.h>
#include <assert.h>
#include <stdint.h>
#include <map>
#include <string>

#ifdef _WIN32
#define PYXIE_EXPORT __declspec(dllexport)
#else
#define PYXIE_EXPORT
#endif

#ifdef NDEBUG
#define LOG_VERBOSE(...)
#define LOG_DEBUG(...)
#define LOG(...)
#define LOG_WARN(...)
#define LOG_ERROR(...)
#else
#ifdef _ANDROID_
#define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "Sound", __VA_ARGS__);
#define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "Sound", __VA_ARGS__);
#define LOG(...) __android_log_print(ANDROID_LOG_INFO, "Sound", __VA_ARGS__);
#define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "Sound", __VA_ARGS__);
#define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "Sound", __VA_ARGS__);
#else
#define LOG_VERBOSE(...) printf(__VA_ARGS__);
#define LOG_DEBUG(...) printf(__VA_ARGS__);
#define LOG(...) printf(__VA_ARGS__);
#define LOG_WARN(...) printf(__VA_ARGS__);
#define LOG_ERROR(...) printf(__VA_ARGS__);
#endif
#endif

#include "soloud.h"

using namespace SoLoud;

class PYXIE_EXPORT Sound
{
public:
	Sound();
	~Sound();
	void init();
	void release();
	void play(char* filename, bool steam = false, bool loop = false);
	void stop(char* filename);
	void stopAllSound();
	void load(char* filename, bool stream);
	void unload(char* filename);
	void unloadUnused();
	void setPositon(char* filename, float x, float y, float z);
	void setPitch(char* filename, float pitch);
	void setGain(char* filename, float gain);
	void setRolloff(char* filename, float rolloff);
	
protected:
	bool isInitialized() { return initialized; }
	void releaseAllSound();

private:
	bool initialized;
	std::map<std::string, AudioSource*> m_audioSourcesDict;
	Soloud *m_soloud;

	static Sound* instance;
public:
	static Sound* Instance()
	{
		if (!instance)
			instance = new Sound;
		return instance;
	}
};