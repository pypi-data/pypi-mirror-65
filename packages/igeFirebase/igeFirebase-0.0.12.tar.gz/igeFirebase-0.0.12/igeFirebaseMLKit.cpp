#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"

PyObject* firebaseMLKit_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseMLKit_obj* self = NULL;

	self = (firebaseMLKit_obj*)type->tp_alloc(type, 0);
	self->firebaseMLKit = FirebaseMLKit::Instance();

	return (PyObject*)self;
}

void firebaseMLKit_dealloc(firebaseMLKit_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseMLKit_str(firebaseMLKit_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase MLKit object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseMLKit_Init(firebaseMLKit_obj* self, PyObject* args)
{
	int mode = 1;	// 1 = FAST ; 2 = ACCURATE
	if (!PyArg_ParseTuple(args, "|i", &mode)) return NULL;

	FirebaseMLKit::Instance()->init(mode);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseMLKit_Release(firebaseMLKit_obj* self)
{
	FirebaseMLKit::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject* firebaseMLKit_Preview(firebaseMLKit_obj* self)
{
	FirebaseMLKit::Instance()->preview();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseMLKit_GetContours(firebaseMLKit_obj* self)
{
	int size = 0;
	float* contours = FirebaseMLKit::Instance()->getContours(size);

	PyObject* list = PyList_New(0);
	for (int i = 0; i < size - 1; i += 2)
	{
		PyObject* obj = Py_BuildValue("(ff)", contours[i], contours[i+1]);
		PyList_Append(list, obj);
	}
	return list;
}

static PyObject* firebaseMLKit_getHeadEulerAngle(firebaseMLKit_obj* self)
{
	PyObject* headEulerAngle = Py_BuildValue("{s:f,s:f}",
		"y", FirebaseMLKit::Instance()->getHeadEulerAngleY(),
		"z", FirebaseMLKit::Instance()->getHeadEulerAngleZ());


	return headEulerAngle;
}

static PyObject* firebaseMLKit_getHeadEulerAngleZ(firebaseMLKit_obj* self)
{
	return Py_BuildValue("f", FirebaseMLKit::Instance()->getHeadEulerAngleZ());
}

static PyObject* firebaseMLKit_isSupported(firebaseMLKit_obj* self)
{
	return PyBool_FromLong(FirebaseMLKit::Instance()->isSupported());
}


static PyObject* firebaseMLKit_GetCameraSize(firebaseMLKit_obj* self)
{
    PyObject* cameraSize = Py_BuildValue("{s:i,s:i}",
        "w", FirebaseMLKit::Instance()->getCameraWidth(),
        "h", FirebaseMLKit::Instance()->getCameraHeight());
    

    return cameraSize;
}

static PyObject* firebaseMLKit_GetCameraData(firebaseMLKit_obj* self)
{
    uint8_t* result = FirebaseMLKit::Instance()->getCameraData();
    PyObject* obj = PyBytes_FromStringAndSize((char*)result, FirebaseMLKit::Instance()->getCameraWidth() * FirebaseMLKit::Instance()->getCameraHeight() * 3);

    return obj;
}

PyMethodDef firebaseMLKit_methods[] = {
	{ "isSupported", (PyCFunction)firebaseMLKit_isSupported, METH_NOARGS, firebaseMLKitIsSupported_doc },
	{ "init", (PyCFunction)firebaseMLKit_Init, METH_VARARGS, firebaseMLKitInit_doc },
	{ "release", (PyCFunction)firebaseMLKit_Release, METH_NOARGS, firebaseMLKitRelease_doc },
	{ "preview", (PyCFunction)firebaseMLKit_Preview, METH_NOARGS, firebaseMLKitPreview_doc },
	{ "getContours", (PyCFunction)firebaseMLKit_GetContours, METH_NOARGS, firebaseMLKitGetContours_doc },
	{ "getHeadEulerAngle", (PyCFunction)firebaseMLKit_getHeadEulerAngle, METH_NOARGS, firebaseMLKitGetHeadEulerAngle_doc },
    { "getCameraSize", (PyCFunction)firebaseMLKit_GetCameraSize, METH_NOARGS, cameraGetCameraSize_doc },
    { "getCameraData", (PyCFunction)firebaseMLKit_GetCameraData, METH_NOARGS, cameraGetCameraData_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseMLKit_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseMLKitType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeFirebase.mlKit",						/* tp_name */
	sizeof(firebaseRemoteConfig_obj),			/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseMLKit_dealloc,			/* tp_dealloc */
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
	(reprfunc)firebaseMLKit_str,				/* tp_str */
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
	firebaseMLKit_methods,						/* tp_methods */
	0,											/* tp_members */
	firebaseMLKit_getsets,						/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseMLKit_new,							/* tp_new */
	0,											/* tp_free */
};
