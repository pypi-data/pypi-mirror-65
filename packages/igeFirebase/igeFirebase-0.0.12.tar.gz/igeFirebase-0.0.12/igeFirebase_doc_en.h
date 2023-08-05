//firebase init
PyDoc_STRVAR(firebaseInit_doc,
	"init the Firebase system \n"\
	"\n"\
	"firebase.init(analytics=,messaging,remoteConfig)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    analytics, messaging, remoteConfig : boolean (optional)");

//firebase release
PyDoc_STRVAR(firebaseRelease_doc,
	"release the Firebase system\n"\
	"\n"\
	"firebase.release()");

//firebase is ready
PyDoc_STRVAR(firebaseIsReady_doc,
    "check if firebase is ready for call the api\n"\
    "\n"\
    "firebase.isReady()");

//firebase testcase
PyDoc_STRVAR(firebaseTestcase_doc,
	"The testcase for firebase\n"\
	"\n"\
	"firebase.testcase()");

//firebase analytics init
PyDoc_STRVAR(firebaseAnalyticsInit_doc,
	"init the Firebase Analytics system \n"\
	"\n"\
	"firebaseAnalytics.init()");

//firebase analytics release
PyDoc_STRVAR(firebaseAnalyticsRelease_doc,
	"release the Firebase Anlytics system\n"\
	"\n"\
	"firebaseAnalytics.release()");

//firebase analytics testcase
PyDoc_STRVAR(firebaseAnalyticsTestcase_doc,
	"The testcase for firebase analytics\n"\
	"\n"\
	"firebaseAnalytics.testcase()");

//firebase analytics logEvent
PyDoc_STRVAR(firebaseAnalyticsLogEvent_doc,
	"sent the event\n"\
	"\n"\
	"firebaseAnalytics.logEvent(name, value)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string\n"\
	"        The event name\n"\
	"    value : string\n"\
	"        Tuple of value pass to the event");

// firebase analytics setUserProperty
PyDoc_STRVAR(firebaseAnalyticsSetUserProperty_doc,
	"Set a user property to the given value.\n"\
	"\n"\
	"firebaseAnalytics.setUserProperty(name, property)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    name : string\n"\
	"        Name of the user property to set\n"\
	"    property : string\n"\
	"        Value to set the user property to. Set this argument to NULL or nullptr to remove the user property.  The value can be between 1 to 100 characters long.");

// firebase analytics setUserId
PyDoc_STRVAR(firebaseAnalyticsSetUserId_doc,
	"Sets the user ID property.\n"\
	"\n"\
	"firebaseAnalytics.setUserId(user_id)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    user_id : string\n"\
	"        The user ID associated with the user of this app on this device.  The user ID must be non-empty and no more than 256 characters long. Setting user_id to NULL or nullptr removes the user ID.");

// firebase analytics SetCurrentScreen
PyDoc_STRVAR(firebaseAnalyticsSetCurrentScreen_doc,
	"Sets the current screen name and screen class, which specifies the current visual context in your app. This helps identify the areas in your app where users spend their time and how they interact with your app.\n"\
	"\n"\
	"firebaseAnalytics.setCurrentScreen(screen_name, screen_class)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    screen_name : string\n"\
	"        The name of the current screen. Set to nullptr to clear the current screen name. Limited to 100 characters.\n"\
	"    screen_class : string\n"\
	"        The name of the screen class. If you specify nullptr for this, it will use the default. On Android, the default is the class name of the current Activity. On iOS, the default is the class name of the current UIViewController. Limited to 100 characters.");
    
 //firebase auth init
PyDoc_STRVAR(firebaseAuthInit_doc,
	"init the Firebase Auth system \n"\
	"\n"\
	"firebaseAuth.init()");

//firebase auth release
PyDoc_STRVAR(firebaseAuthRelease_doc,
	"release the Firebase Auth system\n"\
	"\n"\
	"firebaseAuth.release()");

//firebase auth testcase
PyDoc_STRVAR(firebaseAuthTestcase_doc,
	"The testcase for firebase Auth\n"\
	"\n"\
	"firebaseAuth.testcase()");
    
// firebase auth signInWithEmailAndPassword
PyDoc_STRVAR(firebaseAuthSignInWithEmailAndPassword_doc,
	"Signs in using provided email address and password.\n"\
	"\n"\
	"firebaseAuth.signInWithEmailAndPassword(username, password)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    username : string\n"\
	"    password : string\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");
    
// firebase auth signOut
PyDoc_STRVAR(firebaseAuthSignOut_doc,
	"Removes any existing authentication credentials from this client.\n"\
	"\n"\
	"firebaseAuth.signOut()\n"\
	"\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");
    
// firebase auth isPlayerAuthenticated
PyDoc_STRVAR(firebaseAuthIsPlayerAuthenticated_doc,
	"return true if the user is signed in, false otherwise.\n"\
	"\n"\
	"firebaseAuth.isPlayerAuthenticated()\n"\
	"\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");
    
