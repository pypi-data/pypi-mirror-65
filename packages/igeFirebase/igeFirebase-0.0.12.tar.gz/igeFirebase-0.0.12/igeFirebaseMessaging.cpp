#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"


PyObject* firebaseMessaging_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseMessaging_obj* self = NULL;

	self = (firebaseMessaging_obj*)type->tp_alloc(type, 0);
	self->firebaseMessaging = new FirebaseMessaging();

	return (PyObject*)self;
}

void firebaseMessaging_dealloc(firebaseMessaging_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseMessaging_str(firebaseMessaging_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase messaging object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseMessaging_Init(firebaseMessaging_obj* self)
{
	self->firebaseMessaging->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseMessaging_Release(firebaseMessaging_obj* self)
{
	self->firebaseMessaging->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseMessaging_GetRegistrationToken(firebaseMessaging_obj* self)
{
	const char* token = self->firebaseMessaging->getRegistrationToken();
	PyObject* obj = PyBytes_FromString(token);

	return obj;
}

PyMethodDef firebaseMessaging_methods[] = {
	{ "init", (PyCFunction)firebaseMessaging_Init, METH_NOARGS, firebaseMessagingInit_doc },
	{ "release", (PyCFunction)firebaseMessaging_Release, METH_NOARGS, firebaseMessagingRelease_doc },
	{ "getRegistrationToken", (PyCFunction)firebaseMessaging_GetRegistrationToken, METH_NOARGS, firebaseMessagingGetRegistrationToken_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseMessaging_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseMessagingType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeFirebase.messaging",					/* tp_name */
	sizeof(firebaseMessaging_obj),				/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseMessaging_dealloc,		/* tp_dealloc */
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
	(reprfunc)firebaseMessaging_str,			/* tp_str */
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
	firebaseMessaging_methods,					/* tp_methods */
	0,											/* tp_members */
	firebaseMessaging_getsets,					/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseMessaging_new,						/* tp_new */
	0,											/* tp_free */
};