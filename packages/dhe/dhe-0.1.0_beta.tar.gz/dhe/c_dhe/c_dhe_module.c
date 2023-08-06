#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include "c_dhe.h"

static int PyT_brine_parameters_Converter(PyObject* obj, void **address);
static int PyT_brine_stationary_parameters_Converter(PyObject* obj, void **address);
static _Bool fetch_array_data(const PyObject *item, double **out);
static _Bool dict_get_int(PyObject *dict, const char *key, int *out, const char *parent);
static _Bool dict_get_uint(PyObject *dict, const char *key, unsigned int *out, const char *parent);
static _Bool dict_get_double(PyObject *dict, const char *key, double *out, const char *parent);
static _Bool dict_get_array(PyObject *dict, const char *key, double **out, const char *parent);
typedef _Bool parser(PyObject*, void*);
static _Bool dict_get_struct(PyObject *dict, const char *key, const char *parent, parser *type, void *out);
static PyObject* dict_get_obj(PyObject *dict, const char *key, const char *parent);
static _Bool check(_Bool result, PyObject *err_type, const char* err_msg, ...);
static _Bool parse_struct_array(PyObject* obj, size_t struct_size,
				parser *parse_item,
				void **out_struct, unsigned int *out_n, const char *arr_name);
static _Bool PyDHE_parse(PyObject* obj, DHE* dhe);
static _Bool PyDHE_state_parse(PyObject* obj, DHE_state* state);
static _Bool check_dhe_states(PyObject *py_dhe_states, unsigned int *dim_rad, unsigned int *dim_ax);
static _Bool check_array_shape(PyArrayObject *arr, int ndim, npy_intp *dims, const char *name);

static PyObject *py_calc_P(PyObject *self, PyObject *args, PyObject *keywords)
{
  unsigned int i;
  PyArrayObject *py_P, *py_U_brine, *py_sum_Q0, *py_Q_wall;
  PyObject *py_out_T_sink, *py_out_T_source, *py_out_T_soil;
  PyObject *py_dhe, *py_dhe_states;
  PyObject *retval = NULL;
  DHE *dhe = NULL;
  DHE_state *dhe_states = NULL;
  unsigned int n_DHE = 0, n_DHE_states;
  unsigned int dim_rad, dim_ax;
  npy_intp n_boundary_refresh;
  double precision = 0.05;

  if(PyArg_ParseTupleAndKeywords(args, keywords,
				 "O!O!|$OOO!O!id:c_calc_P",
				 (char*[]){
				   "P",
				     "U_brine",
				     "dhe",
				     "dhe_states",
				     "sum_Q0",
				     "Q_wall",
				     "n_boundary_refresh",
				     "precision",
				     NULL},
				 &PyArray_Type, &py_P,
				 &PyArray_Type, &py_U_brine,
				 &py_dhe,
				 &py_dhe_states,
				 &PyArray_Type, &py_sum_Q0,
				 &PyArray_Type, &py_Q_wall,
				 &n_boundary_refresh,
				 &precision)
     // Validate arguments
     && check(PyArray_NDIM(py_P) == 1, PyExc_ValueError, "P must be 1-dimensional")
     && parse_struct_array(py_dhe, sizeof(DHE), (parser*)&PyDHE_parse, (void**)&dhe, &n_DHE, "dhe")
     && parse_struct_array(py_dhe_states, sizeof(DHE_state), (parser*)&PyDHE_state_parse, (void**)&dhe_states, &n_DHE_states, "dhe_states")
     && check(n_DHE == n_DHE_states, PyExc_ValueError,
	      "dhe and dhe_states must have same size")
     && check_dhe_states(py_dhe_states, &dim_rad, &dim_ax)
     && check_array_shape(py_sum_Q0, 1, (npy_intp[]){dim_ax}, "sum_Q0")
     )
    {
      npy_long dim_t = PyArray_DIMS(py_P)[0];
#define C_NDIM(arr) sizeof(arr)/sizeof(npy_intp)
      npy_intp dims_out_T[] = {n_DHE, dim_t};
      py_out_T_sink = PyArray_SimpleNew(C_NDIM(dims_out_T), dims_out_T, NPY_DOUBLE);
      py_out_T_source = PyArray_SimpleNew(C_NDIM(dims_out_T), dims_out_T, NPY_DOUBLE);
      npy_intp dims_out_T_soil[] = {n_DHE, dim_t, dim_rad + 2, dim_ax};
      py_out_T_soil = PyArray_SimpleNew(C_NDIM(dims_out_T_soil),
					dims_out_T_soil, NPY_DOUBLE);
#undef C_NDIM
      calc_P_output *out = malloc(n_DHE * sizeof(calc_P_output));
      for(i=0; i<n_DHE; i++)
	{
	  out[i].T_sink = (double*)PyArray_DATA((PyArrayObject*)py_out_T_sink) + i*dim_t;
	  out[i].T_source = (double*)PyArray_DATA((PyArrayObject*)py_out_T_source) + i*dim_t;
	  out[i].T_soil = (double*)PyArray_DATA((PyArrayObject*)py_out_T_soil) + i*dim_t*(dim_rad+2)*dim_ax;
	}
      calc_P(PyArray_DATA(py_P), PyArray_DATA(py_U_brine),
	     dim_ax, dim_rad,
	     dim_t,
	     n_DHE,
	     dhe,
	     dhe_states,
	     PyArray_DATA(py_sum_Q0),
	     PyArray_DATA(py_Q_wall),
	     n_boundary_refresh,
	     precision,
	     out);
      retval = PyTuple_Pack(3, py_out_T_sink, py_out_T_source, py_out_T_soil);
      Py_IncRef(retval);
      free(out);
    }
  if(dhe != NULL)
    {
      for(i=0; i<n_DHE; i++)
	{
	  free(dhe[i].pump_dependent_parameters[0].T_brine_parameters);
	  free(dhe[i].pump_dependent_parameters[1].T_brine_parameters);
	}
      free(dhe);
    }
  return retval;
}

