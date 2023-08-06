def zip_header(t, P, data):
    return (("t", t), ("P", P)) + tuple(zip(
        ("T_sink", "T_source", "T_soil"),
        data
    ))


def T_brine_params(dt, n_sub_steps: int,
                   dC_brine: float,
                   U_brine: float,
                   L):
    dt_step = dt / n_sub_steps
    L0mcpdt = U_brine / dC_brine * dt_step
    lambda_brine = 0.5 * L / n_sub_steps
    L1mcpdt = lambda_brine * dt / dC_brine
    return {"kappa_ax": L0mcpdt,
            "kappa_rad": L1mcpdt,
            "lambda_brine": lambda_brine,
            "n_sub_steps": n_sub_steps}


def T_brine_method(method=None):
    """Dynamic T_brine method"""
    def T_brine(dt, n_sub_steps: int,
                dC_brine: float,
                U_brine: float,
                L):
        """Dynamic T_brine method"""
        _method = type('Method', (object,), {})()
        _method.parameters = T_brine_params(
            dt, n_sub_steps, dC_brine, U_brine, L)
        _method.method = method
        return _method
    return T_brine
