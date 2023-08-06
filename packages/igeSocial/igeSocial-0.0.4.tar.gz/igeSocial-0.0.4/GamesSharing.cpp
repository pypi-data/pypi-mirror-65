#include "GamesSharing.h"
#include "GamesSharingImpl.h"

GamesSharing::GamesSharing()
	: m_gamesSharingImpl(new GamesSharingImpl())
{
	LOG("GamesSharing()");
}
GamesSharing::~GamesSharing()
{
	LOG("~GamesSharing()");
}

void GamesSharing::init(SnsType sns)
{
	m_gamesSharingImpl->Init(sns);
}

void GamesSharing::release(SnsType sns)
{
	m_gamesSharingImpl->Release(sns);
}

void GamesSharing::signIn(SnsType sns)
{
	m_gamesSharingImpl->SignIn(sns);
}

void GamesSharing::signOut(SnsType sns)
{
	m_gamesSharingImpl->SignOut(sns);
}

bool GamesSharing::isSignedIn(SnsType sns)
{
	return m_gamesSharingImpl->IsSignedIn(sns);
}

void GamesSharing::share(SnsType sns, ShareType share, const char* value)
{
	m_gamesSharingImpl->Share(sns, share, value);
}

const char* GamesSharing::getProfileID(SnsType sns)
{
	return m_gamesSharingImpl->GetProfileID(sns);
}

const char* GamesSharing::getProfileName(SnsType sns)
{
	return m_gamesSharingImpl->GetProfileName(sns);
}

bool GamesSharing::available(SnsType sns)
{
    return m_gamesSharingImpl->Available(sns);
}