static _Bool check(_Bool result, PyObject *err_type, const char* err_msg, ...)
{
  if(!result)
    {
      va_list ap;
      va_start(ap, err_msg);
      PyErr_FormatV(err_type, err_msg, ap);
      va_end(ap);
    }
  return result;
}
static _Bool check_array_shape(PyArrayObject *arr, int ndim, npy_intp *dims, const char *name)
{
  int i;
  if(!check(PyArray_NDIM(arr) == ndim, PyExc_ValueError,
	    "Shape mismatch: Found %s.ndim = %ld, required: %d", name, PyArray_NDIM(arr), ndim)) return false;
  for(i=0; i<ndim; i++)
    if(!check(PyArray_DIMS(arr)[i] == dims[i], PyExc_ValueError,
	      "Shape mismatch: Found %s.shape[%d] = %ld, required: %ld", name, i, PyArray_DIMS(arr)[i], dims[i]))
      return false;
  return true;
}


static int PyT_brine_parameters_Converter(PyObject* obj, void** address)
{
  int n_substeps;
  T_brine_parameters *prm;
  prm = malloc(sizeof(T_brine_parameters));
  if(!dict_get_int(obj, "n_sub_steps", &n_substeps, "T_soil_parameters_on|off")
     || !dict_get_double(obj, "kappa_ax", &prm->kappa_ax, "T_soil_parameters_on|off")
     || !dict_get_array(obj, "kappa_rad", &prm->kappa_rad, "T_soil_parameters_on|off")
     || !dict_get_array(obj, "lambda_brine", &prm->lambda_brine, "T_soil_parameters_on|off"))
    {
      free(prm);
      return false;
    }
  prm->n_sub_steps = n_substeps;
  *address = prm;
  return true;
}

static parser parse_soil_parameters;

static _Bool PyDHE_parse(PyObject* obj, DHE* dhe)
{
  return PyDict_Check(obj)
    && dict_get_double(obj, "L", &dhe->L, "dhe[i]")
    && dict_get_double(obj, "R", &dhe->R, "dhe[i]")
    && dict_get_double(obj, "x", &dhe->x, "dhe[i]")
    && dict_get_double(obj, "y", &dhe->y, "dhe[i]")
    && dict_get_array(obj, "g", &dhe->g, "dhe[i]")
    && dict_get_array(obj, "d_lambda_soil", &dhe->d_lambda_soil, "dhe[i]")
    && dict_get_struct(obj, "T_soil_parameters_off", "dhe[i]", parse_soil_parameters, &dhe->pump_dependent_parameters[0])
    && dict_get_struct(obj, "T_soil_parameters_on", "dhe[i]", parse_soil_parameters, &dhe->pump_dependent_parameters[1])
    && dict_get_double(obj, "L1_on", &dhe->L1_on, "dhe[i]")
    && dict_get_uint(obj, "n_steps", &dhe->n_steps, "dhe[i]");
}
static _Bool PyDHE_state_parse(PyObject* obj, DHE_state* state)
{
  return PyDict_Check(obj)
    && dict_get_array(obj, "Q", &state->Q, "dhe_state[i]")
    && dict_get_array(obj, "T_soil", &state->T_soil, "dhe_state[i]")
    && dict_get_array(obj, "T_U", &state->T_U, "dhe_state[i]");
}

