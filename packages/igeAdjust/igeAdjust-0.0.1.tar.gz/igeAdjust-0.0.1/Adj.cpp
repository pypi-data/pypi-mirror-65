#include "Adj.h"
#include "AdjustImpl.h"

Adj* Adj::instance = nullptr;

Adj::Adj()
	: m_adjustImpl(new AdjustImpl())
{
	LOG("Adjust()");
}
Adj::~Adj()
{
	LOG("~Adjust()");
}

void Adj::init()
{
	m_adjustImpl->Init();
}

void Adj::release()
{
	m_adjustImpl->Release();
}

void Adj::logEvent(const char* eventType, std::map<std::string, std::string> eventValue)
{
	m_adjustImpl->logEvent(eventType, eventValue);
}
