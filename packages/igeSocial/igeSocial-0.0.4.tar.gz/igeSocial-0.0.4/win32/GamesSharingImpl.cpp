#include "GamesSharingImpl.h"
#include "Social.h"


void GamesSharingImpl::Init(SnsType sns)
{
}

void GamesSharingImpl::Release(SnsType sns)
{
}

void GamesSharingImpl::SignIn(SnsType sns)
{
}

void GamesSharingImpl::SignOut(SnsType sns)
{
}

bool GamesSharingImpl::IsSignedIn(SnsType sns)
{
	return false;
}

void GamesSharingImpl::Share(SnsType sns, ShareType share, const char* value)
{
}

const char* GamesSharingImpl::GetProfileID(SnsType sns)
{
	return "";
}

const char* GamesSharingImpl::GetProfileName(SnsType sns)
{
	return "";
}

bool GamesSharingImpl::Available(SnsType sns)
{
	return false;
}
