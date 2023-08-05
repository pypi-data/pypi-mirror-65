#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"

namespace firebase
{
	int pyObjToIntArray(PyObject* obj, uint32_t* idx) {

		int totalCount = 0;
		int type = -1;
		if (PyTuple_Check(obj)) type = 0;
		else if (PyList_Check(obj))  type = 1;
		if (type == -1) return 0;

		int elementCount = 0;
		int numElem = (type == 0) ? PyTuple_Size(obj) : PyList_Size(obj);
		for (int i = 0; i < numElem; i++) {
			PyObject* element = (type == 0) ? PyTuple_GET_ITEM(obj, i) : PyList_GET_ITEM(obj, i);
			if (PyLong_Check(element)) {
				if (idx)idx[totalCount] = PyLong_AsLong(element);
				totalCount++;
				elementCount++;
				if (elementCount >= 3) elementCount = 0;
			}
			else if (PyTuple_Check(element)) {
				int d = (int)PyTuple_Size(element);
				for (int j = 0; j < d; j++) {
					PyObject* val = PyTuple_GET_ITEM(element, j);
					if (idx)idx[totalCount] = PyLong_AsLong(val);
					totalCount++;
					elementCount++;
					if (elementCount >= 3) break;
				}
				elementCount = 0;
			}
			else if (PyList_Check(element)) {
				int d = (int)PyList_Size(element);
				for (int j = 0; j < d; j++) {
					PyObject* val = PyList_GET_ITEM(element, j);
					if (idx)idx[totalCount] = PyLong_AsLong(val);
					totalCount++;
					elementCount++;
					if (elementCount >= 3) break;
				}
				elementCount = 0;
			}
		}
		return totalCount;
	}
}

PyObject* firebase_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebase_obj* self = NULL;

	self = (firebase_obj*)type->tp_alloc(type, 0);
	self->firebase = new Firebase();

	return (PyObject*)self;
}

void firebase_dealloc(firebase_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebase_str(firebase_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebase_Init(firebase_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "analytics","messaging","remoteConfig",NULL };
	
	int analytics = 1;
	int messaging = 1;
	int remoteConfig = 1;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|iii", kwlist, &analytics, &messaging, &remoteConfig)) return NULL;

	self->firebase->init(analytics, messaging, remoteConfig);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebase_Release(firebase_obj* self)
{
	self->firebase->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebase_IsReady(firebase_obj* self)
{
    return PyLong_FromLong(self->firebase->isReady());
}

PyMethodDef firebase_methods[] = {
	{ "init", (PyCFunction)firebase_Init, METH_VARARGS | METH_KEYWORDS, firebaseInit_doc },
	{ "release", (PyCFunction)firebase_Release, METH_NOARGS, firebaseRelease_doc },
    { "isReady", (PyCFunction)firebase_IsReady, METH_NOARGS, firebaseIsReady_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebase_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeFirebase",						/* tp_name */
	sizeof(firebase_obj),				/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)firebase_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)firebase_str,				/* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	firebase_methods,					/* tp_methods */
	0,                                  /* tp_members */
	firebase_getsets,					/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	firebase_new,						/* tp_new */
	0,									/* tp_free */
};

static PyModuleDef firebase_module = {
	PyModuleDef_HEAD_INIT,
	"igeFirebase",						// Module name to use with Python import statements
	"Firebase Module.",					// Module description
	0,
	firebase_methods					// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeFirebase() {
	PyObject* module = PyModule_Create(&firebase_module);

	if (PyType_Ready(&FirebaseType) < 0) return NULL;
	if (PyType_Ready(&FirebaseAnalyticsType) < 0) return NULL;
	if (PyType_Ready(&FirebaseAuthType) < 0) return NULL;
	if (PyType_Ready(&FirebaseMessagingType) < 0) return NULL;
	if (PyType_Ready(&FirebaseRemoteConfigType) < 0) return NULL;
	if (PyType_Ready(&FirebaseMLKitType) < 0) return NULL;

	Py_INCREF(&FirebaseAnalyticsType);
	PyModule_AddObject(module, "analytics", (PyObject*)&FirebaseAnalyticsType);

	Py_INCREF(&FirebaseAuthType);
	PyModule_AddObject(module, "auth", (PyObject*)&FirebaseAuthType);

	Py_INCREF(&FirebaseMessagingType);
	PyModule_AddObject(module, "messaging", (PyObject*)&FirebaseMessagingType);

	Py_INCREF(&FirebaseRemoteConfigType);
	PyModule_AddObject(module, "remoteConfig", (PyObject*)&FirebaseRemoteConfigType);

	Py_INCREF(&FirebaseMLKitType);
	PyModule_AddObject(module, "mlKit", (PyObject*)&FirebaseMLKitType);

	return module;
}
