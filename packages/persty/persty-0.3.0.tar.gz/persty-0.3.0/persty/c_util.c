#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include <math.h>

static PyObject*
get_A(PyObject* self, PyObject* args) {
    /* Parse arguments */
    PyObject* args_ptr;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &args_ptr)) {
        PyErr_SetString(PyExc_TypeError, "Need list of arguments as input");
        return NULL;
    }

    /* Type Checks */
    PyObject* p_ptr = PyList_GetItem(args_ptr, 0);
    if (!p_ptr) {
        return NULL;
    }
    if (!PyList_Check(p_ptr)) {
        PyErr_SetString(PyExc_TypeError, "First argument needs to be list.");
        return NULL;
    }

    PyObject* q_ptr = PyList_GetItem(args_ptr, 1);
    if (!q_ptr) {
        return NULL;
    }
    if (!PyList_Check(q_ptr)) {
        PyErr_SetString(PyExc_TypeError, "Second argument needs to be list.");
        return NULL;
    }

    PyObject* first_value_p = PyList_GetItem(p_ptr, 0);
    PyObject* first_value_q = PyList_GetItem(q_ptr, 0);
    if (! (PyFloat_Check(first_value_p) && PyFloat_Check(first_value_q)) ) {
        PyErr_SetString(PyExc_TypeError, "Elements of p and q must be floats");
        return NULL;
    }

    /* Max coordinate difference between p and q */
    Py_ssize_t d = PyList_Size(p_ptr);
    double p_0 = PyFloat_AsDouble(first_value_p);
    double q_0 = PyFloat_AsDouble(first_value_q);
    double delta = fabs(p_0 - q_0);
    double new_delta;
    Py_ssize_t coord_max_delta = 0;
    for (Py_ssize_t index = 0; index < d; ++index) {
        PyObject* p_i_ptr = PyList_GetItem(p_ptr, index);
        PyObject* q_i_ptr = PyList_GetItem(q_ptr, index);
        double p_i = PyFloat_AsDouble(p_i_ptr);
        double q_i = PyFloat_AsDouble(q_i_ptr);
        new_delta = fabs(p_i - q_i);
        if (new_delta > delta) {
            delta = new_delta;
            coord_max_delta = index;
        }
    }
    double radius = delta / 2.0;

    /* Create and return A as list of 2d float values */
    PyObject* A_ptr = PyList_New(2*d);
    PyObject* p_i_ptr;
    double p_i = 0.0;
    PyObject* q_i_ptr;
    double q_i = 0.0;
    PyObject* low_ptr;
    PyObject* high_ptr;
    PyObject* mean_p_q_ptr = NULL;
    for (Py_ssize_t i = 0; i < d; ++i) {
        p_i_ptr = PyList_GetItem(p_ptr, i);
        q_i_ptr = PyList_GetItem(q_ptr, i);
        p_i = PyFloat_AsDouble(p_i_ptr);
        q_i = PyFloat_AsDouble(q_i_ptr);

        if (i == coord_max_delta) {
            double mean_p_q = (p_i + q_i) / 2.0;
            mean_p_q_ptr = PyFloat_FromDouble(mean_p_q);
            PyList_SetItem(A_ptr, 2*i, mean_p_q_ptr);
            PyList_SetItem(A_ptr, 2*i+1, mean_p_q_ptr);
        } else {
            if  (p_i <= q_i) {
                low_ptr = PyFloat_FromDouble(q_i - radius);
                high_ptr = PyFloat_FromDouble(p_i + radius);
                PyList_SetItem(A_ptr, 2*i, low_ptr);
                PyList_SetItem(A_ptr, 2*i+1, high_ptr);
            } else {
                low_ptr = PyFloat_FromDouble(p_i - radius);
                high_ptr = PyFloat_FromDouble(q_i + radius);
                PyList_SetItem(A_ptr, 2*i, low_ptr);
                PyList_SetItem(A_ptr, 2*i+1, high_ptr);
            }
        }
    }
    return A_ptr;
}

