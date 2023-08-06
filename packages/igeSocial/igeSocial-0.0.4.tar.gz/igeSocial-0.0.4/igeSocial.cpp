#include "igeSocial.h"
#include "igeSocial_doc_en.h"

PyObject* social_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	social_obj* self = NULL;

	self = (social_obj*)type->tp_alloc(type, 0);
	self->social = new Social();

	return (PyObject*)self;
}

void social_dealloc(social_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* social_str(social_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "social object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}


static PyObject* social_Init(social_obj* self)
{
	self->social->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* social_Release(social_obj* self)
{
	self->social->release();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef social_methods[] = {
	{ "init", (PyCFunction)social_Init, METH_NOARGS, socialInit_doc },
	{ "release", (PyCFunction)social_Release, METH_NOARGS, socialRelease_doc },
	{ NULL,	NULL }
};

PyGetSetDef social_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject SocialType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeSocial",						/* tp_name */
	sizeof(social_obj),					/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)social_dealloc,			/* tp_dealloc */
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
	(reprfunc)social_str,				/* tp_str */
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
	social_methods,						/* tp_methods */
	0,                                  /* tp_members */
	social_getsets,						/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	social_new,							/* tp_new */
	0,									/* tp_free */
};

static PyModuleDef social_module = {
	PyModuleDef_HEAD_INIT,
	"igeSocial",						// Module name to use with Python import statements
	"Social Module.",					// Module description
	0,
	social_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeSocial() {
	PyObject* module = PyModule_Create(&social_module);

	if (PyType_Ready(&SocialType) < 0) return NULL;
	if (PyType_Ready(&GamesSharingType) < 0) return NULL;
	
	Py_INCREF(&GamesSharingType);
	PyModule_AddObject(module, "gamesSharing", (PyObject*)&GamesSharingType);

	return module;
}