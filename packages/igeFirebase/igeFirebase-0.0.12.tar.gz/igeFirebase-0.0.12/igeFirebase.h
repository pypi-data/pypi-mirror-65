#include <Python.h>
#include "Firebase.h"
#include "FirebaseAnalytics.h"
#include "FirebaseAuth.h"
#include "FirebaseMessaging.h"
#include "FirebaseRemoteConfig.h"
#include "FirebaseMLKit.h"

typedef struct {
	PyObject_HEAD
		Firebase* firebase;
} firebase_obj;

typedef struct {
	PyObject_HEAD
		FirebaseAnalytics* firebaseAnalytics;
} firebaseAnalytics_obj;

typedef struct {
	PyObject_HEAD
		FirebaseAuth* firebaseAuth;
} firebaseAuth_obj;

typedef struct {
	PyObject_HEAD
		FirebaseMessaging* firebaseMessaging;
} firebaseMessaging_obj;

typedef struct {
	PyObject_HEAD
		FirebaseRemoteConfig* firebaseRemoteConfig;
} firebaseRemoteConfig_obj;

typedef struct {
	PyObject_HEAD
		FirebaseMLKit* firebaseMLKit;
} firebaseMLKit_obj;

extern PyTypeObject FirebaseType;
extern PyTypeObject FirebaseAnalyticsType;
extern PyTypeObject FirebaseAuthType;
extern PyTypeObject FirebaseMessagingType;
extern PyTypeObject FirebaseRemoteConfigType;
extern PyTypeObject FirebaseMLKitType;