static _Bool parse_struct_array(PyObject* obj, size_t struct_size,
				parser parse_item,
				void **out_struct, unsigned int *out_n, const char *arr_name)
{
  void *out = NULL;
  unsigned int n, i;
  if(!check(PyTuple_Check(obj), PyExc_TypeError, "%s: Not of type tuple", arr_name))
    return false;
  n = PyTuple_Size(obj);
  if(n > 0)
    {
      out = malloc(n * struct_size);
      for(i=0; i<n; i++)
	if(!(*parse_item)(PyTuple_GetItem(obj, i), out + i*struct_size))
	  {
	    free(out);
	    return false;
	  }
    }
  *out_struct = out;
  *out_n = n;
  return true;
}
static _Bool check_dhe_states(PyObject *py_dhe_states, unsigned int *dim_rad, unsigned int *dim_ax)
{
  unsigned int n, i, shape[2] = {2, 0};
  PyObject *obj;
  PyArrayObject* T_soil;
  if(!check(PyTuple_Check(py_dhe_states), PyExc_TypeError, "dhe_states: Not of type tuple"))
    return false;
  n = PyTuple_Size(py_dhe_states);
  for(i=0; i<n; i++)
    {
      obj = PyTuple_GetItem(py_dhe_states, i);
      if(!check(PyDict_Check(obj), PyExc_TypeError, "Not of type dict"))
	return false;
      T_soil = (PyArrayObject*)dict_get_obj(obj, "T_soil", "dhe_states[i]");
      if(!check(PyArray_Check(T_soil) && PyArray_NDIM(T_soil) == 2, PyExc_ValueError,
		"T_soil.ndim = 2 required. Found: %d", (int)PyArray_NDIM(T_soil))
	 || !check(PyArray_DIMS(T_soil)[0] >= 3, PyExc_ValueError,
		   "T_soil.shape[0] >= 3 required. Found: %d", PyArray_DIMS(T_soil)[0]))
	     return false;
      if(i == 0)
	{
	  shape[0] = PyArray_DIMS(T_soil)[0];
	  shape[1] = PyArray_DIMS(T_soil)[1];
	}
      else if(!check(shape[0] == PyArray_DIMS(T_soil)[0], PyExc_ValueError,
		     "Shape mismatch: dhe_states[%d].T_soil.shape[0] = %d, dhe_states[0].T_soil.shape[0] = %d", i, (int)PyArray_DIMS(T_soil)[0], shape[0])
	      || !check(shape[1] == PyArray_DIMS(T_soil)[1], PyExc_ValueError,
			"Shape mismatch: dhe_states[%d].T_soil.shape[1] = %d, dhe_states[0].T_soil.shape[1] = %d", i, (int)PyArray_DIMS(T_soil)[1], shape[1]))
	return false;
    }
  *dim_rad = shape[0] - 2;
  *dim_ax = shape[1];
  return true;
}

static int PyT_brine_stationary_parameters_Converter(PyObject* obj, void **address)
{
  T_brine_stationary_parameters *prm;
  prm = malloc(sizeof(T_brine_stationary_parameters));
  if(!dict_get_array(obj, "kappa_brine", &prm->kappa_brine, "T_soil_parameters_on|off")
     || !dict_get_array(obj, "kappa_soil", &prm->kappa_soil, "T_soil_parameters_on|off")
     || !dict_get_array(obj, "L", &prm->L, "T_soil_parameters_on|off"))
    {
      free(prm);
      return false;
    }
  *address = prm;
  return true;
}

typedef struct {T_brine_refresh_fun f; const char *name; int (*converter)(PyObject*, void**);} named_T_brine_f;
static const named_T_brine_f T_brine_functions[] = {
  {
    .f=(T_brine_refresh_fun)T_brine,
    .name="C_DHE_T_BRINE_DYNAMIC",
    .converter=PyT_brine_parameters_Converter
  },
  {
    .f=(T_brine_refresh_fun)T_brine_stationary,
    .name="C_DHE_T_BRINE_STATIONARY",
    .converter = PyT_brine_stationary_parameters_Converter
  } };

