#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"


PyObject* firebaseAuth_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseAuth_obj* self = NULL;

	self = (firebaseAuth_obj*)type->tp_alloc(type, 0);
	self->firebaseAuth = new FirebaseAuth();

	return (PyObject*)self;
}

void firebaseAuth_dealloc(firebaseAuth_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseAuth_str(firebaseAuth_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase auth object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseAuth_Init(firebaseAuth_obj* self)
{
	self->firebaseAuth->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAuth_Release(firebaseAuth_obj* self)
{
	self->firebaseAuth->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAuth_Testcase(firebaseAuth_obj* self)
{
	self->firebaseAuth->testcase();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAuth_SignInWithEmailAndPassword(firebaseAuth_obj* self, PyObject* args)
{
	char* username = nullptr;
	char* password = nullptr;

	if(!PyArg_ParseTuple(args, "ss", &username, &password)) return NULL;

	return PyLong_FromLong(self->firebaseAuth->signInWithEmailAndPassword(username, password));
}

static PyObject* firebaseAuth_SignOut(firebaseAuth_obj* self)
{
	return PyLong_FromLong(self->firebaseAuth->signOut());
}

static PyObject* firebaseAuth_IsPlayerAuthenticated(firebaseAuth_obj* self)
{
	return PyLong_FromLong(self->firebaseAuth->isPlayerAuthenticated());
}

static PyObject* firebaseAuth_RegisterWithEmailAndPassword(firebaseAuth_obj* self, PyObject* args)
{
	char* username = nullptr;
	char* password = nullptr;

	if (!PyArg_ParseTuple(args, "ss", &username, &password)) return NULL;

	return PyLong_FromLong(self->firebaseAuth->registerWithEmailAndPassword(username, password));
}


PyMethodDef firebaseAuth_methods[] = {
	{ "init", (PyCFunction)firebaseAuth_Init, METH_NOARGS, firebaseAuthInit_doc },
	{ "release", (PyCFunction)firebaseAuth_Release, METH_NOARGS, firebaseAuthRelease_doc },
	{ "testcase", (PyCFunction)firebaseAuth_Testcase, METH_NOARGS, firebaseAuthTestcase_doc },
	{ "signInWithEmailAndPassword", (PyCFunction)firebaseAuth_SignInWithEmailAndPassword, METH_VARARGS, firebaseAuthSignInWithEmailAndPassword_doc },
	{ "registerWithEmailAndPassword", (PyCFunction)firebaseAuth_RegisterWithEmailAndPassword, METH_VARARGS, firebaseAuthRegisterWithEmailAndPassword_doc },
	{ "signOut", (PyCFunction)firebaseAuth_SignOut, METH_NOARGS, firebaseAuthSignOut_doc },
	{ "isPlayerAuthenticated", (PyCFunction)firebaseAuth_IsPlayerAuthenticated, METH_NOARGS, firebaseAuthIsPlayerAuthenticated_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseAuth_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseAuthType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeFirebase.auth",							/* tp_name */
	sizeof(firebaseAuth_obj),				/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseAuth_dealloc,			/* tp_dealloc */
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
	(reprfunc)firebaseAuth_str,					/* tp_str */
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
	firebaseAuth_methods,						/* tp_methods */
	0,											/* tp_members */
	firebaseAuth_getsets,						/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseAuth_new,							/* tp_new */
	0,											/* tp_free */
};