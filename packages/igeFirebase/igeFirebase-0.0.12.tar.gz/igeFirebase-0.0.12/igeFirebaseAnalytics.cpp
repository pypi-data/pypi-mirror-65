#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"

void ParseFirebaseAnalytics(std::vector<analytics::Parameter> &analyticParameters, PyObject* parameters, PyObject* parameter_value)
{
	if (PyBytes_Check(parameter_value))
	{
		const char* value = PyBytes_AsString(parameter_value);
		const char* name = PyUnicode_AsUTF8(parameters);
		analyticParameters.push_back(analytics::Parameter(name, value));
	}
	else if (PyFloat_Check(parameter_value))
	{
		const double value = PyFloat_AsDouble(parameter_value);
		const char* name = PyUnicode_AsUTF8(parameters);
		analyticParameters.push_back(analytics::Parameter(name, value));
	}
	else if (PyLong_Check(parameter_value))
	{
		const int value = PyLong_AsLong(parameter_value);
		const char* name = PyUnicode_AsUTF8(parameters);
		analyticParameters.push_back(analytics::Parameter(name, value));
	}
	else
	{
		const char* value = PyUnicode_AsUTF8(parameter_value);
		const char* name = PyUnicode_AsUTF8(parameters);
		analyticParameters.push_back(analytics::Parameter(name, value));
	}
}

PyObject* firebaseAnalytics_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseAnalytics_obj* self = NULL;

	self = (firebaseAnalytics_obj*)type->tp_alloc(type, 0);
	self->firebaseAnalytics = new FirebaseAnalytics();

	return (PyObject*)self;
}

void firebaseAnalytics_dealloc(firebaseAnalytics_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseAnalytics_str(firebaseAnalytics_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase analytics object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseAnalytics_Init(firebaseAnalytics_obj* self)
{
	self->firebaseAnalytics->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAnalytics_Release(firebaseAnalytics_obj* self)
{
	self->firebaseAnalytics->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAnalytics_Testcase(firebaseAnalytics_obj* self)
{
	self->firebaseAnalytics->testcase();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAnalytics_LogEvent(firebaseAnalytics_obj* self, PyObject* args)
{
	char* eventName;
	PyObject* parameters = nullptr;
	PyObject* parameter_value = nullptr;

	if (!PyArg_ParseTuple(args, "s|OO", &eventName, &parameters, &parameter_value)) return NULL;

	std::vector<analytics::Parameter> analyticParameters;
	if (parameters && PyTuple_Check(parameters))
	{
		uint32_t numAttr = (uint32_t)PyTuple_Size(parameters);

		for (uint32_t i = 0; i < numAttr; i++)
		{
			PyObject* v = PyTuple_GET_ITEM(parameters, i);
			if (PyTuple_Check(v))
			{
				int n = (int)PyTuple_Size(v);
				if (n != 2) { numAttr = 0; break; }

				ParseFirebaseAnalytics(analyticParameters, PyTuple_GET_ITEM(v, 0), PyTuple_GET_ITEM(v, 1));
			}
			else
			{
				ParseFirebaseAnalytics(analyticParameters, PyTuple_GET_ITEM(parameters, 0), PyTuple_GET_ITEM(parameters, 1));
				break;
			}
		}
		self->firebaseAnalytics->logEvent(eventName, &analyticParameters[0], analyticParameters.size());
		analyticParameters.clear();
	}
	else if (parameter_value)
	{
		ParseFirebaseAnalytics(analyticParameters, parameters, parameter_value);

		self->firebaseAnalytics->logEvent(eventName, &analyticParameters[0], analyticParameters.size());
		analyticParameters.clear();
	}
	else
	{
		self->firebaseAnalytics->logEvent(eventName);
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAnalytics_SetUserProperty(firebaseAnalytics_obj* self, PyObject* args)
{
	char* name = nullptr;
	char* property = nullptr;
	if (!PyArg_ParseTuple(args, "ss", &name, &property)) return NULL;

	self->firebaseAnalytics->setUserProperty(name, property);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAnalytics_SetUserId(firebaseAnalytics_obj* self, PyObject* args)
{
	char* user_id;
	if (!PyArg_ParseTuple(args, "s", &user_id)) return NULL;

	self->firebaseAnalytics->setUserId(user_id);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAnalytics_SetCurrentScreen(firebaseAnalytics_obj* self, PyObject* args)
{	
	char* screen_name;
	char* screen_class;
	if (!PyArg_ParseTuple(args, "ss", &screen_name, &screen_class)) return NULL;

	self->firebaseAnalytics->setCurrentScreen(screen_name, screen_class);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef firebaseAnalytics_methods[] = {
	{ "init", (PyCFunction)firebaseAnalytics_Init, METH_NOARGS, firebaseAnalyticsInit_doc },
	{ "release", (PyCFunction)firebaseAnalytics_Release, METH_NOARGS, firebaseAnalyticsRelease_doc },
	{ "testcase", (PyCFunction)firebaseAnalytics_Testcase, METH_NOARGS, firebaseAnalyticsTestcase_doc },
	{ "logEvent", (PyCFunction)firebaseAnalytics_LogEvent, METH_VARARGS, firebaseAnalyticsLogEvent_doc },
	{ "setUserProperty", (PyCFunction)firebaseAnalytics_SetUserProperty, METH_VARARGS, firebaseAnalyticsSetUserProperty_doc },
	{ "setUserId", (PyCFunction)firebaseAnalytics_SetUserId, METH_VARARGS, firebaseAnalyticsSetUserId_doc },
	{ "setCurrentScreen", (PyCFunction)firebaseAnalytics_SetCurrentScreen, METH_VARARGS, firebaseAnalyticsSetCurrentScreen_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseAnalytics_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseAnalyticsType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeFirebase.analytics",					/* tp_name */
	sizeof(firebaseAnalytics_obj),				/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseAnalytics_dealloc,		/* tp_dealloc */
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
	(reprfunc)firebaseAnalytics_str,			/* tp_str */
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
	firebaseAnalytics_methods,					/* tp_methods */
	0,											/* tp_members */
	firebaseAnalytics_getsets,					/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseAnalytics_new,						/* tp_new */
	0,											/* tp_free */
};