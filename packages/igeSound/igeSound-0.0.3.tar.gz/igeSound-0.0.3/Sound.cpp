#include "Sound.h"

#include "soloud_wav.h"
#include "soloud_wavstream.h"

Sound* Sound::instance;

Sound::Sound()
	:initialized(false)
	, m_soloud(nullptr)
{	
}

Sound::~Sound()
{
	delete m_soloud;
}

void Sound::init()
{
	if (m_soloud == nullptr)
	{
		m_soloud = new SoLoud::Soloud();
		m_soloud->init();		
	}
	initialized = true;
}

void Sound::release()
{
	if (m_soloud != nullptr)
	{
		stopAllSound();
		releaseAllSound();

		m_soloud->deinit();

		delete m_soloud;
		m_soloud = nullptr;
	}
	initialized = false;
}

void Sound::load(char* filename, bool stream)
{
	auto it = m_audioSourcesDict.find(filename);
	if (it == m_audioSourcesDict.end())
	{
		if (stream)
		{
			WavStream* audio = new WavStream();
			audio->load(filename);
			m_audioSourcesDict[filename] = audio;
		}
		else
		{
			Wav* audio = new Wav();
			audio->load(filename);
			m_audioSourcesDict[filename] = audio;
		}
	}
}

void Sound::unload(char* filename)
{
	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		it->second->stop();
		delete it->second;		
	}
}

void Sound::unloadUnused()
{
	
}

void Sound::setPositon(char* filename, float x, float y, float z)
{
	
}

void Sound::setPitch(char* filename, float pitch)
{
	
}

void Sound::setGain(char* filename, float gain)
{
	
}

void Sound::setRolloff(char* filename, float rolloff)
{

}

void Sound::play(char* filename, bool stream, bool loop)
{
	if (!isInitialized())
	{
		LOG("Sound need to initialize first");
		return;
	}

	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		it->second->setLooping(loop);
		m_soloud->play(*it->second);
	}
	else
	{
		if(stream)
		{
			WavStream* audio = new WavStream();
			audio->setSingleInstance(true);
			audio->load(filename);
			audio->setLooping(loop);
			m_soloud->play(*audio);
			m_audioSourcesDict[filename] = audio;
		}
		else
		{
			Wav* audio = new Wav();
			audio->load(filename);
			audio->setLooping(loop);
			m_soloud->play(*audio);
			m_audioSourcesDict[filename] = audio;
		}		
	}
}

void Sound::stop(char* filename)
{
	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		Wav* audio = (Wav*)(it->second);
		m_soloud->stopAudioSource(*audio);
	}
}

void Sound::stopAllSound()
{
	m_soloud->stopAll();
}

void Sound::releaseAllSound()
{
	for (auto it = m_audioSourcesDict.begin(); it != m_audioSourcesDict.end(); it++)
	{
		it->second->stop();
		delete (it->second);
	}

	m_audioSourcesDict.clear();
}