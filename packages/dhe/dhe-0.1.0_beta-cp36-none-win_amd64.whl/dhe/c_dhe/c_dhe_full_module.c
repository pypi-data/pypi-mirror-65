#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include "c_dhe_full.h"

typedef _Bool parser(PyObject*, void*);

static int PyGlobalParameters_Converter(PyObject* obj, void **address);
static _Bool obj_get_uint(PyObject *obj, const char *key, unsigned int *out, const char *parent);
static _Bool obj_get_double(PyObject *obj, const char *key, double *out, const char *parent);
static _Bool obj_get_array(PyObject *obj, const char *key, size_t struct_size,
				parser parse_item,
				void **out_struct, unsigned int *out_n, const char *arr_name);
static _Bool obj_get_struct(PyObject *obj, const char *key, parser *type, void *out, const char *parent);
static PyObject* _obj_get_obj(PyObject *obj, const char *key, const char *parent);
static _Bool obj_get_obj(PyObject *obj, const char *key, PyObject** out, const char *parent);
static _Bool check(_Bool result, PyObject *err_type, const char* err_msg, ...);
static _Bool parse_struct_array(PyObject* obj, size_t struct_size,
				parser *parse_item,
				void **out_struct, unsigned int *out_n, const char *arr_name);
static _Bool parse_T_soil_0_properties(PyObject* obj, void* void_address);
static _Bool parse_material_properties(PyObject* obj, void* void_address);
static _Bool parse_fluid_properties(PyObject* obj, void* void_address);
static _Bool parse_soil_parameters(PyObject* obj, void* void_address);
static _Bool parse_soil_layer_properties(PyObject* obj, void* void_address);
static _Bool parse_g_method(PyObject* obj, void* void_address);
static _Bool parse_double(PyObject* obj, void* void_address);
static _Bool PyDHE_parse(PyObject* obj, DHE2* dhe);
static _Bool parse_double_seq(PyObject* obj, unsigned int n, void* void_address, const char* name);

static PyObject *py_calc_P(PyObject *self, PyObject *args, PyObject *keywords) {
  unsigned int i;
  PyArrayObject *py_t, *py_P;
  PyObject *py_out_T_sink, *py_out_T_source, *py_out_T_soil;
  PyObject *py_dhe;
  PyObject *retval = NULL;
  DHE2 *dhe = NULL;
  GlobalParameters *env = NULL;
  unsigned int n_DHE = 0;
  unsigned int dim_rad, dim_ax;
  double precision = 0.05;

  if(PyArg_ParseTupleAndKeywords(args, keywords,
				 "O!O!|$OO&d:c_calc_P",
				 (char*[]){
				   "t",
				     "P",
				     "dhe",
				     "env",
				     "precision",
				     NULL},
				 &PyArray_Type, &py_t,
				 &PyArray_Type, &py_P,
				 &py_dhe,
				 &PyGlobalParameters_Converter, &env,
				 &precision)
     // Validate arguments
     && check(PyArray_NDIM(py_t) == 1, PyExc_ValueError, "t must be 1-dimensional")
     && check(PyArray_NDIM(py_P) == 1, PyExc_ValueError, "P must be 1-dimensional")
     && parse_struct_array(py_dhe, sizeof(DHE2), (parser*)&PyDHE_parse, (void**)&dhe, &n_DHE, "dhe")
     ) {
  npy_long dim_t = PyArray_DIMS(py_P)[0];
  dim_ax = env->dim_ax;
  dim_rad = env->dim_rad;
#define C_NDIM(arr) sizeof(arr)/sizeof(npy_intp)
  npy_intp dims_out_T[] = {n_DHE, dim_t};
  py_out_T_sink = PyArray_SimpleNew(C_NDIM(dims_out_T), dims_out_T, NPY_DOUBLE);
  py_out_T_source = PyArray_SimpleNew(C_NDIM(dims_out_T), dims_out_T, NPY_DOUBLE);
  npy_intp dims_out_T_soil[] = {n_DHE, dim_t, dim_rad + 2, dim_ax};
  py_out_T_soil = PyArray_SimpleNew(C_NDIM(dims_out_T_soil),
				    dims_out_T_soil, NPY_DOUBLE);
#undef C_NDIM
      CalcPOutput *out = malloc(n_DHE * sizeof(CalcPOutput));
      for(i=0; i<n_DHE; i++) {
	  out[i].T_sink = (double*)PyArray_DATA((PyArrayObject*)py_out_T_sink) + i*dim_t;
	  out[i].T_source = (double*)PyArray_DATA((PyArrayObject*)py_out_T_source) + i*dim_t;
	  out[i].T_soil = (double*)PyArray_DATA((PyArrayObject*)py_out_T_soil) + i*dim_t*(dim_rad+2)*dim_ax;
	}
      calc_P_2(PyArray_DATA(py_t),
	       PyArray_DATA(py_P),
	       dim_t,
	       dhe,
	       n_DHE,
	       env,
	       precision,
	       out);
      retval = PyTuple_Pack(3, py_out_T_sink, py_out_T_source, py_out_T_soil);
      Py_IncRef(retval);
      free(out);
    }
  free_global_parameters(env);
  if(dhe != NULL) free(dhe);
  return retval;
}

