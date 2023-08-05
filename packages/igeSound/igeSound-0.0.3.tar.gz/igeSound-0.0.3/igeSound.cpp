#include "igeSound.h"
#include "igeSound_doc_en.h"


PyObject* igeSound_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	igeSound_obj* self = NULL;

	self = (igeSound_obj*)type->tp_alloc(type, 0);
	self->sound = Sound::Instance();

	return (PyObject*)self;
}

void igeSound_dealloc(igeSound_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* igeSound_str(igeSound_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "igeSound object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* igeSound_Init(igeSound_obj* self)
{
	self->sound->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Release(igeSound_obj* self)
{
	self->sound->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Play(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	int stream = 0;
	int loop = 0;
	if (!PyArg_ParseTuple(args, "s|ii", &soundName, &stream, &loop))
		return NULL;

	self->sound->play(soundName, stream, loop);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Stop(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	if (!PyArg_ParseTuple(args, "s", &soundName))
		return NULL;

	self->sound->stop(soundName);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_StopAll(igeSound_obj* self)
{
	self->sound->stopAllSound();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Load(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	int stream = 0;
	if (!PyArg_ParseTuple(args, "s|i", &soundName, &stream))
		return NULL;

	self->sound->load(soundName, stream);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Unload(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	if (!PyArg_ParseTuple(args, "s", &soundName))
		return NULL;

	self->sound->unload(soundName);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_UnloadUnused(igeSound_obj* self)
{
	self->sound->unloadUnused();

	Py_INCREF(Py_None);
	return Py_None;
}	

static PyObject* igeSound_SetPositon(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "sfff", &soundName, &x, &y, &z))
		return NULL;

	self->sound->setPositon(soundName, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_SetPitch(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	float pitch;
	if (!PyArg_ParseTuple(args, "sf", &soundName, &pitch))
		return NULL;

	self->sound->setPitch(soundName, pitch);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_SetGain(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	float gain;
	if (!PyArg_ParseTuple(args, "sf", &soundName, &gain))
		return NULL;

	self->sound->setGain(soundName, gain);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_SetRolloff(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	float rolloff;
	if (!PyArg_ParseTuple(args, "sf", &soundName, &rolloff))
		return NULL;

	self->sound->setRolloff(soundName, rolloff);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_SetListenerPosition(igeSound_obj* self, PyObject* args)
{
	float x, y, z;
	if (!PyArg_ParseTuple(args, "fff", &x, &y, &z))
		return NULL;

	//self->sound->setListenerPosition(x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_SetListenerOrientation(igeSound_obj* self, PyObject* args)
{
	float xAt, yAt, zAt, xUp, yUp, zUp;
	if (!PyArg_ParseTuple(args, "ffffff", &xAt, &yAt, &zAt, &xUp, &yUp, &zUp))
		return NULL;

	//self->sound->setListenerOrientation(xAt, yAt, zAt, xUp, yUp, zUp);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef igeSound_methods[] = {
	{ "init", (PyCFunction)igeSound_Init, METH_NOARGS, soundInit_doc },
	{ "release", (PyCFunction)igeSound_Release, METH_NOARGS, soundRelease_doc },
	{ "play", (PyCFunction)igeSound_Play, METH_VARARGS, soundPlay_doc },
	{ "stop", (PyCFunction)igeSound_Stop, METH_VARARGS, soundStop_doc },
	{ "stopAll", (PyCFunction)igeSound_StopAll, METH_NOARGS, soundStopAll_doc },
	{ "load", (PyCFunction)igeSound_Load, METH_VARARGS, soundLoad_doc },
	{ "unload", (PyCFunction)igeSound_Unload, METH_VARARGS, soundUnload_doc },
	{ "unloadUnused", (PyCFunction)igeSound_UnloadUnused, METH_NOARGS, soundUnloadUnused_doc },
	{ "setPositon", (PyCFunction)igeSound_SetPositon, METH_VARARGS, soundSetPositon_doc },
	{ "setPitch", (PyCFunction)igeSound_SetPitch, METH_VARARGS, soundSetPitch_doc },
	{ "setGain", (PyCFunction)igeSound_SetGain, METH_VARARGS, soundSetGain_doc },
	{ "setRolloff", (PyCFunction)igeSound_SetRolloff, METH_VARARGS, soundSetRolloff_doc },
	{ "setListenerPosition", (PyCFunction)igeSound_SetListenerPosition, METH_VARARGS, soundSetListenerPosition_doc },
	{ "setListenerOrientation", (PyCFunction)igeSound_SetListenerOrientation, METH_VARARGS, soundSetListenerOrientation_doc },
	{ NULL,	NULL }
};

PyGetSetDef igeSound_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject IgeSoundType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeSound.sound",					/* tp_name */
	sizeof(igeSound_obj),					/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)igeSound_dealloc,			/* tp_dealloc */
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
	(reprfunc)igeSound_str,				/* tp_str */
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
	igeSound_methods,						/* tp_methods */
	0,                                  /* tp_members */
	igeSound_getsets,						/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	igeSound_new,							/* tp_new */
	0,									/* tp_free */
};

static PyModuleDef igeSound_module = {
	PyModuleDef_HEAD_INIT,
	"igeSound.sound",							// Module name to use with Python import statements
	"IGE Sound Module.",						// Module description
	0,
	igeSound_methods								// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeSound() {
	PyObject* module = PyModule_Create(&igeSound_module);

	if (PyType_Ready(&IgeSoundType) < 0) return NULL;

	Py_INCREF(&IgeSoundType);
	PyModule_AddObject(module, "sound", (PyObject*)&IgeSoundType);

	return module;
}