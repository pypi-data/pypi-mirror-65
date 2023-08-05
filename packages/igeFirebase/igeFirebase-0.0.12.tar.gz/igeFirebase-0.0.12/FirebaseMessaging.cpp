#include "FirebaseMessaging.h"

FirebaseMessaging::FirebaseMessaging()
{
	LOG("FirebaseMessaging()");
}
FirebaseMessaging::~FirebaseMessaging()
{
	LOG("~FirebaseMessaging()");
}

void FirebaseMessaging::init()
{
	
}

void FirebaseMessaging::release()
{
	
}

const char* FirebaseMessaging::getRegistrationToken()
{
	return GetImpl()->MessagingGetRegistrationToken();
}
