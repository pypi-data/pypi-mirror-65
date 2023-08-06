#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE void __Pyx_crop_slice(Py_ssize_t* _start, Py_ssize_t* _stop, Py_ssize_t* _length) {
    Py_ssize_t start = *_start, stop = *_stop, length = *_length;
    if (start < 0) {
        start += length;
        if (start < 0)
            start = 0;
    }
    if (stop < 0)
        stop += length;
    else if (stop > length)
        stop = length;
    *_length = stop - start;
    *_start = start;
    *_stop = stop;
}
static CYTHON_INLINE void __Pyx_copy_object_array(PyObject** CYTHON_RESTRICT src, PyObject** CYTHON_RESTRICT dest, Py_ssize_t length) {
    PyObject *v;
    Py_ssize_t i;
    for (i = 0; i < length; i++) {
        v = dest[i] = src[i];
        Py_INCREF(v);
    }
}
static CYTHON_INLINE PyObject* __Pyx_PyList_GetSlice(
            PyObject* src, Py_ssize_t start, Py_ssize_t stop) {
    PyObject* dest;
    Py_ssize_t length = PyList_GET_SIZE(src);
    __Pyx_crop_slice(&start, &stop, &length);
    if (unlikely(length <= 0))
        return PyList_New(0);
    dest = PyList_New(length);
    if (unlikely(!dest))
        return NULL;
    __Pyx_copy_object_array(
        ((PyListObject*)src)->ob_item + start,
        ((PyListObject*)dest)->ob_item,
        length);
    return dest;
}
static CYTHON_INLINE PyObject* __Pyx_PyTuple_GetSlice(
            PyObject* src, Py_ssize_t start, Py_ssize_t stop) {
    PyObject* dest;
    Py_ssize_t length = PyTuple_GET_SIZE(src);
    __Pyx_crop_slice(&start, &stop, &length);
    if (unlikely(length <= 0))
        return PyTuple_New(0);
    dest = PyTuple_New(length);
    if (unlikely(!dest))
        return NULL;
    __Pyx_copy_object_array(
        ((PyTupleObject*)src)->ob_item + start,
        ((PyTupleObject*)dest)->ob_item,
        length);
    return dest;
}
#endif

