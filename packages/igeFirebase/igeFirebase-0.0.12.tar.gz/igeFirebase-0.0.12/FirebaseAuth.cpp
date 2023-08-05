#include "FirebaseAuth.h"

class AuthStateChangeCounter : public firebase::auth::AuthStateListener {
public:
	AuthStateChangeCounter() : num_state_changes_(0) {}

	virtual void OnAuthStateChanged(Auth* auth) {  // NOLINT
		num_state_changes_++;
		LOG("OnAuthStateChanged User %p (state changes %d)",
			auth->current_user(), num_state_changes_);
	}

	void CompleteTest(const char* test_name, int expected_state_changes) {
		CompleteTest(test_name, expected_state_changes, expected_state_changes);
	}

	void CompleteTest(const char* test_name, int min_state_changes,
		int max_state_changes) {
		const bool success = min_state_changes <= num_state_changes_ &&
			num_state_changes_ <= max_state_changes;
		LOG("%sAuthStateListener called %d time%s on %s.",
			success ? "" : "ERROR: ", num_state_changes_,
			num_state_changes_ == 1 ? "" : "s", test_name);
		num_state_changes_ = 0;
	}

private:
	int num_state_changes_;
};

class IdTokenChangeCounter : public firebase::auth::IdTokenListener {
public:
	IdTokenChangeCounter() : num_token_changes_(0) {}

	virtual void OnIdTokenChanged(Auth* auth) {  // NOLINT
		num_token_changes_++;
		LOG("OnIdTokenChanged User %p (token changes %d)",
			auth->current_user(), num_token_changes_);
	}

	void CompleteTest(const char* test_name, int token_changes) {
		CompleteTest(test_name, token_changes, token_changes);
	}

	void CompleteTest(const char* test_name, int min_token_changes,
		int max_token_changes) {
		const bool success = min_token_changes <= num_token_changes_ &&
			num_token_changes_ <= max_token_changes;
		LOG("%sIdTokenListener called %d time%s on %s.",
			success ? "" : "ERROR: ", num_token_changes_,
			num_token_changes_ == 1 ? "" : "s", test_name);
		num_token_changes_ = 0;
	}

private:
	int num_token_changes_;
};


class PhoneListener : public PhoneAuthProvider::Listener {
public:
	PhoneListener()
		: num_calls_on_verification_complete_(0),
		num_calls_on_verification_failed_(0),
		num_calls_on_code_sent_(0),
		num_calls_on_code_auto_retrieval_time_out_(0) {}

	void OnVerificationCompleted(Credential /*credential*/) override {
		LOG("PhoneListener: successful automatic verification.");
		num_calls_on_verification_complete_++;
	}

	void OnVerificationFailed(const std::string& error) override {
		LOG("ERROR: PhoneListener verification failed with error, %s",
			error.c_str());
		num_calls_on_verification_failed_++;
	}

	void OnCodeSent(const std::string& verification_id,
		const PhoneAuthProvider::ForceResendingToken&
		force_resending_token) override {
		LOG("PhoneListener: code sent. verification_id=%s",
			verification_id.c_str());
		verification_id_ = verification_id;
		force_resending_token_ = force_resending_token;
		num_calls_on_code_sent_++;
	}

	void OnCodeAutoRetrievalTimeOut(const std::string& verification_id) override {
		LOG("PhoneListener: auto retrieval timeout. verification_id=%s",
			verification_id.c_str());
		verification_id_ = verification_id;
		num_calls_on_code_auto_retrieval_time_out_++;
	}

	const std::string& verification_id() const { return verification_id_; }
	const PhoneAuthProvider::ForceResendingToken& force_resending_token() const {
		return force_resending_token_;
	}
	int num_calls_on_verification_complete() const {
		return num_calls_on_verification_complete_;
	}
	int num_calls_on_verification_failed() const {
		return num_calls_on_verification_failed_;
	}
	int num_calls_on_code_sent() const { return num_calls_on_code_sent_; }
	int num_calls_on_code_auto_retrieval_time_out() const {
		return num_calls_on_code_auto_retrieval_time_out_;
	}

private:
	std::string verification_id_;
	PhoneAuthProvider::ForceResendingToken force_resending_token_;
	int num_calls_on_verification_complete_;
	int num_calls_on_verification_failed_;
	int num_calls_on_code_sent_;
	int num_calls_on_code_auto_retrieval_time_out_;
};

FirebaseAuth::FirebaseAuth()
{
	LOG("FirebaseAuth()");
}
FirebaseAuth::~FirebaseAuth()
{
	LOG("~FirebaseAuth()");
}

