#pragma once
#include <Python.h>
#include <string>
#include <tuple>
#include <algorithm>
#include "utils.hpp"

inline std::wstring PyObject_To_Wstring(PyObject *object, bool preprocess = false) {
    Py_ssize_t len = PyUnicode_GET_LENGTH(object);
    wchar_t* buffer = PyUnicode_AsWideCharString(object, &len);
    std::wstring str(buffer, len);
    PyMem_Free(buffer);

    return (preprocess) ? utils::default_process(str) : str;
}
