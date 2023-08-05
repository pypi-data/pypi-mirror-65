#include "Firebase.h"
#include "firebase/app.h"

#if defined(_WIN32)
#include <windows.h>
#include <stdarg.h>

WindowContext FirebaseGetWindowContext()
{
    return nullptr;
}
#elif defined(__ANDROID__)
#include <unistd.h>
#include <jni.h>
#include "SDL.h"

JNIEnv *FirebaseGetJniEnv()
{
    return (JNIEnv *)SDL_AndroidGetJNIEnv();
}

jobject FirebaseGetActivity()
{
    return (jobject)SDL_AndroidGetActivity();
}

// Get the window context. For Android, it's a jobject pointing to the Activity.
jobject FirebaseGetWindowContext()
{
    return FirebaseGetActivity();
}
#elif defined(__APPLE__)
#include <unistd.h>
#include <stdarg.h>
#include <mach/mach_time.h>

extern "C" WindowContext GetWindowContext();
WindowContext FirebaseGetWindowContext()
{
#if FIREBASE_PLATFORM_IOS
    return GetWindowContext();
#else // not yet supported MacOS
    return nullptr;
#endif
}
#endif // __APPLE__

firebase::App *Firebase::firebase_app = nullptr;
FirebaseImpl *Firebase::m_firebaseImpl = nullptr;

Firebase::Firebase()
{
}

Firebase::~Firebase()
{
}

void Firebase::init(bool analytics, bool messaging, bool remoteConfig)
{
	m_firebaseImpl = new FirebaseImpl();
	
    firebase_app = firebase::App::GetInstance();
    if (firebase_app == nullptr)
    {
        GetImpl()->Init(analytics, messaging, remoteConfig);
        LOG("fb.initCreated the firebase app %x", static_cast<int>(reinterpret_cast<intptr_t>(firebase_app)));
    }
}

void Firebase::release()
{
    if(GetImpl() != nullptr)
    {
        GetImpl()->Release();
    }

    delete firebase_app;
}

bool Firebase::isReady()
{
    if(GetImpl() != nullptr)
    {
        return GetImpl()->IsReady();
    }
    
    return false;
}