void FirebaseAuth::init()
{
	LOG("Initializing the Auth with Firebase API.");	
	
	LOG("Created the Firebase app %x.", static_cast<int>(reinterpret_cast<intptr_t>(firebase_app)));
	// Create the Auth class for that App.

	::firebase::ModuleInitializer initializer;
	initializer.Initialize(firebase_app, nullptr, [](::firebase::App* app, void*) {
		::firebase::InitResult init_result;
		Auth::GetAuth(app, &init_result);
		return init_result;
		});
	while (initializer.InitializeLastResult().status() !=
		firebase::kFutureStatusComplete) {
		if (GetImpl()->ProcessEvents(1000)) return;  // exit if requested
	}

	if (initializer.InitializeLastResult().error() != 0) {
		LOG("Failed to initialize Auth: %s",
			initializer.InitializeLastResult().error_message());
		GetImpl()->ProcessEvents(2000);
		return;
	}

	m_auth = Auth::GetAuth(firebase_app);

	LOG("Created the Auth %x class for the Firebase app.",
		static_cast<int>(reinterpret_cast<intptr_t>(m_auth)));
}

void FirebaseAuth::release()
{
	LOG("FirebaseAuth::release()");
	delete m_auth;
}

bool FirebaseAuth::signInWithEmailAndPassword(char* username, char* password)
{
	Future<User*> sign_in_future = m_auth->SignInWithEmailAndPassword(username, password);
	WaitForSignInFuture( sign_in_future, "Auth::SignInWithEmailAndPassword() existing email and password", kAuthErrorNone, m_auth);

	if (sign_in_future.error() == kAuthErrorNone)
	{
		return true;
	}
	return false;
}

bool FirebaseAuth::signOut()
{
	if (m_auth->current_user() == nullptr)
	{
		LOG("No user signed in at creation time.");
		return false;
	}
	else
	{
		m_auth->SignOut();
		// Wait for the sign out to complete.
		WaitForSignOut(m_auth);

		if (m_auth->current_user() != nullptr)
		{
			return false;
		}
	}
	return true;
}

bool FirebaseAuth::isPlayerAuthenticated()
{
	return (m_auth->current_user() != nullptr);
}

bool FirebaseAuth::registerWithEmailAndPassword(char* username, char* password)
{
	Future<User*> register_account = m_auth->CreateUserWithEmailAndPassword(username, password);
	FirebaseAuth::WaitForSignInFuture(register_account, "CreateUserWithEmailAndPassword() to create user", kAuthErrorNone, m_auth);
	return (register_account.error() == kAuthErrorNone);
}

void FirebaseAuth::testcase()
{
	
}

bool FirebaseAuth::WaitForFuture(const FutureBase& future, const char* fn,
	AuthError expected_error, bool log_error) {
	// Note if the future has not be started properly.
	if (future.status() == ::firebase::kFutureStatusInvalid) {
		LOG("ERROR: Future for %s is invalid", fn);
		return false;
	}

	// Wait for future to complete.
	LOG("  Calling %s...", fn);
	while (future.status() == ::firebase::kFutureStatusPending) {
		if (GetImpl()->ProcessEvents(10000)) return true;
	}

	// Log error result.
	if (log_error) {
		const AuthError error = static_cast<AuthError>(future.error());
		if (error == expected_error) {
			const char* error_message = future.error_message();
			if (error_message) {
				LOG("%s completed as expected", fn);
			}
			else {
				LOG("%s completed as expected, error: %d '%s'", fn, error,
					error_message);
			}
		}
		else {
			LOG("ERROR: %s completed with error: %d, `%s`", fn, error,
				future.error_message());
		}
	}
	return false;
}


bool FirebaseAuth::WaitForSignInFuture(Future<User*> sign_in_future, const char* fn,
	AuthError expected_error, Auth* auth) {
	if (WaitForFuture(sign_in_future, fn, expected_error)) return true;

	const User* const* sign_in_user_ptr = sign_in_future.result();
	const User* sign_in_user =
		sign_in_user_ptr == nullptr ? nullptr : *sign_in_user_ptr;
	const User* auth_user = auth->current_user();

	if (expected_error == ::firebase::auth::kAuthErrorNone &&
		sign_in_user != auth_user) {
		LOG("ERROR: future's user (%x) and current_user (%x) don't match",
			static_cast<int>(reinterpret_cast<intptr_t>(sign_in_user)),
			static_cast<int>(reinterpret_cast<intptr_t>(auth_user)));
	}

	return false;
}

