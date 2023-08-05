#pragma once
#include "Firebase.h"

#include "firebase/analytics.h"

namespace analytics = ::firebase::analytics;
class IGE_EXPORT FirebaseAnalytics : public Firebase
{
public:
	FirebaseAnalytics();
	~FirebaseAnalytics();
	void init();
	void release();
	void testcase();

	void setSessionTimeoutDuration(int64_t milliseconds);
	void setUserProperty(const char* name, const char* property);
	void setUserId(const char* user_id);
	void setCurrentScreen(const char* screen_name, const char* screen_class);

	void logEvent(const char* name);
	void logEvent(const char* name, const char* parameter_name, const double parameter_value);
	void logEvent(const char* name, const char* parameter_name, const int parameter_value);
	void logEvent(const char* name, const char* parameter_name, const char* parameter_value);
	void logEvent(const char* name, const analytics::Parameter* parameters, size_t number_of_parameters);
};
