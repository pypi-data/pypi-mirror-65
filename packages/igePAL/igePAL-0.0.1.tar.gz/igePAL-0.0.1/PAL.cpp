#include "PAL.h"
#include "PALImpl.h"

PAL* PAL::instance = nullptr;

PAL::PAL()
	: m_PALImpl(new PALImpl())
	, m_NotifyHandlerFunc(nullptr)
{
}
PAL::~PAL()
{
}

void PAL::init()
{
	m_PALImpl->Init();
}

void PAL::release()
{
	m_PALImpl->Release();
}

void PAL::registerNotifyEvent(NotifyHandlerFunc handler)
{
	m_NotifyHandlerFunc = handler;
}

void PAL::notifyCallback(NotifyCallback callback)
{
	if (m_NotifyHandlerFunc != nullptr)
	{
		m_NotifyHandlerFunc(callback);
	}
	else
	{
		m_notifyEvents.push_back(callback);
	}
}

std::vector<NotifyCallback> PAL::pollNotifyEvent()
{
	return m_notifyEvents;
}