bool FirebaseAuth::WaitForSignInFuture(const Future<SignInResult>& sign_in_future,
	const char* fn, AuthError expected_error,
	Auth* auth) {
	if (WaitForFuture(sign_in_future, fn, expected_error)) return true;

	const SignInResult* sign_in_result = sign_in_future.result();
	const User* sign_in_user = sign_in_result ? sign_in_result->user : nullptr;
	const User* auth_user = auth->current_user();

	if (expected_error == ::firebase::auth::kAuthErrorNone &&
		sign_in_user != auth_user) {
		LOG("ERROR: future's user (%x) and current_user (%x) don't match",
			static_cast<int>(reinterpret_cast<intptr_t>(sign_in_user)),
			static_cast<int>(reinterpret_cast<intptr_t>(auth_user)));
	}

	return false;
}

// Wait for the current user to sign out.  Typically you should use the
// state listener to determine whether the user has signed out.
bool FirebaseAuth::WaitForSignOut(firebase::auth::Auth* auth) {
	while (auth->current_user() != nullptr) {
		if (GetImpl()->ProcessEvents(1000)) return true;
	}
	// Wait - hopefully - long enough for listeners to be signalled.
	GetImpl()->ProcessEvents(1000);
	return false;
}

// Create an email that will be different from previous runs.
// Useful for testing creating new accounts.
std::string FirebaseAuth::CreateNewEmail() {
	std::stringstream email;
	email << "random_" << std::time(0) << "@gmail.com";
	return email.str();
}

void FirebaseAuth::ExpectFalse(const char* test, bool value) {
	if (value) {
		LOG("ERROR: %s is true instead of false", test);
	}
	else {
		LOG("%s is false, as expected", test);
	}
}

void FirebaseAuth::ExpectTrue(const char* test, bool value) {
	if (value) {
		LOG("%s is true, as expected", test);
	}
	else {
		LOG("ERROR: %s is false instead of true", test);
	}
}

// Log results of a string comparison for `test`.
void FirebaseAuth::ExpectStringsEqual(const char* test, const char* expected,
	const char* actual) {
	if (strcmp(expected, actual) == 0) {
		LOG("%s is '%s' as expected", test, actual);
	}
	else {
		LOG("ERROR: %s is '%s' instead of '%s'", test, actual, expected);
	}
}

// Log a vector of variants.
void FirebaseAuth::LogVariantVector(const std::vector<Variant>& variants, int indent) {
	std::string indent_string(indent * 2, ' ');
	LOG("%s[", indent_string.c_str());
	for (auto it = variants.begin(); it != variants.end(); ++it) {
		const Variant& item = *it;
		if (item.is_fundamental_type()) {
			const Variant& string_value = item.AsString();
			LOG("%s  %s,", indent_string.c_str(), string_value.string_value());
		}
		else if (item.is_vector()) {
			LogVariantVector(item.vector(), indent + 2);
		}
		else if (item.is_map()) {
			LogVariantMap(item.map(), indent + 2);
		}
		else {
			LOG("%s  ERROR: unknown type %d", indent_string.c_str(),
				static_cast<int>(item.type()));
		}
	}
	LOG("%s]", indent_string.c_str());
}

// Log a map of variants.
void FirebaseAuth::LogVariantMap(const std::map<Variant, Variant>& variant_map,
	int indent) {
	std::string indent_string(indent * 2, ' ');
	for (auto it = variant_map.begin(); it != variant_map.end(); ++it) {
		const Variant& key_string = it->first.AsString();
		const Variant& value = it->second;
		if (value.is_fundamental_type()) {
			const Variant& string_value = value.AsString();
			LOG("%s%s: %s,", indent_string.c_str(), key_string.string_value(),
				string_value.string_value());
		}
		else {
			LOG("%s%s:", indent_string.c_str(), key_string.string_value());
			if (value.is_vector()) {
				LogVariantVector(value.vector(), indent + 1);
			}
			else if (value.is_map()) {
				LogVariantMap(value.map(), indent + 1);
			}
			else {
				LOG("%s  ERROR: unknown type %d", indent_string.c_str(),
					static_cast<int>(value.type()));
			}
		}
	}
}

// Display the sign-in result.
void FirebaseAuth::LogSignInResult(const SignInResult& result) {
	if (!result.user) {
		LOG("ERROR: User not signed in");
		return;
	}
	LOG("* User ID %s", result.user->uid().c_str());
	const AdditionalUserInfo& info = result.info;
	LOG("* Provider ID %s", info.provider_id.c_str());
	LOG("* User Name %s", info.user_name.c_str());
	LogVariantMap(info.profile, 0);
	const UserMetadata& metadata = result.meta;
	LOG("* Sign in timestamp %d",
		static_cast<int>(metadata.last_sign_in_timestamp));
	LOG("* Creation timestamp %d",
		static_cast<int>(metadata.creation_timestamp));
}