static _Bool check(_Bool result, PyObject *err_type, const char* err_msg, ...) {
  if(!result) {
      va_list ap;
      va_start(ap, err_msg);
      PyErr_FormatV(err_type, err_msg, ap);
      va_end(ap);
    }
  return result;
}

typedef struct {
    PyObject_HEAD
    void* data;
} WrapperObject;

static _Bool PyDHE_parse(PyObject* obj, DHE2* dhe) {
  #define T "DHE"
  if(
     !obj_get_double(obj, "x", &dhe->x, T)
     || !obj_get_double(obj, "y", &dhe->y, T)
     || !obj_get_double(obj, "L", &dhe->L, T)
     || !obj_get_double(obj, "D", &dhe->D, T)
     || !obj_get_double(obj, "D_borehole", &dhe->D_borehole, T)
     || !obj_get_double(obj, "thickness", &dhe->thickness, T)
     || !obj_get_double(obj, "Ra", &dhe->Ra, T)
     || !obj_get_double(obj, "Rb", &dhe->Rb, T)
     || !obj_get_double(obj, "R1", &dhe->R1, T)
     || !obj_get_struct(obj, "fill_properties", parse_material_properties, &dhe->fill_properties, T)
     || !obj_get_struct(obj, "T_soil_0_parameters", parse_T_soil_0_properties, &dhe->T_soil_0_parameters, T)
     || !obj_get_struct(obj, "brine_properties", parse_fluid_properties, &dhe->brine_properties, T)
     || !obj_get_double(obj, "Phi_m", &dhe->Phi_m, T)
     )
    return false;
  return true;
  #undef T  
}

static int PyGlobalParameters_Converter(PyObject* obj, void **address) {
  GlobalParameters *env = malloc(sizeof(GlobalParameters));
  PyObject *py_T_brine_method = NULL;
  #define T "GlobalParameters"
  if(
     !obj_get_uint(obj, "dim_ax", &env->dim_ax, T)
     || !obj_get_uint(obj, "dim_rad", &env->dim_rad, T)
     || !obj_get_obj(obj, "T_brine_method", &py_T_brine_method, T)
     || !obj_get_struct(obj, "g_method", parse_g_method, &env->g_method, T)
     || !obj_get_array(obj, "soil_layers", sizeof(SoilLayerProperties), &parse_soil_layer_properties, (void**)&env->soil_layers, &env->n_soil_layers, T)
     || !obj_get_double(obj, "R", &env->R, T)
     || !obj_get_double(obj, "opt_n_steps_multiplier", &env->optimal_n_steps_multiplier, T)
     || !obj_get_double(obj, "Gamma", &env->Gamma, T)
     || !obj_get_double(obj, "adiabat", &env->adiabat, T)
     || !obj_get_uint(obj, "n_steps_0", &env->n_steps_0, T)
     || !obj_get_double(obj, "dt_boundary_refresh", &env->dt_boundary_refresh, T)
     || !obj_get_double(obj, "dt", &env->dt, T)
     || !obj_get_double(obj, "t0", &env->t0, T)
     || !obj_get_struct(obj, "soil_parameters", &parse_soil_parameters, &env->soil_parameters, T)
     ) {
    free(env);
    return false;
  }
  env->T_brine_method = ((WrapperObject*)obj)->data;
  *address = env;
  return true;
  #undef T
}

static _Bool unpack_sequence(PyObject* seq,
			     size_t item_size,
			     parser parse_item,
			     void *out,
			     unsigned int n) {
  unsigned int i;
  for(i=0; i<n; i++)
    if(!(*parse_item)(PySequence_GetItem(seq, i), out + i*item_size))
      return false;
  return true;
}

static _Bool parse_double_seq(PyObject* obj, unsigned int n, void* void_address, const char* name) {
  if(!check(PySequence_Check(obj), PyExc_TypeError, "%s: Not a sequence", name))
    return false;
  if(!check(PySequence_Size(obj) == n, PyExc_ValueError, "%s: Expected sequence of size %i, found size %i", name, n, PySequence_Size(obj)))
    return false;
  if(!unpack_sequence(obj, sizeof(double), &parse_double, void_address, n)) {
    PyErr_Format(PyExc_TypeError, "%s: Contains items of wrong type (expected float)", name);
    return false;
  }
  return true;
}

