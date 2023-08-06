#include "igePAL.h"
#include "igePAL_doc_en.h"

static PyObject* onNotifyCallBack = nullptr;

PyObject* pal_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	pal_obj* self = NULL;

	self = (pal_obj*)type->tp_alloc(type, 0);
	self->pal = PAL::Instance();

	return (PyObject*)self;
}

void pal_dealloc(pal_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

void pal_ProcessNotifyEvent(NotifyCallback notify)
{
	PyObject* arglist;
	arglist = Py_BuildValue("(sss)", notify.name, notify.type, notify.id);
	PyObject* result = PyEval_CallObject(onNotifyCallBack, arglist);

	Py_DECREF(arglist);
	Py_XDECREF(result);
}

PyObject* pal_str(pal_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "PAL object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* pal_Init(pal_obj* self)
{
	PAL::Instance()->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* pal_Release(pal_obj* self)
{
	PAL::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}


PyObject* pal_RegisterNotifyEvent(pal_obj* self, PyObject* args)
{
	if (!PyArg_ParseTuple(args, "O", &onNotifyCallBack))
		return NULL;

	if (!PyCallable_Check(onNotifyCallBack)) {
		PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
		return NULL;
	}
	Py_XINCREF(onNotifyCallBack);

	PAL::Instance()->registerNotifyEvent(pal_ProcessNotifyEvent);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* pal_PollNotifyEvents(pal_obj* self, PyObject* args)
{	
	PyObject* list = PyList_New(0);
	std::vector<NotifyCallback> notifyEvents = PAL::Instance()->pollNotifyEvent();
	for (int i = 0; i < notifyEvents.size(); i++)
	{
		PyObject* obj = Py_BuildValue("{s:s,s:s,s:s}",
			"name", notifyEvents[i].name,
			"type", notifyEvents[i].type,
			"id", notifyEvents[i].id);

		PyList_Append(list, obj);
	}
	return list;
}



PyMethodDef pal_methods[] = {
	{ "init", (PyCFunction)pal_Init, METH_NOARGS, palInit_doc },
	{ "release", (PyCFunction)pal_Release, METH_NOARGS, palRelease_doc },
	{ "registerNotifyEvent", (PyCFunction)pal_RegisterNotifyEvent, METH_VARARGS, palRegisterNotifyEventListener_doc },
	{ "pollNotifyEvents", (PyCFunction)pal_PollNotifyEvents, METH_VARARGS, palPollNotifyEvents_doc },
	{ NULL,	NULL }
};

PyGetSetDef pal_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject PALType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igePAL",										/* tp_name */
	sizeof(pal_obj),								/* tp_basicsize */
	0,												/* tp_itemsize */
	(destructor)pal_dealloc,						/* tp_dealloc */
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
	(reprfunc)pal_str,								/* tp_str */
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
	pal_methods,									/* tp_methods */
	0,												/* tp_members */
	pal_getsets,									/* tp_getset */
	0,												/* tp_base */
	0,												/* tp_dict */
	0,												/* tp_descr_get */
	0,												/* tp_descr_set */
	0,												/* tp_dictoffset */
	0,												/* tp_init */
	0,												/* tp_alloc */
	pal_new,										/* tp_new */
	0,												/* tp_free */
};

static PyModuleDef pal_module = {
	PyModuleDef_HEAD_INIT,
	"igePAL",									// Module name to use with Python import statements
	"PAL Module",								// Module description
	0,
	pal_methods									// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igePAL() {
	PyObject* module = PyModule_Create(&pal_module);

	if (PyType_Ready(&PALType) < 0) return NULL;
	return module;
}
