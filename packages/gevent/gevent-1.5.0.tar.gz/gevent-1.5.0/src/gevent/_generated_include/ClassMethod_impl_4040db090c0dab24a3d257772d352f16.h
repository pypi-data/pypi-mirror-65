static PyObject* __Pyx_Method_ClassMethod(PyObject *method) {
#if CYTHON_COMPILING_IN_PYPY && PYPY_VERSION_NUM <= 0x05080000
    if (PyObject_TypeCheck(method, &PyWrapperDescr_Type)) {
        return PyClassMethod_New(method);
    }
#else
#if CYTHON_COMPILING_IN_PYSTON || CYTHON_COMPILING_IN_PYPY
    if (PyMethodDescr_Check(method))
#else
    static PyTypeObject *methoddescr_type = NULL;
    if (methoddescr_type == NULL) {
       PyObject *meth = PyObject_GetAttrString((PyObject*)&PyList_Type, "append");
       if (!meth) return NULL;
       methoddescr_type = Py_TYPE(meth);
       Py_DECREF(meth);
    }
    if (__Pyx_TypeCheck(method, methoddescr_type))
#endif
    {
        PyMethodDescrObject *descr = (PyMethodDescrObject *)method;
        #if PY_VERSION_HEX < 0x03020000
        PyTypeObject *d_type = descr->d_type;
        #else
        PyTypeObject *d_type = descr->d_common.d_type;
        #endif
        return PyDescr_NewClassMethod(d_type, descr->d_method);
    }
#endif
    else if (PyMethod_Check(method)) {
        return PyClassMethod_New(PyMethod_GET_FUNCTION(method));
    }
    else if (PyCFunction_Check(method)) {
        return PyClassMethod_New(method);
    }
#ifdef __Pyx_CyFunction_USED
    else if (__Pyx_CyFunction_Check(method)) {
        return PyClassMethod_New(method);
    }
#endif
    PyErr_SetString(PyExc_TypeError,
                   "Class-level classmethod() can only be called on "
                   "a method_descriptor or instance method.");
    return NULL;
}

