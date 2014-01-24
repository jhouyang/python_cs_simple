#include <Python.h>

int main()
{
    Py_Initialize();
    PyImport_ImportModule("server");
    return 0;
}
