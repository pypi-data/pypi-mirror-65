#include "AppsFlyer.h"
#include "AppsFlyerImpl.h"

AppsFlyer::AppsFlyer()
	: m_appsFlyerImpl(new AppsFlyerImpl())
{
	LOG("AppsFlyer()");
}
AppsFlyer::~AppsFlyer()
{
	LOG("~AppsFlyer()");
}

void AppsFlyer::init()
{
	m_appsFlyerImpl->Init();
}

void AppsFlyer::release()
{
	m_appsFlyerImpl->Release();
}

void AppsFlyer::logEvent(const char* eventType, std::map<std::string, std::string> eventValue)
{
	m_appsFlyerImpl->logEvent(eventType, eventValue);
}