bool ball_and_rect_intersect(PyObject* rect_ptr, PyObject* y_ptr, double radius) {
    Py_ssize_t d = PyList_Size(y_ptr);

    for (Py_ssize_t index = 0; index < d; ++index) {
        PyObject* y_i_ptr    = PyList_GetItem(y_ptr, index);
        PyObject* low_i_ptr  = PyList_GetItem(rect_ptr, 2*index);
        PyObject* high_i_ptr = PyList_GetItem(rect_ptr, 2*index+1);
        double y_i    = PyFloat_AsDouble(y_i_ptr);
        double low_i  = PyFloat_AsDouble(low_i_ptr);
        double high_i = PyFloat_AsDouble(high_i_ptr);
        /* if y_i is not within low_i-r and high_i+r --> no intersection */
        if (!((low_i - radius < y_i) && (y_i < high_i + radius))) {
            return false;
        }
    }
    return true;
}

bool update_rect_and_new_rect(PyObject* rect_ptr, double* new_rect,
                              Py_ssize_t index, double y_i, double radius) {
    Py_ssize_t d = PyList_Size(rect_ptr) / 2;
    PyObject* y_i_plus_r_ptr = PyFloat_FromDouble(y_i+radius);
    PyObject* y_i_minus_r_ptr = PyFloat_FromDouble(y_i-radius);
    PyObject* low_i_ptr = PyList_GetItem(rect_ptr, 2*index);
    PyObject* high_i_ptr = PyList_GetItem(rect_ptr, 2*index+1);
    double low_i  = PyFloat_AsDouble(low_i_ptr);
    double high_i = PyFloat_AsDouble(high_i_ptr);

    PyObject* low_i_new_ptr;
    PyObject* high_i_new_ptr;
    double low_i_new = 0.0;
    double high_i_new = 0.0;

    if (low_i < y_i + radius && y_i + radius < high_i) {
        /* if y_i+r is in [low_i, high_i] new_rect range is [y_i+r, high_i]*/
        for (Py_ssize_t index_new_rect = 0; index_new_rect < d; ++index_new_rect) {
            low_i_new_ptr = PyList_GetItem(rect_ptr, 2*index_new_rect);
            high_i_new_ptr = PyList_GetItem(rect_ptr, 2*index_new_rect+1);
            low_i_new  = PyFloat_AsDouble(low_i_new_ptr);
            high_i_new = PyFloat_AsDouble(high_i_new_ptr);
            if (index_new_rect == index) {
                PyList_SetItem(rect_ptr, 2*index_new_rect+1, y_i_plus_r_ptr);
                new_rect[2*index_new_rect]   = y_i + radius;
                new_rect[2*index_new_rect+1] = high_i_new;
            } else {
                new_rect[2*index_new_rect]   = low_i_new;
                new_rect[2*index_new_rect+1] = high_i_new;
            }
        }
        return true;
    } else if (low_i < y_i - radius && y_i - radius < high_i) {
        /* if y_i-r is in [low_i, high_i] new_rect range is [low_i, y_i-r]*/
        for (Py_ssize_t index_new_rect = 0; index_new_rect < d; ++index_new_rect) {
            low_i_new_ptr = PyList_GetItem(rect_ptr, 2*index_new_rect);
            high_i_new_ptr = PyList_GetItem(rect_ptr, 2*index_new_rect+1);
            low_i_new  = PyFloat_AsDouble(low_i_new_ptr);
            high_i_new = PyFloat_AsDouble(high_i_new_ptr);
            if (index_new_rect == index) {
                PyList_SetItem(rect_ptr, 2*index_new_rect, y_i_minus_r_ptr);
                new_rect[2*index_new_rect]   = low_i_new;
                new_rect[2*index_new_rect+1] = y_i - radius;
            } else {
                new_rect[2*index_new_rect]   = low_i_new;
                new_rect[2*index_new_rect+1] = high_i_new;
            }
        }
        return true;
    } else {
        /* [y_i-r, y_i+r] covers [low_i, high_i] */
        return false;
    }

}

