#include "Firebase.h"

#include "firebase/app.h"
#include "firebase/future.h"
#include "firebase/remote_config.h"
#include "FirebaseAnalytics.h"
#include "FirebaseRemoteConfig.h"

#include <windows.h>

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

#include <fstream>
#include <sstream>
#include "json.hpp"
using json = nlohmann::json;

void FirebaseLogMessage(const char* format, ...) {
	va_list list;
	va_start(list, format);
	vprintf(format, list);
	va_end(list);
	printf("\n");
	fflush(stdout);
}

static LARGE_INTEGER freq;

FirebaseImpl::FirebaseImpl()
        : m_listener(nullptr)
		, m_messageInitializer(nullptr)
		, m_remoteConfigInitializer(nullptr)
        , m_isReady(false)
{
#if defined(_WIN32)
	QueryPerformanceFrequency(&freq);
#elif defined(__APPLE__)
	mach_timebase_info(&timebase);
#endif
}

FirebaseImpl::~FirebaseImpl()
{
}

bool FirebaseImpl::ProcessEvents(int msec)
{
    Sleep(msec);
    return false;
}

void FirebaseImpl::Init(bool analytics, bool messaging, bool remoteConfig)
{
	m_analytics = analytics;
	m_messaging = messaging;
	m_remoteConfig = remoteConfig;
    // app
    Firebase::firebase_app = ::firebase::App::GetInstance();
    if(Firebase::firebase_app == nullptr)
    {
        Firebase::firebase_app = ::firebase::App::Create();    
    }

	// analytics
	if (m_analytics)
	{
		AnalyticsInit();
	}

	// messaging
	if (m_messaging)
	{
		MessagingInit();
	}

	// remote config
	if (m_remoteConfig)
	{
		RemoteConfigInit();
	}

    m_isReady = true;
}

void FirebaseImpl::Release()
{
    m_isReady = false;
    
	if (m_analytics)
	{
		AnalyticsRelease();
	}

	if (m_messaging)
	{
		MessagingRelease();
	}

	if (m_remoteConfig)
	{
		RemoteConfigRelease();
	}
}

void FirebaseImpl::AnalyticsInit()
{
    analytics::Initialize(*Firebase::firebase_app);
    analytics::SetAnalyticsCollectionEnabled(true);
    analytics::SetSessionTimeoutDuration(1000 * 60 * 30);
}

void FirebaseImpl::AnalyticsRelease()
{
	analytics::Terminate();
}

void FirebaseImpl::MessagingInit()
{
    LOG("Initialize the Messaging library");	
	m_listener = new ::firebase::messaging::PollableListener();
	m_messageInitializer = new ::firebase::ModuleInitializer();

	m_messageInitializer->Initialize(
            Firebase::firebase_app, m_listener, [](::firebase::App* app, void* userdata) {
                firebase::messaging::PollableListener* listener = static_cast<::firebase::messaging::PollableListener*>(userdata);

                firebase::messaging::MessagingOptions options;
                options.suppress_notification_permission_prompt = true;

                return firebase::messaging::Initialize(*app, listener, options);
            });


    while (m_messageInitializer->InitializeLastResult().status() != firebase::kFutureStatusComplete) {
        if (ProcessEvents(100)) return;  // exit if requested
    }

    if (m_messageInitializer->InitializeLastResult().error() != 0) {
        LOG("Failed to initialize Firebase Messaging: %s", m_messageInitializer->InitializeLastResult().error_message());
        return;
    }

    // Display permission prompt if necessary
    firebase::Future<void> result = firebase::messaging::RequestPermission();
    WaitForFutureCompletion(result);
    if (result.error() == firebase::messaging::kErrorFailedToRegisterForRemoteNotifications) {
        LOG("Error registering for remote notifications.");
        return;
    }
	MessagingGetRegistrationToken();
}

void FirebaseImpl::MessagingRelease()
{
    delete m_listener;
	delete m_messageInitializer;
    firebase::messaging::Terminate();
}

const char* FirebaseImpl::MessagingGetRegistrationToken()
{
    static std::string token;
    if (m_listener && m_listener->PollRegistrationToken(&token)) {
        LOG("Received Registration Token: %s", token.c_str());
    }
    return token.c_str();
}

