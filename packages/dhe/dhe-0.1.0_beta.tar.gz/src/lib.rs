#![allow(non_snake_case)]

use std::fmt::Display;

use numpy::{PyArray1, PyArray2, PyArray4};
use pyo3::prelude::{pymodule, pyclass, pymethods, Py, PyModule, PyResult, Python, PyErr, PyObject, AsPyRef, PyCell};
use pyo3::exceptions::RuntimeError;
use pyo3::{FromPyObject, ToPyObject};
use pyo3::types::{PyAny, PySequence};

use libdhe as dhe;

fn make_error<E: Display + Sized>(e: E) -> PyErr {
    PyErr::new::<RuntimeError, _>(format!("{}", e))
}

trait _FromPyObject<'source>: Sized {
    fn _extract(ob: &'source PyAny) -> PyResult<Self>;
}
macro_rules! impl_from_py_object_builtin {
    ($($t:ty),+) => { $(
	impl _FromPyObject<'_> for $t {
	    fn _extract(ob: &PyAny) -> PyResult<Self> { type T = $t; T::extract(ob) }
	}
    )* }
}
impl_from_py_object_builtin!(f64, usize, [f64; 5]);

struct Foreign<T>(T);
impl<'src, T: _FromPyObject<'src>> FromPyObject<'src> for Foreign<T> {
    fn extract(ob: &'src PyAny) -> PyResult<Self> { T::_extract(ob).map(|x| Foreign(x)) }
}

macro_rules! impl_from_py_object {
    ($t:ty, $($f_from:ident -> $f_to:ident),+) => {
	impl _FromPyObject<'_> for $t {
	    fn _extract(ob: &PyAny) -> PyResult<Self> {
		let gil = Python::acquire_gil();
		let py = gil.python();
		let o = ob.to_object(py);
		type T = $t;
		println!(stringify!($t));
		let out = T{
		    $($f_to: <_>::_extract(&o.getattr(py, stringify!($f_from))?.as_ref(py))?,)*
		};
		Ok(out)
	    }
	}
    }
}
impl_from_py_object!(dhe::MaterialProperties, rho->rho, c -> c, lambda_ -> lambda);
impl_from_py_object!(dhe::FluidProperties, rho -> rho, c -> c, lambda_ -> lambda, nu -> nu);
impl_from_py_object!(dhe::SoilLayerProperties, rho -> rho, c -> c, lambda_ -> lambda, d -> d);
impl_from_py_object!(dhe::SoilParameters, T_soil_mean -> T_soil_mean, T_grad -> T_grad);
impl_from_py_object!(dhe::TSoil0Parameters, d_DHE->d_DHE, g_coefs -> g_coefs);
impl_from_py_object!(dhe::DHE2, x->x, y->y, L->L, D->D, D_borehole->D_borehole, thickness->thickness, Ra->Ra, Rb->Rb, R1->R1, fill_properties->fill_properties, T_soil_0_parameters->T_soil_0_parameters, brine_properties->brine_properties, Phi_m->Phi_m);
impl_from_py_object!(dhe::GlobalParameters<BoundaryMethod>, dim_ax->dim_ax, dim_rad->dim_rad, g_method->g_method, soil_layers->soil_layers, R->R, opt_n_steps_multiplier->optimal_n_steps_multiplier, Gamma->Gamma, adiabat->adiabat, n_steps_0->n_steps_0, dt_boundary_refresh->dt_boundary_refresh, dt->dt, t0->t0, soil_parameters->soil_parameters);

type BoundaryMethod = Foreign<Box<dyn dhe::BoundaryMethod>>;

impl _FromPyObject<'_> for BoundaryMethod {
    fn _extract(any: &PyAny) -> PyResult<Self> {
	println!("BoundaryMethod");
	if let Ok(g) = any.downcast::<PyCell<GFuncParameters>>() {
	    Ok(Foreign(Box::new(g.borrow().wrapped.clone())))
	} else { Ok({
	    any.downcast::<PyCell<GConeParameters>>()?;
	    Foreign(Box::new(dhe::GConeParameters{}))
	}) }
    }
}

fn extract_sequence<'s, T>(seq: &'s PySequence) -> PyResult<Vec<T>>
where
    T: _FromPyObject<'s>,
{
    use pyo3::ObjectProtocol;
    println!("extract_sequence");
    let mut v = Vec::with_capacity(seq.len().unwrap_or(0) as usize);
    for item in seq.iter()? {
        v.push(<_>::_extract(item?)?);
    }
    Ok(v)
}
impl<'a, T: _FromPyObject<'a>> _FromPyObject<'a> for Vec<T> {
    fn _extract(ob: &'a PyAny) -> PyResult<Self> {
	extract_sequence(ob.downcast()?)
    }
}


