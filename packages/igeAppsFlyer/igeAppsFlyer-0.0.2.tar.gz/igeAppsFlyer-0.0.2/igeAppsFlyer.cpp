#include "igeAppsFlyer.h"
#include "igeAppsFlyer_doc_en.h"
#include <map>
#include <string>


PyObject* appsFlyer_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	appsFlyer_obj* self = NULL;

	self = (appsFlyer_obj*)type->tp_alloc(type, 0);
	self->appsFlyer = new AppsFlyer();

	return (PyObject*)self;
}

void appsFlyer_dealloc(appsFlyer_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* appsFlyer_str(appsFlyer_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "appsFlyer object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* appsFlyer_Init(appsFlyer_obj* self)
{
	self->appsFlyer->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* appsFlyer_Release(appsFlyer_obj* self)
{
	self->appsFlyer->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* appsFlyer_LogEvent(appsFlyer_obj* self, PyObject* args)
{
	char* eventName;
	PyObject* parameters = nullptr;

	if (!PyArg_ParseTuple(args, "sO", &eventName, &parameters)) return NULL;

	std::map<std::string, std::string> analyticParameters;
	if (parameters && PyTuple_Check(parameters))
	{
		uint32_t numAttr = 0;
		numAttr = (uint32_t)PyTuple_Size(parameters);

		for (uint32_t i = 0; i < numAttr; i++)
		{
			PyObject* v = PyTuple_GET_ITEM(parameters, i);
			if (PyTuple_Check(v))
			{
				int n = (int)PyTuple_Size(v);
				if (n != 2) { numAttr = 0; break; }

				PyObject* nameObject = PyTuple_GET_ITEM(v, 0);
				const char* parameter_name = PyUnicode_AsUTF8(nameObject);

				PyObject* valueObject = PyTuple_GET_ITEM(v, 1);

				if (PyLong_Check(valueObject))
				{
					int value = PyLong_AsLong(valueObject);
					std::string _value = std::to_string(value);
					analyticParameters.insert({ parameter_name, _value.c_str() });
				}
				else if (PyFloat_Check(valueObject))
				{
					double value = PyFloat_AsDouble(valueObject);
					std::string _value = std::to_string(value);
					analyticParameters.insert({ parameter_name, _value.c_str() });
				}
				else
				{
					const char* parameter_value = PyUnicode_AsUTF8(valueObject);
					analyticParameters.insert({ parameter_name, parameter_value });
				}				
			}
		}		
	}

	self->appsFlyer->logEvent(eventName, analyticParameters);
	analyticParameters.clear();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef appsFlyer_methods[] = {
	{ "init", (PyCFunction)appsFlyer_Init, METH_NOARGS, appsflyerInit_doc },
	{ "release", (PyCFunction)appsFlyer_Release, METH_NOARGS, appsflyerRelease_doc },
	{ "logEvent", (PyCFunction)appsFlyer_LogEvent, METH_VARARGS, appsflyerLogEvent_doc },
	{ NULL,	NULL }
};

PyGetSetDef appsFlyer_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject AppsFlyerType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeAppsFlyer",								/* tp_name */
	sizeof(appsFlyer_obj),						/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)appsFlyer_dealloc,				/* tp_dealloc */
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
	(reprfunc)appsFlyer_str,					/* tp_str */
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
	appsFlyer_methods,							/* tp_methods */
	0,											/* tp_members */
	appsFlyer_getsets,							/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	appsFlyer_new,								/* tp_new */
	0,											/* tp_free */
};

static PyModuleDef appsFlyer_module = {
	PyModuleDef_HEAD_INIT,
	"igeAppsFlyer",						// Module name to use with Python import statements
	"AppsFlyer Module.",					// Module description
	0,
	appsFlyer_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeAppsFlyer() {
	PyObject* module = PyModule_Create(&appsFlyer_module);

	if (PyType_Ready(&AppsFlyerType) < 0) return NULL;

	return module;
}