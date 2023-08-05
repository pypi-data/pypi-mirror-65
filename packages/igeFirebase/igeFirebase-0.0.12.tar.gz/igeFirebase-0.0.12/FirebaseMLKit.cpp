#include "FirebaseMLKit.h"
#include "FirebaseMLKitImpl.h"

FirebaseMLKit* FirebaseMLKit::instance = nullptr;
using namespace firebase;

FirebaseMLKit::FirebaseMLKit()
	: m_firebaseMLKitImpl(new FirebaseMLKitImpl())
{
	LOG("FirebaseMLKit()");
}
FirebaseMLKit::~FirebaseMLKit()
{
	LOG("~FirebaseMLKit()");
}

bool FirebaseMLKit::isSupported()
{
	return m_firebaseMLKitImpl->IsSupported();
}

void FirebaseMLKit::init(int mode)
{
	m_firebaseMLKitImpl->Init(mode);
}

void FirebaseMLKit::release()
{
	m_firebaseMLKitImpl->Release();
}

void FirebaseMLKit::preview()
{
	m_firebaseMLKitImpl->Preview();
}

float* FirebaseMLKit::getContours(int& size)
{
	return m_firebaseMLKitImpl->GetContours(size);
}

float FirebaseMLKit::getHeadEulerAngleY()
{
	return m_firebaseMLKitImpl->GetHeadEulerAngleY();
}

float FirebaseMLKit::getHeadEulerAngleZ()
{
	return m_firebaseMLKitImpl->GetHeadEulerAngleZ();
}

uint32_t FirebaseMLKit::getCameraWidth()
{
    return m_firebaseMLKitImpl->GetCameraWidth();
}

uint32_t FirebaseMLKit::getCameraHeight()
{
    return m_firebaseMLKitImpl->GetCameraHeight();
}

uint8_t* FirebaseMLKit::getCameraData()
{
    return m_firebaseMLKitImpl->GetCameraData();
}