static _Bool parse_struct_array(PyObject* obj, size_t struct_size,
				parser parse_item,
				void **out_struct, unsigned int *out_n, const char *arr_name) {
  void *out = NULL;
  unsigned int n;
  if(!check(PySequence_Check(obj), PyExc_TypeError, "%s: Not a sequence", arr_name))
    return false;
  n = PySequence_Size(obj);
  if(n > 0) {
    out = malloc(n * struct_size);
    if(!unpack_sequence(obj, struct_size, parse_item, out, n)) {
      free(out);
      return false;
    }
  }
  *out_struct = out;
  *out_n = n;
  return true;
}

typedef struct {
    PyObject_HEAD
    GFuncParameters wrapped;
} GFuncParametersObject;

static int
GFuncParametersObject_init(GFuncParametersObject *self, PyObject *args, PyObject *kwds);

PyTypeObject GFuncParametersType =
  {
   PyVarObject_HEAD_INIT(NULL, 0)
   .tp_name = "c_dhe.GFuncParameters",
   .tp_doc = PyDoc_STR("C_DHE GFuncParameters"),
   .tp_basicsize = sizeof(GFuncParametersObject),
   .tp_itemsize = 0,
   .tp_flags = Py_TPFLAGS_DEFAULT,
   .tp_new = PyType_GenericNew,
   .tp_init = (initproc)GFuncParametersObject_init,
  };

static int
GFuncParametersObject_init(GFuncParametersObject *self, PyObject *args, PyObject *kwds) {
    PyObject *py_g_coefs = NULL;

    if(!PyArg_ParseTupleAndKeywords(args, kwds,
				     "|Oddd",
				     (char*[]){
				       "g_coefs",
					 "u_min",
					 "L",
					 "go_const",
					 NULL},
                                     &py_g_coefs,
                                     &self->wrapped.u_min,
				     &self->wrapped.L,
				     &self->wrapped.go_const)
       || !parse_double_seq(py_g_coefs, 6, &self->wrapped.g_coefs, "GFuncParameters.g_coefs"))
        return -1;
    
    return 0;
}

typedef struct {
    PyObject_HEAD
    GConeParameters wrapped;
} GConeParametersObject;

PyTypeObject GConeParametersType =
  {
   PyVarObject_HEAD_INIT(NULL, 0)
   .tp_name = "c_dhe.GConeParameters",
   .tp_doc = PyDoc_STR("C_DHE GConeParameters"),
   .tp_basicsize = sizeof(GConeParametersObject),
   .tp_itemsize = 0,
   .tp_flags = Py_TPFLAGS_DEFAULT,
   .tp_new = PyType_GenericNew,
  };

static _Bool parse_g_method(PyObject* obj, void* void_address) {
  GMethod *m = (GMethod*)void_address;
  if(PyObject_TypeCheck(obj, &GConeParametersType)) {
    m->data = malloc(sizeof(GConeParameters));
    return true;
  }
  if(PyObject_TypeCheck(obj, &GFuncParametersType)) {
    GFuncParameters* prm = malloc(sizeof(GFuncParameters));
    *prm = ((GFuncParametersObject*)obj)->wrapped;
    m->data = prm;
    return true;
  }
  return false;
}

static _Bool parse_soil_parameters(PyObject* obj, void* void_address) {
  SoilParameters *address = (SoilParameters*)void_address;
  if(!obj_get_double(obj, "T_soil_mean", &address->T_soil_mean, "SoilParameters")
     || !obj_get_double(obj, "T_grad", &address->T_grad, "SoilParameters"))
    return false;
  return true;
}
static _Bool parse_soil_layer_properties(PyObject* obj, void* void_address) {
  SoilLayerProperties *address = (SoilLayerProperties*)void_address;
  if(!parse_material_properties(obj, address)
     || !obj_get_double(obj, "d", &address->d, "SoilParameters"))
    return false;
  return true;
}
static _Bool parse_fluid_properties(PyObject* obj, void* void_address) {
  FluidProperties *address = (FluidProperties*)void_address;
  if(!parse_material_properties(obj, address)
     || !obj_get_double(obj, "nu", &address->nu, "SoilParameters"))
    return false;
  return true;
}
static _Bool parse_material_properties(PyObject* obj, void* void_address) {
  MaterialProperties *address = (MaterialProperties*)void_address;
  if(!obj_get_double(obj, "rho", &address->rho, "SoilParameters")
     || !obj_get_double(obj, "c", &address->c, "SoilParameters")
     || !obj_get_double(obj, "lambda_", &address->lambda, "SoilParameters")
     )
    return false;
  return true;
}
static _Bool parse_T_soil_0_properties(PyObject* obj, void* void_address) {
PyObject *py_g_coefs = NULL;
  TSoil0Parameters *address = (TSoil0Parameters*)void_address;
  if(!obj_get_double(obj, "d_DHE", &address->d_DHE, "TSoil0Parameters")
     || !obj_get_obj(obj, "g_coefs", &py_g_coefs, "SoilParameters")
     || !parse_double_seq(py_g_coefs, 5, &address->g_coefs, "SoilParameters"))
    return false;
  return true;
}