static PyObject*
update_list_hyperrectangles(PyObject* self, PyObject* args) {
    /* Parse arguments */
    PyObject* args_ptr;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &args_ptr)) {
        PyErr_SetString(PyExc_TypeError, "Need list of arguments as input");
        return NULL;
    }

    PyObject* hyperrect_ptr = PyList_GetItem(args_ptr, 0);
    if (!PyList_Check(hyperrect_ptr)) {
        PyErr_SetString(PyExc_TypeError, "First argument needs to be list.");
        return NULL;
    }

    PyObject* y_ptr = PyList_GetItem(args_ptr, 1);
    if (!PyList_Check(hyperrect_ptr)) {
        PyErr_SetString(PyExc_TypeError, "Second argument needs to be list.");
        return NULL;
    }

    PyObject* y_0_ptr = PyList_GetItem(y_ptr, 0);
    if (!PyFloat_Check(y_0_ptr)) {
        PyErr_SetString(PyExc_TypeError, "Elements of point y must be floats.");
        return NULL;
    }

    PyObject* radius_ptr = PyList_GetItem(args_ptr, 2);
    double radius = PyFloat_AsDouble(radius_ptr);

    /* Update hyperrect_ptr */
    Py_ssize_t d = PyList_Size(y_ptr);
    PyObject* new_hyperrect_ptr = PyList_New(0);
    Py_ssize_t num_hyperrect = PyList_Size(hyperrect_ptr);

    PyObject* rect_ptr;
    PyObject* new_rect_ptr;
    double* new_rect = calloc(2*d, sizeof(double));
    bool append_new_rect = false;
    if (!new_rect) {
        return PyErr_NoMemory();
    }

    for (Py_ssize_t index_rect = 0; index_rect < num_hyperrect; ++index_rect) {
        rect_ptr = PyList_GetItem(hyperrect_ptr, index_rect);
        if (ball_and_rect_intersect(rect_ptr, y_ptr, radius)) {
            for (Py_ssize_t index = 0; index < d; ++index) {
                PyObject* y_i_ptr    = PyList_GetItem(y_ptr, index);
                PyObject* low_i_ptr  = PyList_GetItem(rect_ptr, 2*index);
                PyObject* high_i_ptr = PyList_GetItem(rect_ptr, 2*index+1);
                double y_i    = PyFloat_AsDouble(y_i_ptr);
                double low_i  = PyFloat_AsDouble(low_i_ptr);
                double high_i = PyFloat_AsDouble(high_i_ptr);
                append_new_rect = update_rect_and_new_rect(rect_ptr,
                                                           new_rect,
                                                           index,
                                                           y_i,
                                                           radius);
                if (append_new_rect) {
                    new_rect_ptr = PyList_New(2*d);
                    for (Py_ssize_t i = 0; i < d; ++i) {
                        PyObject* low  = PyFloat_FromDouble(new_rect[2*i]);
                        PyObject* high = PyFloat_FromDouble(new_rect[2*i+1]);

                        PyList_SetItem(new_rect_ptr, 2*i, low);
                        PyList_SetItem(new_rect_ptr, 2*i+1, high);
                    }
                    PyList_Append(new_hyperrect_ptr, new_rect_ptr);
                    Py_DECREF(new_rect_ptr);
                }

            }
        } else {
            PyList_Append(new_hyperrect_ptr, rect_ptr); // rect_ptr borrowed
        }
    }
    free(new_rect);
    return new_hyperrect_ptr;
}

// 2 TABLE OF METHODS TO EXPORT
PyMethodDef method_table[] = {
    {"get_A",
     (PyCFunction) get_A,
     METH_VARARGS,
     "Find A"
     "\n"
    },
    {"update_list_hyperrectangles",
     (PyCFunction) update_list_hyperrectangles,
     METH_VARARGS,
     "Find new list of hyperrectangles"
     "\n"
    },
	{NULL, NULL, 0, NULL} // end of table
};

// 3 STRUCT DEFINING MODULE
PyModuleDef c_util_module = {
			      PyModuleDef_HEAD_INIT,
			      "c_util",             // name of module
			      "C extension functions for Delaunay edges computations.",
			      -1,
			      method_table,
			      NULL, NULL,
			      NULL, NULL
};

// 4 INIT FUNC
PyMODINIT_FUNC PyInit_c_util(void)   // PyInit_<NAME_OF_MODULE>
{
  return PyModule_Create(&c_util_module);
}
