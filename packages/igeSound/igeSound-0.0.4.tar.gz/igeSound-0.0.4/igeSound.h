#include <Python.h>
#include "Sound.h"

typedef struct {
	PyObject_HEAD
		Sound* sound;
} igeSound_obj;
