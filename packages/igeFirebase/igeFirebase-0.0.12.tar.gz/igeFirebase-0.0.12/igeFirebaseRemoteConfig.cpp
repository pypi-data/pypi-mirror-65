#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"


PyObject* firebaseRemoteConfig_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseRemoteConfig_obj* self = NULL;

	self = (firebaseRemoteConfig_obj*)type->tp_alloc(type, 0);
	self->firebaseRemoteConfig = FirebaseRemoteConfig::Instance();

	return (PyObject*)self;
}

void firebaseRemoteConfig_dealloc(firebaseRemoteConfig_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseRemoteConfig_str(firebaseRemoteConfig_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase remote config object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseRemoteConfig_Init(firebaseRemoteConfig_obj* self)
{
	FirebaseRemoteConfig::Instance()->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseRemoteConfig_Release(firebaseRemoteConfig_obj* self)
{
	FirebaseRemoteConfig::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseRemoteConfig_GetString(firebaseRemoteConfig_obj* self, PyObject* args)
{
	char* key = nullptr;
	if (!PyArg_ParseTuple(args, "s", &key)) return NULL;

	std::string result = FirebaseRemoteConfig::Instance()->GetString(key);
	PyObject* obj = PyBytes_FromString(result.c_str());

	return obj;
}

static PyObject* firebaseRemoteConfig_GetLong(firebaseRemoteConfig_obj* self, PyObject* args)
{
	char* key = nullptr;
	if (!PyArg_ParseTuple(args, "s", &key)) return NULL;

	return PyLong_FromLong(FirebaseRemoteConfig::Instance()->GetLong(key));
}

static PyObject* firebaseRemoteConfig_GetFloat(firebaseRemoteConfig_obj* self, PyObject* args)
{
	char* key = nullptr;
	if (!PyArg_ParseTuple(args, "s", &key)) return NULL;

	return PyFloat_FromDouble(FirebaseRemoteConfig::Instance()->GetDouble(key));
}

static PyObject* firebaseRemoteConfig_GetBoolean(firebaseRemoteConfig_obj* self, PyObject* args)
{
	char* key = nullptr;
	if (!PyArg_ParseTuple(args, "s", &key)) return NULL;

	return PyBool_FromLong(FirebaseRemoteConfig::Instance()->GetBoolean(key));
}

static PyObject* firebaseRemoteConfig_FetchAll(firebaseRemoteConfig_obj* self)
{
	FirebaseRemoteConfig::Instance()->FetchAll();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef firebaseRemoteConfig_methods[] = {
	{ "init", (PyCFunction)firebaseRemoteConfig_Init, METH_NOARGS, firebaseRemoteConfigInit_doc },
	{ "release", (PyCFunction)firebaseRemoteConfig_Release, METH_NOARGS, firebaseRemoteConfigRelease_doc },
	{ "getString", (PyCFunction)firebaseRemoteConfig_GetString, METH_VARARGS, firebaseRemoteConfigGetString_doc },
	{ "getLong", (PyCFunction)firebaseRemoteConfig_GetLong, METH_VARARGS, firebaseRemoteConfigGetLong_doc },
	{ "getFloat", (PyCFunction)firebaseRemoteConfig_GetFloat, METH_VARARGS, firebaseRemoteConfigGetFloat_doc },
	{ "getBoolean", (PyCFunction)firebaseRemoteConfig_GetBoolean, METH_VARARGS, firebaseRemoteConfigGetBoolean_doc },
	{ "fetch", (PyCFunction)firebaseRemoteConfig_FetchAll, METH_NOARGS, firebaseRemoteConfigFetch_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseRemoteConfig_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseRemoteConfigType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igefirebase.remoteConfig",					/* tp_name */
	sizeof(firebaseRemoteConfig_obj),			/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseRemoteConfig_dealloc,	/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)firebaseRemoteConfig_str,			/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	firebaseRemoteConfig_methods,				/* tp_methods */
	0,											/* tp_members */
	firebaseRemoteConfig_getsets,				/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseRemoteConfig_new,					/* tp_new */
	0,											/* tp_free */
};