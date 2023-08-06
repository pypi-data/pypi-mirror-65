#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdbool.h>

/* ===================================================== */

bool y_inside_minibox(double* mini_pq, double* y, Py_ssize_t d) {
    double y_i = 0.0;
    for (Py_ssize_t i = 0; i < d; ++i) {
        y_i = y[i];
        if (y_i <= mini_pq[2*i] || y_i >= mini_pq[2*i+1]) {
            return false;
        }
    }
    return true;
}

/* ----------------------------------------------------- */

PyDoc_STRVAR(edges_doc,
    "persty.minibox.edges(points)\n\
    \n\
    Return Minibox edges on d-dimensional points.\n\
    \n\
    Find the Minibox edges iterating on all possible\n\
    pairs of indices in `points`.\n\
    \n\
    Parameters\n\
    \----------\n\
    points: list of `n` lists\n\
    \tThe list of d-dimensional points.\n\
    \n\
    Return\n\
    \-------\n\
    minibox_edges: list of pairs of integers\n\
    \tThe indices of elements in `points` forming a\n\
    \tMinibox edge.\n");

static PyObject*
edges(PyObject* self, PyObject* args) {
    /* Parse arguments */
    PyObject* points_py = NULL;
    PyObject* first_point_py = NULL;
    Py_ssize_t n = 0;
    Py_ssize_t d = 0;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &points_py)) {
        PyErr_SetString(PyExc_TypeError, "Argument passed needs to be a list");
        return NULL;
    }

    n = PyList_Size(points_py);
    first_point_py = PyList_GetItem(points_py, 0);
    if(!PyList_Check(first_point_py)) {
        PyErr_SetString(PyExc_TypeError, "List items must be lists.");
        return NULL;
    }
    d = PyList_Size(first_point_py);

    /* Read points into dynamically allocated array */
    double* array_points = calloc(n*d, sizeof(double));
    if (!array_points) {
        return PyErr_NoMemory();
    }
    PyObject* tmp_py = NULL;
    PyObject* coord_py = NULL;
    Py_ssize_t tmp_d = 0;
    double coord_i = 0;
    for (Py_ssize_t index = 0; index < n; ++index) {
        tmp_py = PyList_GetItem(points_py, index);
        tmp_d = PyList_Size(tmp_py);
        if(!PyList_Check(tmp_py)) {
            PyErr_SetString(PyExc_TypeError, "List items must be lists.");
            free(array_points);
            return NULL;
        }
        if(tmp_d != d) {
            PyErr_SetString(PyExc_TypeError, "Sublist must contain d elements.");
            free(array_points);
            return NULL;
        }
        for (Py_ssize_t i = 0; i < d; ++i) {
            coord_py = PyList_GetItem(tmp_py, i);
            if (!coord_py) {
                free(array_points);
                return NULL;
            }
            coord_i = PyFloat_AsDouble(coord_py);
            if (PyErr_Occurred()) {
                printf("could not convert coord_py to coord_i\n");
                free(array_points);
                return NULL;
            }
            array_points[index*d+i] = coord_i;
        }
    }

    /* Search Minibox edges */
    PyObject* edges_py = PyList_New(0);
    PyObject* e_py = NULL;

    double* mini_pq = calloc(2*d, sizeof(double));
    if (!mini_pq) {
        free(array_points);
        return NULL;
    }
    double* p = NULL;
    double p_i = 0.0;
    double* q = NULL;
    double q_i = 0.0;
    double* y = NULL;
    bool add_edge = true;
    int append_ok = 0;
    for (Py_ssize_t p_ind = 0; p_ind < n; ++p_ind) {
        for (Py_ssize_t q_ind = p_ind+1; q_ind < n; ++q_ind) {
            e_py = PyTuple_New(2);
            if (!e_py) {
                printf("could not create PyTuple_New(2)\n");
                free(mini_pq);
                free(array_points);
                return NULL;
            }
            if (PyTuple_SetItem(e_py, 0, PyLong_FromSsize_t(p_ind)) != 0 ||
                PyTuple_SetItem(e_py, 1, PyLong_FromSsize_t(q_ind)) != 0) {
                free(mini_pq);
                free(array_points);
                return NULL;
            }

            /* init p and q */
            p = (array_points + p_ind*d);
            q = (array_points + q_ind*d);

            /* init mini_pq */
            for (Py_ssize_t i = 0; i < d; ++i) {
                p_i = p[i];
                q_i = q[i];
                if (p_i <= q_i) {
                    mini_pq[2*i]   = p_i;
                    mini_pq[2*i+1] = q_i;
                } else {
                    mini_pq[2*i]   = q_i;
                    mini_pq[2*i+1] = p_i;
                }
            }

            add_edge = true;
            for (Py_ssize_t y_ind = 0; y_ind < n; ++y_ind) {
                if (y_ind == p_ind || y_ind == q_ind) {
                    continue;
                }
                y = (array_points + y_ind*d);
                if(y_inside_minibox(mini_pq, y, d)) {
                    add_edge = false;
                    break;
                }
            }
            if (add_edge) {
                append_ok = PyList_Append(edges_py, e_py);
                if (append_ok != 0) {
                    free(mini_pq);
                    free(array_points);
                    return NULL;
                }
                Py_DECREF(e_py);
            }
        }
    }

    free(array_points);
    free(mini_pq);
    return edges_py;
}

/* ===================================================== */

PyMethodDef method_table[] = {
    {"edges", (PyCFunction) edges, METH_VARARGS, edges_doc},
	{NULL, NULL, 0, NULL}
};

/* ===================================================== */

PyDoc_STRVAR(module_doc,
"Module for computing minibox edges.");

PyModuleDef minibox_module = {
			      PyModuleDef_HEAD_INIT,
			      "minibox",
			      module_doc,
			      -1,
			      method_table,
			      NULL, NULL,
			      NULL, NULL
};

/* ===================================================== */

PyMODINIT_FUNC
PyInit_minibox(void)
{
  return PyModule_Create(&minibox_module);
}