// firebase auth registerWithEmailAndPassword
PyDoc_STRVAR(firebaseAuthRegisterWithEmailAndPassword_doc,
	"Creates, and on success, logs in a user with the given email address and password..\n"\
    "An error is returned when account creation is unsuccessful (due to another existing account, invalid password, etc.)..\n"\
	"\n"\
	"firebaseAuth.registerWithEmailAndPassword(username, password)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    username : string\n"\
	"    password : string\n"\
    "Returns\n"\
	"-------\n"\
	"    result : bool");

//firebase messaging init
PyDoc_STRVAR(firebaseMessagingInit_doc,
	"init the Firebase Messaging system \n"\
	"\n"\
	"firebaseMessaging.init()");

//firebase messaging release
PyDoc_STRVAR(firebaseMessagingRelease_doc,
	"release the Firebase Messaging system\n"\
	"\n"\
	"firebaseMessaging.release()");

//firebase messaging get registration token
PyDoc_STRVAR(firebaseMessagingGetRegistrationToken_doc,
	"get the registration token\n"\
	"\n"\
	"firebaseMessaging.getRegistrationToken()\n"\
	"Returns\n"\
	"-------\n"\
	"    token : string");

//firebase remote config init
PyDoc_STRVAR(firebaseRemoteConfigInit_doc,
	"init the Firebase Remote Config system \n"\
	"\n"\
	"firebaseRemoteConfig.init()");

//firebase remote config release
PyDoc_STRVAR(firebaseRemoteConfigRelease_doc,
	"release the Firebase Remote Config system\n"\
	"\n"\
	"firebaseRemoteConfig.release()");

//firebase remote config get string
PyDoc_STRVAR(firebaseRemoteConfigGetString_doc,
	"get the string result\n"\
	"\n"\
	"firebaseRemoteConfig.getString(key)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    key : string\n"\
	"Returns\n"\
	"-------\n"\
	"    result : string");

//firebase remote config get long
PyDoc_STRVAR(firebaseRemoteConfigGetLong_doc,
	"get the long result\n"\
	"\n"\
	"firebaseRemoteConfig.getLong(key)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    key : string\n"\
	"Returns\n"\
	"-------\n"\
	"    result : long");

//firebase remote config get float
PyDoc_STRVAR(firebaseRemoteConfigGetFloat_doc,
	"get the long result\n"\
	"\n"\
	"firebaseRemoteConfig.getFloat(key)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    key : string\n"\
	"Returns\n"\
	"-------\n"\
	"    result : float");

//firebase remote config get boolean
PyDoc_STRVAR(firebaseRemoteConfigGetBoolean_doc,
	"get the bool result\n"\
	"\n"\
	"firebaseRemoteConfig.getBoolean(key)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    key : string\n"\
	"Returns\n"\
	"-------\n"\
	"    result : boolean");

//firebase remote config fetch
PyDoc_STRVAR(firebaseRemoteConfigFetch_doc,
	"fetch the new data\n"\
	"\n"\
	"firebaseRemoteConfig.fetch()");

//firebase MLKit is supported or not
PyDoc_STRVAR(firebaseMLKitIsSupported_doc,
	"checking if the mlKit is supported by plarform or not \n"\
	"\n"\
	"firebaseMLKit.isSupported()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result : boolean");

//firebase MLKit init
PyDoc_STRVAR(firebaseMLKitInit_doc,
	"init the Firebase MLKit system \n"\
	"\n"\
	"firebaseMLKit.init()\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    mode : int (optional) 1 = FAST ; 2 = ACCURATE");

//firebase MLKit release
PyDoc_STRVAR(firebaseMLKitRelease_doc,
	"release the Firebase MLKit system\n"\
	"\n"\
	"firebaseMLKit.release()");

//firebase MLKit preview mode
PyDoc_STRVAR(firebaseMLKitPreview_doc,
	"preview the Firebase MLKit system\n"\
	"\n"\
	"firebaseMLKit.preview()");

//firebase MLKit get contours point
PyDoc_STRVAR(firebaseMLKitGetContours_doc,
	"Get the contours point\n"\
	"\n"\
	"firebaseMLKit.getContours()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result : list(float)");

//firebase MLKit get head euler angle
PyDoc_STRVAR(firebaseMLKitGetHeadEulerAngle_doc,
	"Get the head euler angle\n"\
	"\n"\
	"firebaseMLKit.getHeadEulerAngle()\n"\
	"\n"\
	"Returns\n"\
	"-------\n"\
	"    result : tuple(y,z)");

//get camera size
PyDoc_STRVAR(cameraGetCameraSize_doc,
    "get the camera size\n"\
    "\n"\
    "igeCamera.getCameraSize()\n"\
    "\n"\
    "Returns\n"\
    "-------\n"\
    "    result : tuple(w, h)");

//get camera data
PyDoc_STRVAR(cameraGetCameraData_doc,
    "Get the camera data\n"\
    "\n"\
    "igeCamera.getCameraData()\n"\
    "\n"\
    "Returns\n"\
    "-------\n"\
    "    result : list(unsigned char)");
