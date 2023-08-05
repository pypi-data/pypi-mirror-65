#pragma once

#include <stdio.h>
#include <assert.h>
#include <stdint.h>

#include "firebase/future.h"

#include "FirebaseImpl.h"

#if defined _WIN32
    #include <time.h>
#elif defined(__ANDROID__)
    #include <jni.h>
    #include <sys/time.h>
    #include <time.h>
#elif defined __APPLE__
	#include <objc/objc.h>
	#include <mach/mach_time.h>
#endif

#ifdef _WIN32
    #define IGE_EXPORT __declspec(dllexport)
#else
    #define IGE_EXPORT
#endif

#ifdef NDEBUG
    #define LOG_VERBOSE(...)
    #define LOG_DEBUG(...)
    #define LOG(...)
    #define LOG_WARN(...)
    #define LOG_ERROR(...)
#else
    #if defined(__ANDROID__)
        #include <android/log.h>

        #define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "firebase", __VA_ARGS__);
        #define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "firebase", __VA_ARGS__);
        #define LOG(...) __android_log_print(ANDROID_LOG_INFO, "firebase", __VA_ARGS__);
        #define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "firebase", __VA_ARGS__);
        #define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "firebase", __VA_ARGS__);
    #else
        void FirebaseLogMessage(const char* format, ...);

        #define LOG_VERBOSE(...) FirebaseLogMessage(__VA_ARGS__);
        #define LOG_DEBUG(...) FirebaseLogMessage(__VA_ARGS__);
        #define LOG(...) FirebaseLogMessage(__VA_ARGS__);
        #define LOG_WARN(...) FirebaseLogMessage(__VA_ARGS__);
        #define LOG_ERROR(...) FirebaseLogMessage(__VA_ARGS__);
    #endif
#endif

// WindowContext represents the handle to the parent window.  It's type
// (and usage) vary based on the OS.
#if defined(__ANDROID__)
    typedef jobject WindowContext;  // A jobject to the Java Activity.

    JNIEnv* FirebaseGetJniEnv();
    jobject FirebaseGetActivity();
#elif defined(__APPLE__)
    typedef id WindowContext;  // A pointer to an iOS UIView.
#else
    typedef void* WindowContext;  // A void* for any other environments.
#endif
WindowContext FirebaseGetWindowContext();

namespace firebase
{
	class FutureBase;
	class App;
	//enum FutureStatus;
}

class IGE_EXPORT Firebase
{
public:
	Firebase();
	~Firebase();
	void init(bool analytics = 1, bool messaging = 1, bool remoteConfig = 1);
	void release();
    bool isReady();

	static firebase::App* firebase_app;
	static FirebaseImpl* m_firebaseImpl;
	FirebaseImpl* GetImpl() { return m_firebaseImpl; }
	
};