#define N_named_T_brine_f (sizeof(T_brine_functions) / sizeof(named_T_brine_f))

static _Bool parse_soil_parameters(PyObject* obj, void* void_address)
{
  T_soil_parameters *address = (T_soil_parameters *)void_address;
  PyObject *item;
  int n;
  if(!dict_get_array(obj, "T_soil_tensor", &address->T_soil_tensor, "T_soil_parameters_[on|off]")
     || !dict_get_array(obj, "L", &address->L, "T_soil_parameters_[on|off]")
     || !dict_get_int(obj, "T_brine_refresh", &n, "T_soil_parameters_[on|off]"))
    return false;
  if(n < 0 || (unsigned long)n >= N_named_T_brine_f)
    {
      PyErr_SetString(PyExc_ValueError, "T_brine_refresh not supported!");
      return false;
    }
  address->T_brine_refresh = T_brine_functions[n].f;

  item = dict_get_obj(obj, "T_brine_parameters", "T_soil_parameters_[on|off]");
  if(item == NULL || !T_brine_functions[n].converter(item, &address->T_brine_parameters))
    return false;
  return true;
}

static PyObject* dict_get_obj(PyObject *dict, const char *key, const char *parent)
{
  PyObject *item;
  item = PyDict_GetItemString(dict, key);
  if(item == NULL)
    PyErr_Format(PyExc_KeyError, "%s[\"%s\"]", parent, key);
  return item;
}
static _Bool dict_get_struct(PyObject *dict, const char *key, const char *parent, parser type, void *out)
{
  PyObject *item = dict_get_obj(dict, key, parent);
  if(item == NULL) return false;
  return type(item, out);
}

static _Bool dict_get_int(PyObject *dict, const char *key, int *out, const char *parent)
{
  PyObject *item = dict_get_obj(dict, key, parent);
  if(item == NULL) return false;
  if(!PyLong_Check(item))
    {
      PyErr_Format(PyExc_TypeError, "%s: Not of type int", key);
      return false;
    }
  *out = PyLong_AsLong(item);
  return true;
}
static _Bool dict_get_uint(PyObject *dict, const char *key, unsigned int *out, const char *parent)
{
  PyObject *item = dict_get_obj(dict, key, parent);
  if(item == NULL) return false;
  if(!PyLong_Check(item))
    {
      PyErr_Format(PyExc_TypeError, "%s: Not of type int", key);
      return false;
    }
  *out = (unsigned int)PyLong_AsLong(item);
  return true;
}
static _Bool dict_get_double(PyObject *dict, const char *key, double *out, const char *parent)
{
  PyObject *item = dict_get_obj(dict, key, parent);
  if(item == NULL) return false;
  if(!PyFloat_Check(item))
    {
      PyErr_Format(PyExc_TypeError, "%s: Not of type float", key);
      return false;
    }
  *out = PyFloat_AsDouble(item);
  return true;
}
static _Bool dict_get_array(PyObject *dict, const char *key, double **out, const char *parent)
{
  PyObject *item = dict_get_obj(dict, key, parent);
  if(item == NULL) return false;
  if(!fetch_array_data(item, out))
    {
      PyErr_Format(PyExc_TypeError, "%s: Not of type numpy.ndarray", key);
      return false;
    }
  return true;
}
static _Bool fetch_array_data(const PyObject *item, double **out)
{
  if(item == NULL || !PyArray_Check(item) || !PyArray_IS_C_CONTIGUOUS((PyArrayObject*)item))
    return false;
  *out = PyArray_DATA((PyArrayObject*)item);
  return true;
}

static PyMethodDef methods[] = {
  { "calc_P", (PyCFunction)py_calc_P, METH_VARARGS | METH_KEYWORDS, "calc_P" },
  { NULL, NULL, 0, NULL }
};
static struct PyModuleDef module_def = {
  .m_base = PyModuleDef_HEAD_INIT,
  .m_name = "c_dhe",   /* name of module */
  .m_doc = NULL, /* module documentation, may be NULL */
  .m_size = -1,       /* size of per-interpreter state of the module,
	       or -1 if the module keeps state in global variables. */
  .m_methods = methods,
  .m_slots = NULL
};
PyMODINIT_FUNC
PyInit_c_dhe(void)
{
  unsigned long i;
  import_array();
  PyObject *module = PyModule_Create(&module_def);
  for(i=0; i<N_named_T_brine_f; i++)
    PyModule_AddIntConstant(module, T_brine_functions[i].name, i);
  return module;
}
