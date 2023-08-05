#include "FirebaseRemoteConfig.h"
#include "firebase/remote_config.h"

#include <fstream>
#include <sstream>

FirebaseRemoteConfig* FirebaseRemoteConfig::instance = nullptr;
using namespace firebase;

template <typename Out>
void split(const std::string& s, char delim, Out result) {
	std::istringstream iss(s);
	std::string item;
	while (std::getline(iss, item, delim)) {
		*result++ = item;
	}
}

std::vector<std::string> split(const std::string& s, char delim) {
	std::vector<std::string> elems;
	split(s, delim, std::back_inserter(elems));
	return elems;
}

const char* ValueSourceToString(firebase::remote_config::ValueSource source) {
	static const char* kSourceToString[] = {
	  "Static",   // kValueSourceStaticValue
	  "Remote",   // kValueSourceRemoteValue
	  "Default",  // kValueSourceDefaultValue
	};
	return kSourceToString[source];
}

FirebaseRemoteConfig::FirebaseRemoteConfig()
{
	LOG("FirebaseRemoteConfig()");
}
FirebaseRemoteConfig::~FirebaseRemoteConfig()
{
	LOG("~FirebaseRemoteConfig()");
}

void FirebaseRemoteConfig::init()
{
	
}

void FirebaseRemoteConfig::release()
{	
}

void FirebaseRemoteConfig::FetchAll()
{
	GetImpl()->RemoteConfigFetchAll();
}


json FirebaseRemoteConfig::Preprocess(const char* key)
{
	std::vector<std::string> steps = split(key, '.');

	remote_config::ValueInfo value_info;
	auto result = remote_config::GetString(steps[0].c_str(), &value_info);
	if (result.empty() || result == "null")	return "";

	json result_json;
	std::stringstream(result) >> result_json;

	for (int i = 1; i < steps.size() ; i++)
	{
		if (result.empty() || result == "null")	return "";
		result_json = result_json[steps[i]];
	}

	return result_json;
}

std::string FirebaseRemoteConfig::GetString(const char* key)
{
	json result = Preprocess(key);
	if(result.is_string())
		return result.get<std::string>();

	return result.dump();
}

long FirebaseRemoteConfig::GetLong(const char* key)
{
	json result = Preprocess(key);
	if (result.is_number_integer())
		return result.get<int32_t>();

	return 0;
}

double FirebaseRemoteConfig::GetDouble(const char* key)
{
	json result = Preprocess(key);
	if (result.is_number_float())
		return result.get<float>();

	return 0.0;
}

bool FirebaseRemoteConfig::GetBoolean(const char* key)
{
	json result = Preprocess(key);
	if (result.is_boolean())
		return result.get<bool>();

	return false;
}