void FirebaseImpl::RemoteConfigInit()
{
	std::vector<firebase::remote_config::ConfigKeyValueVariant> remoteDefaultValues;

	std::ifstream remoteConfig("remote_config.json");
	json config_json, result_json;
	if (!remoteConfig.fail())
	{
		remoteConfig >> config_json;		
		result_json = config_json["parameters"];
		if (result_json != nullptr)
		{
			for (auto it = result_json.begin(); it != result_json.end(); it++)
			{
				auto _json = result_json[it.key()]["defaultValue"]["value"];
				if (_json.is_string())
				{
					std::string value = _json.get<std::string>();
					remoteDefaultValues.push_back({ it.key().c_str(), value });
				}				
				else if(_json.is_number_integer())
				{
					int value = _json.get<int32_t>();
					remoteDefaultValues.push_back({ it.key().c_str(), value });
				}
				else if (_json.is_number_float())
				{
					float value = _json.get<float>();
					remoteDefaultValues.push_back({ it.key().c_str(), value });
				}
				else if (_json.is_boolean())
				{
					bool value = _json.get<bool>();
					remoteDefaultValues.push_back({ it.key().c_str(), value });
				}
				else
				{
					std::string value = _json.dump();
					remoteDefaultValues.push_back({ it.key().c_str(), value });
				}
			}
		}
	}	

	LOG("Initialize the RemoteConfig library");
	
	m_remoteConfigInitializer = new ::firebase::ModuleInitializer();

	m_remoteConfigInitializer->Initialize(Firebase::firebase_app, nullptr, [](::firebase::App* app, void*) {
		LOG("Try to initialize Remote Config");
		return firebase::remote_config::Initialize(*app);
	});

	while (m_remoteConfigInitializer->InitializeLastResult().status() != firebase::kFutureStatusComplete) {
		if (ProcessEvents(100)) return;  // exit if requested
	}

	if (m_remoteConfigInitializer->InitializeLastResult().error() != 0) {
		LOG("Failed to initialize Firebase Remote Config: %s", m_remoteConfigInitializer->InitializeLastResult().error_message());
		ProcessEvents(2000);
		return;
	}

	LOG("Initialized the Firebase Remote Config API");

	if(remoteDefaultValues.size() > 0)
		firebase::remote_config::SetDefaults(&remoteDefaultValues[0], remoteDefaultValues.size());

	remoteDefaultValues.clear();
}

void FirebaseImpl::RemoteConfigRelease()
{
	delete m_remoteConfigInitializer;
	firebase::remote_config::Terminate();
}

void FirebaseImpl::RemoteConfigFetchAll()
{
	auto future_result = firebase::remote_config::Fetch(0);
	while (future_result.status() == firebase::kFutureStatusPending) {
		if (ProcessEvents(1000)) {
			break;
		}
	}

	if (future_result.status() == firebase::kFutureStatusComplete) {
		bool activate_result = firebase::remote_config::ActivateFetched();
		LOG("ActivateFetched %s", activate_result ? "succeeded" : "failed");
	}
}

void FirebaseImpl::WaitForFutureCompletion(firebase::FutureBase future, firebase::FutureStatus toCheck, int msec, double timeout)
{
    double time = GetTime();
    while (ProcessEvents(msec))
    {
        double elapsedTime = GetTime() - time;
        if (future.status() != firebase::kFutureStatusPending || elapsedTime > timeout)
        {
            break;
        }
    }
}

double FirebaseImpl::GetTime()
{
#if defined(_WIN32)
	static LARGE_INTEGER cuurentTime;
	QueryPerformanceCounter(&cuurentTime);
	return (double)cuurentTime.QuadPart / (double)freq.QuadPart;
#elif defined __ANDROID__
	struct timespec tv;
	clock_gettime(CLOCK_MONOTONIC, &tv);
	return (double)tv.tv_sec + (double)tv.tv_nsec / 1000000000.0;
#else
	uint64_t t = mach_absolute_time();
	double tsec = (double)t * (double)timebase.numer / (double)timebase.denom / 1000000000.0;
	return tsec;
#endif
}