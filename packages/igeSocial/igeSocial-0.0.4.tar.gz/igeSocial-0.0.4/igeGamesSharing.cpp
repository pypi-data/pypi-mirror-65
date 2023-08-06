#include "igeSocial.h"
#include "igeSocial_doc_en.h"

PyObject* gamesSharing_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	gamesSharing_obj* self = NULL;

	self = (gamesSharing_obj*)type->tp_alloc(type, 0);
	self->gamesSharing = new GamesSharing();

	return (PyObject*)self;
}

void gamesSharing_dealloc(gamesSharing_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* gamesSharing_str(gamesSharing_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "Social GamesSharing object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* gamesSharing_Init(gamesSharing_obj* self, PyObject* args)
{
    int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	self->gamesSharing->init((SnsType)snsType);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesSharing_Release(gamesSharing_obj* self, PyObject* args)
{
    int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	self->gamesSharing->release((SnsType)snsType);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesSharing_SignIn(gamesSharing_obj* self, PyObject* args)
{
	int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	self->gamesSharing->signIn((SnsType)snsType);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesSharing_SignOut(gamesSharing_obj* self, PyObject* args)
{
	int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	self->gamesSharing->signOut((SnsType)snsType);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesSharing_IsSignedIn(gamesSharing_obj* self, PyObject* args)
{
	int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	return PyLong_FromLong(self->gamesSharing->isSignedIn((SnsType)snsType));
}

static PyObject* gamesSharing_Share(gamesSharing_obj* self, PyObject* args)
{
	int snsType = 0;
	int shareType = 0;
	const char* value = "";
	if (!PyArg_ParseTuple(args, "s|ii", &value, &snsType, &shareType))
		return NULL;
	self->gamesSharing->share((SnsType)snsType, (ShareType)shareType, value);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* gamesSharing_GetProfileID(gamesSharing_obj* self, PyObject* args)
{
	int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	const char* token = self->gamesSharing->getProfileID((SnsType)snsType);
	PyObject* obj = PyBytes_FromString(token);

	return obj;
}

static PyObject* gamesSharing_GetProfileName(gamesSharing_obj* self, PyObject* args)
{
	int snsType = 0;
	if (!PyArg_ParseTuple(args, "|i", &snsType))
		return NULL;
	const char* token = self->gamesSharing->getProfileName((SnsType)snsType);
	PyObject* obj = PyBytes_FromString(token);

	return obj;
}

static PyObject* gamesSharing_Available(gamesSharing_obj* self, PyObject* args)
{
    int snsType = 0;
    if (!PyArg_ParseTuple(args, "|i", &snsType))
        return NULL;
    return PyBool_FromLong(self->gamesSharing->available((SnsType)snsType));
}

PyMethodDef gamesSharing_methods[] = {
	{ "init", (PyCFunction)gamesSharing_Init, METH_VARARGS, socialGamesSharingInit_doc },
	{ "release", (PyCFunction)gamesSharing_Release, METH_VARARGS, socialGamesSharingRelease_doc },
	{ "signIn", (PyCFunction)gamesSharing_SignIn, METH_VARARGS, socialGamesSharingSignIn_doc },
	{ "signOut", (PyCFunction)gamesSharing_SignOut, METH_VARARGS, socialGamesSharingSignOut_doc },
	{ "isSignedIn", (PyCFunction)gamesSharing_IsSignedIn, METH_VARARGS, socialGamesSharingIsSignedIn_doc },
	{ "share", (PyCFunction)gamesSharing_Share, METH_VARARGS, socialGamesSharingShare_doc },
	{ "getProfileID", (PyCFunction)gamesSharing_GetProfileID, METH_VARARGS, socialGamesSharingGetProfileID_doc },
	{ "getProfileName", (PyCFunction)gamesSharing_GetProfileName, METH_VARARGS, socialGamesSharingGetProfileName_doc },
    { "available", (PyCFunction)gamesSharing_Available, METH_VARARGS, socialGamesSharingAvailable_doc },
	{ NULL,	NULL }
};

PyGetSetDef gamesSharing_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject GamesSharingType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeSocial.gamesSharing",						/* tp_name */
	sizeof(gamesSharing_obj),						/* tp_basicsize */
	0,												/* tp_itemsize */
	(destructor)gamesSharing_dealloc,				/* tp_dealloc */
	0,												/* tp_print */
	0,												/* tp_getattr */
	0,												/* tp_setattr */
	0,												/* tp_reserved */
	0,												/* tp_repr */
	0,												/* tp_as_number */
	0,												/* tp_as_sequence */
	0,												/* tp_as_mapping */
	0,												/* tp_hash */
	0,												/* tp_call */
	(reprfunc)gamesSharing_str,						/* tp_str */
	0,												/* tp_getattro */
	0,												/* tp_setattro */
	0,												/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,								/* tp_flags */
	0,												/* tp_doc */
	0,												/* tp_traverse */
	0,												/* tp_clear */
	0,												/* tp_richcompare */
	0,												/* tp_weaklistoffset */
	0,												/* tp_iter */
	0,												/* tp_iternext */
	gamesSharing_methods,							/* tp_methods */
	0,												/* tp_members */
	gamesSharing_getsets,							/* tp_getset */
	0,												/* tp_base */
	0,												/* tp_dict */
	0,												/* tp_descr_get */
	0,												/* tp_descr_set */
	0,												/* tp_dictoffset */
	0,												/* tp_init */
	0,												/* tp_alloc */
	gamesSharing_new,								/* tp_new */
	0,												/* tp_free */
};
