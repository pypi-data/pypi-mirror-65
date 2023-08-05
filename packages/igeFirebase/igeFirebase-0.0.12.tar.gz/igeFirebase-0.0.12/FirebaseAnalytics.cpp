#include "FirebaseAnalytics.h"

#include "firebase/analytics/event_names.h"
#include "firebase/analytics/parameter_names.h"
#include "firebase/analytics/user_property_names.h"

namespace analytics = ::firebase::analytics;

FirebaseAnalytics::FirebaseAnalytics()
{
	LOG("FirebaseAnalytics()");
}
FirebaseAnalytics::~FirebaseAnalytics()
{
	LOG("~FirebaseAnalytics()");
}

void FirebaseAnalytics::init()
{
}

void FirebaseAnalytics::release()
{		
}

void FirebaseAnalytics::setSessionTimeoutDuration(int64_t milliseconds)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::SetSessionTimeoutDuration(milliseconds);
}

void FirebaseAnalytics::setUserProperty(const char* name, const char* property)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::SetUserProperty(name, property);
}

void FirebaseAnalytics::setUserId(const char* user_id)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::SetUserId(user_id);
}

void FirebaseAnalytics::setCurrentScreen(const char* screen_name, const char* screen_class)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::SetCurrentScreen(screen_name, screen_class);
}

void FirebaseAnalytics::logEvent(const char* name)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::LogEvent(name);
}

void FirebaseAnalytics::logEvent(const char* name, const char* parameter_name, const double parameter_value)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::LogEvent(name, parameter_name, parameter_value);
}

void FirebaseAnalytics::logEvent(const char* name, const char* parameter_name, const int parameter_value)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::LogEvent(name, parameter_name, parameter_value);
}

void FirebaseAnalytics::logEvent(const char* name, const char* parameter_name, const char* parameter_value)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::LogEvent(name, parameter_name, parameter_value);
}

void FirebaseAnalytics::logEvent(const char* name, const analytics::Parameter* parameters, size_t number_of_parameters)
{
    if(GetImpl() && GetImpl()->IsReady())
        analytics::LogEvent(name, parameters, number_of_parameters);
}

void FirebaseAnalytics::testcase()
{
	LOG("Get App Instance ID...");
	auto future_result = analytics::GetAnalyticsInstanceId();
	GetImpl()->WaitForFutureCompletion(future_result);	

	LOG("Set user properties.");
	// Set the user's sign up method.
	setUserProperty(analytics::kUserPropertySignUpMethod, "Google");
	// Set the user ID.
	setUserId("uber_user_510");

	LOG("Set current screen.");
	// Set the user's current screen.
	setCurrentScreen("Firebase Analytics C++ testapp", "testapp");
	
	LOG("Log login event.");
	// Log an event with no parameters.
	logEvent(analytics::kEventLogin);
	
	LOG("Log progress event.");
	// Log an event with a floating point parameter.
	logEvent("progress", "percent", 0.4f);
	
	LOG("Log post score event.");
	// Log an event with an integer parameter.
	logEvent(analytics::kEventPostScore, analytics::kParameterScore, 42);
		
	LOG("Log group join event.");
	// Log an event with a string parameter.
	logEvent(analytics::kEventJoinGroup, analytics::kParameterGroupID, "spoon_welders");
	
	LOG("Log level up event.");
	// Log an event with multiple parameters.
	{
		const analytics::Parameter kLevelUpParameters[] = {
			analytics::Parameter(analytics::kParameterLevel, 5),
			analytics::Parameter(analytics::kParameterCharacter, "mrspoon"),
			analytics::Parameter("hit_accuracy", 3.14f),
		};
		logEvent(analytics::kEventLevelUp, kLevelUpParameters, sizeof(kLevelUpParameters) / sizeof(kLevelUpParameters[0]));
	}

	LOG("The Firebase Analytics Testcase Complete");
}