type CalcMethod = fn(&[f64], &[f64], &[dhe::DHE2], &dhe::GlobalParameters<BoundaryMethod>, f64, &mut [dhe::CalcPOutput]) -> Result<(), String>;

#[pyclass]
#[derive(Clone)]
struct TBrineMethod {
    method: CalcMethod
}

struct GlobalParameters {
    env: dhe::GlobalParameters<BoundaryMethod>,
    calc_method: CalcMethod
}

impl FromPyObject<'_> for GlobalParameters {
    fn extract(ob: &PyAny) -> PyResult<Self> {
	let gil = Python::acquire_gil();
	let py = gil.python();
	let o = ob.to_object(py);
	println!("GlobalParameters");
	Ok(GlobalParameters{
	    calc_method: o.getattr(py, "T_brine_method")?.extract::<TBrineMethod>(py)?.method,
	    env: <_>::_extract(ob)?})
    }
}

impl dhe::BoundaryMethod for BoundaryMethod {
    fn g_func(&self,
	      t: &[f64],
	      c_V_soil: &[f64],
	      lambda_soil: &[f64],
	      r: &[f64]
    ) -> Vec<f64> {
	self.0.g_func(t, c_V_soil, lambda_soil, r)
    }
}

#[pyclass]
struct GFuncParameters {
    wrapped: dhe::GFuncParameters 
}
#[pymethods]
impl GFuncParameters {
    #[new]
    fn new(g_coefs: (f64, f64, f64, f64, f64, f64),
	   u_min: f64,
	   L: f64,
	   go_const: f64
    ) -> Self {
	Self{wrapped: dhe::GFuncParameters{g_coefs: [g_coefs.0, g_coefs.1, g_coefs.2, g_coefs.3, g_coefs.4, g_coefs.5], u_min, L, go_const}}
    }
}

#[pyclass]
struct GConeParameters{}
#[pymethods]
impl GConeParameters {
    #[new]
    fn new() -> Self { Self{} }
}

#[pymodule]
fn dhe(py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m, "calc_P")]
    fn calc_P(
	py: Python,
	t: &PyArray1<f64>,
	P: &PyArray1<f64>,
	dhe: Foreign<Vec<dhe::DHE2>>,
	env: GlobalParameters,
	precision: f64,
    ) -> PyResult<(Py<PyArray2<f64>>, Py<PyArray2<f64>>, Py<PyArray4<f64>>)>
    {
	let GlobalParameters{env, calc_method} = env;
	let dim_t = P.len();
	let dhe = dhe.0;
	let n_DHE: usize = dhe.len();
	let dim_ax = env.dim_ax;
	let dim_rad = env.dim_rad;

	let py_out_T_sink = PyArray2::new(py, [n_DHE, dim_t], false);
	let py_out_T_source = PyArray2::new(py, [n_DHE, dim_t], false);
	let py_out_T_soil = PyArray4::new(py, [n_DHE, dim_t, dim_rad + 2, dim_ax], false);
	let chunk_size_T_soil = dim_t * (dim_rad + 2) * dim_ax;
	let mut out: Vec<dhe::CalcPOutput> = (0..n_DHE).map(|i| Ok(dhe::CalcPOutput{
	    T_sink: &mut py_out_T_sink.as_slice_mut()?[i*dim_t..(i+1)*dim_t],
	    T_source: &mut py_out_T_source.as_slice_mut()?[i*dim_t..(i+1)*dim_t],
	    T_soil: &mut py_out_T_soil.as_slice_mut()?[i*chunk_size_T_soil..(i+1)*chunk_size_T_soil]
	})).collect::<Result<Vec<dhe::CalcPOutput>, PyErr>>()?;
	calc_method(
	    t.as_slice()?,
	    P.as_slice()?,
	    &dhe,
	    &env,
	    precision,
	    &mut out).map_err(make_error)?;
	Ok((py_out_T_sink.to_owned(), py_out_T_source.to_owned(), py_out_T_soil.to_owned()))
    }

    m.add("T_BRINE_METHOD_DYNAMIC", PyCell::new(py, TBrineMethod{method: dhe::calc_P_2::<dhe::TBrineDynamicParameters, _>})?)?;
    m.add("T_BRINE_METHOD_STATIONARY", PyCell::new(py, TBrineMethod{method: dhe::calc_P_2::<dhe::TBrineStationaryParameters, _>})?)?;
    m.add_class::<GFuncParameters>()?;
    m.add_class::<GConeParameters>()?;
    Ok(())
}