static PyObject* _obj_get_obj(PyObject *obj, const char *key, const char *parent) {
  PyObject *item;
  item = PyObject_GetAttrString(obj, key);
  if(item == NULL)
    PyErr_Format(PyExc_KeyError, "%s[\"%s\"]", parent, key);
  return item;
}
static _Bool obj_get_struct(PyObject *obj, const char *key, parser type, void *out, const char *parent) {
  PyObject *item = _obj_get_obj(obj, key, parent);
  if(item == NULL) return false;
  return type(item, out);
}
static _Bool obj_get_obj(PyObject *obj, const char *key, PyObject **out, const char *parent) {
  PyObject *item = _obj_get_obj(obj, key, parent);
  if(item == NULL) return false;
  *out = item;
  return true;
}

static _Bool obj_get_uint(PyObject *obj, const char *key, unsigned int *out, const char *parent) {
  PyObject *item = _obj_get_obj(obj, key, parent);
  if(item == NULL) return false;
  if(!PyLong_Check(item)) {
      PyErr_Format(PyExc_TypeError, "%s: Not of type int", key);
      return false;
    }
  *out = (unsigned int)PyLong_AsLong(item);
  return true;
}
static _Bool parse_double(PyObject* obj, void* void_address) {
  if(!PyFloat_Check(obj)) return false;
  *(double*)void_address = PyFloat_AsDouble(obj);
  return true;
}

static _Bool obj_get_double(PyObject *obj, const char *key, double *out, const char *parent) {
  PyObject *item = _obj_get_obj(obj, key, parent);
  if(item == NULL) return false;
  if(!parse_double(item, out)) {
      PyErr_Format(PyExc_TypeError, "%s: Not of type float", key);
      return false;
    }
  return true;
}
static _Bool obj_get_array(PyObject *obj, const char *key, size_t struct_size,
				parser parse_item,
				void **out_struct, unsigned int *out_n, const char *arr_name) {
  PyObject *item = _obj_get_obj(obj, key, arr_name);
  return parse_struct_array(item, struct_size, parse_item, out_struct, out_n, arr_name);
}

PyTypeObject WrapperType =
  {
   PyVarObject_HEAD_INIT(NULL, 0)
   .tp_name = "c_dhe.Opaque",
   .tp_doc = PyDoc_STR("C_DHE opaque type"),
   .tp_basicsize = sizeof(WrapperObject),
   .tp_itemsize = 0,
   .tp_flags = Py_TPFLAGS_DEFAULT,
   .tp_new = PyType_GenericNew,
  };
static PyObject* wrapper_new(void* data) {
  WrapperObject *obj = PyObject_New(WrapperObject, &WrapperType);
  obj->data = data;
  return (PyObject*)obj;
}

static PyMethodDef methods[] = {
  { "calc_P", (PyCFunction)py_calc_P, METH_VARARGS | METH_KEYWORDS, "calc_P" },
  { NULL, NULL, 0, NULL }
};
static struct PyModuleDef module_def = {
  .m_base = PyModuleDef_HEAD_INIT,
  .m_name = "c_dhe_full",
  .m_doc = NULL,
  .m_size = -1,
  .m_methods = methods,
  .m_slots = NULL
};
static _Bool py_module_add(PyObject *mod, const char* name, PyObject *obj) {
  Py_INCREF(obj);
  if (PyModule_AddObject(mod, name, obj) < 0) {
    Py_DECREF(obj);
    return false;
  }
  return true;
}
PyMODINIT_FUNC
PyInit_c_dhe_full(void) {
  if(PyType_Ready(&GFuncParametersType) < 0
     || PyType_Ready(&GConeParametersType) < 0)
    return NULL;
  import_array();
  PyObject *module = PyModule_Create(&module_def);
  if(module == NULL) return NULL;
  Py_INCREF(&GFuncParametersType);
  Py_INCREF(&GConeParametersType);
  if(
     !py_module_add(module, "GFuncParameters", (PyObject*)&GFuncParametersType)
     || !py_module_add(module, "GConeParameters", (PyObject*)&GConeParametersType)
     || !py_module_add(module, "T_BRINE_METHOD_STATIONARY", wrapper_new(&T_brine_stationary))
     || !py_module_add(module, "T_BRINE_METHOD_DYNAMIC", wrapper_new(&T_brine_dynamic))) {
    Py_DECREF(module);
    return NULL;
  }
    
  return module;
}
