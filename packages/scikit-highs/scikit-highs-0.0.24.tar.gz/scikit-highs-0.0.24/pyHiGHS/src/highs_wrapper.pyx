# distutils: language=c++
# cython: language_level=3

from libc.stdio cimport FILE, tmpfile
from libcpp.memory cimport unique_ptr, make_unique

from HConst cimport ML_NONE
from Highs cimport Highs
from HighsStatus cimport (
    HighsStatus,
    HighsStatusError,
    HighsStatusWarning,
    HighsStatusOK,
)
from HighsLp cimport (
    HighsLp,
    HighsSolution,
    HighsModelStatus,
    HighsModelStatusNOTSET,
    HighsModelStatusLOAD_ERROR,
    HighsModelStatusMODEL_ERROR,
    HighsModelStatusMODEL_EMPTY,
    HighsModelStatusPRESOLVE_ERROR,
    HighsModelStatusSOLVE_ERROR,
    HighsModelStatusPOSTSOLVE_ERROR,
    HighsModelStatusPRIMAL_INFEASIBLE,
    HighsModelStatusPRIMAL_UNBOUNDED,
    HighsModelStatusOPTIMAL,
    HighsModelStatusREACHED_DUAL_OBJECTIVE_VALUE_UPPER_BOUND,
    HighsModelStatusREACHED_TIME_LIMIT,
    HighsModelStatusREACHED_ITERATION_LIMIT,
)
from HighsInfo cimport HighsInfo

cdef apply_options(dict options, Highs & highs):
    '''Take options from dictionary and apply to HiGHS object.'''

    # Send logging to dummy file to get rid of output from stdout
    cdef FILE * f
    if options.get('message_level', None) == ML_NONE:
        f = tmpfile()
        highs.setHighsLogfile(f)

    # Do all the ints
    for opt in [
            'ipm_iteration_limit',
            'max_threads',
            'message_level',
            'min_threads',
            'simplex_crash_strategy',
            'simplex_dual_edge_weight_strategy',
            'simplex_iteration_limit',
            'simplex_primal_edge_weight_strategy',
            'simplex_scale_strategy',
            'simplex_strategy',
            'simplex_update_limit',
            'small_matrix_value']:
        val = options.get(opt, None)
        if val is not None:
            highs.setHighsOptionValueInt(opt.encode(), val)

    # Do all the doubles
    for opt in [
            'dual_feasibility_tolerance',
            'dual_objective_value_upper_bound',
            'infinite_bound',
            'infinite_cost',
            'large_matrix_value',
            'primal_feasibility_tolerance',
            'small_matrix_value',
            'time_limit']:
        val = options.get(opt, None)
        if val is not None:
            highs.setHighsOptionValueDbl(opt.encode(), val)

    # Do all the strings
    for opt in ['solver']:
        val = options.get(opt, None)
        if val is not None:
            highs.setHighsOptionValueStr(opt.encode(), val.encode())

    # Do all the bool to strings
    for opt in ['parallel', 'presolve']:
        val = options.get(opt, None)
        if val is not None:
            if val:
                val0 = b'on'
            else:
                val0 = b'off'
            highs.setHighsOptionValueStr(opt.encode(), val0)

def highs_wrapper(
        double[::1] c,
        int[::1] astart,
        int[::1] aindex,
        double[::1] avalue,
        double[::1] lhs,
        double[::1] rhs,
        double[::1] lb,
        double[::1] ub,
        dict options):

    cdef int numcol = c.size
    cdef int numrow = rhs.size
    cdef int numnz = avalue.size

    # Fill up a HighsLp object
    cdef HighsLp lp
    lp.numCol_ = numcol
    lp.numRow_ = numrow
    lp.nnz_ = numnz

    lp.colCost_.resize(numcol)
    lp.colLower_.resize(numcol)
    lp.colUpper_.resize(numcol)

    lp.rowLower_.resize(numrow)
    lp.rowUpper_.resize(numrow)
    lp.Astart_.resize(numcol + 1)
    lp.Aindex_.resize(numnz)
    lp.Avalue_.resize(numnz)

    # Be careful not index into nothing
    cdef double * colcost_ptr = NULL
    cdef double * collower_ptr = NULL
    cdef double * colupper_ptr = NULL
    cdef double * rowlower_ptr = NULL
    cdef double * rowupper_ptr = NULL
    cdef int * astart_ptr = NULL
    cdef int * aindex_ptr = NULL
    cdef double * avalue_ptr = NULL
    if numrow > 0:
        rowlower_ptr = &lhs[0]
        rowupper_ptr = &rhs[0]
        lp.rowLower_.assign(rowlower_ptr, rowlower_ptr + numrow)
        lp.rowUpper_.assign(rowupper_ptr, rowupper_ptr + numrow)
    else:
        lp.rowLower_.empty()
        lp.rowUpper_.empty()
    if numcol > 0:
        colcost_ptr = &c[0]
        collower_ptr = &lb[0]
        colupper_ptr = &ub[0]
        lp.colCost_.assign(colcost_ptr, colcost_ptr + numcol)
        lp.colLower_.assign(collower_ptr, collower_ptr + numcol)
        lp.colUpper_.assign(colupper_ptr, colupper_ptr + numcol)
    else:
        lp.colCost_.empty()
        lp.colLower_.empty()
        lp.colUpper_.empty()
    if numnz > 0:
        astart_ptr = &astart[0]
        aindex_ptr = &aindex[0]
        avalue_ptr = &avalue[0]
        lp.Astart_.assign(astart_ptr, astart_ptr + numcol + 1)
        lp.Aindex_.assign(aindex_ptr, aindex_ptr + numnz)
        lp.Avalue_.assign(avalue_ptr, avalue_ptr + numnz)
    else:
        lp.Astart_.empty()
        lp.Aindex_.empty()
        lp.Avalue_.empty()

    # Create the options
    apply_options(options, highs)

    # Make a Highs object and pass it everything
    cdef Highs highs
    cdef HighsStatus init_status = highs.passModel(lp)
    if init_status != HighsStatusOK:
        if init_status != HighsStatusWarning:
            print("Error setting HighsLp");
            return <int>HighsStatusError

    # Solve the fool thing
    cdef HighsStatus run_status = highs.run()

    # Extract what we need from the solution
    #     HighsModelStatus
    #     solution
    #     dual solution
    #     objective value
    #     Number of iterations (simplex or ipm)
    #     sum of primal infeasibilities

    cdef HighsModelStatus model_status = highs.getModelStatus()
    cdef HighsModelStatus scaled_model_status = highs.getModelStatus(True)
    if model_status != scaled_model_status:
        if scaled_model_status == HighsModelStatusOPTIMAL:
            # The scaled model has been solved to optimality, but not the
            # unscaled model, flag this up, but report the scaled model
            # status
            print('model_status is not optimal, using scaled_model_status instead.')
            model_status = scaled_model_status

    # We might need an info object if we can look up the solution and a place to put solution
    cdef HighsInfo info
    cdef unique_ptr[HighsSolution] solution

    print('Got', highs.highsModelStatusToString(model_status).decode())

    # If the status is bad, don't look up the solution
    if model_status in [
            HighsModelStatusNOTSET,
            HighsModelStatusLOAD_ERROR,
            HighsModelStatusMODEL_ERROR,
            HighsModelStatusMODEL_EMPTY,
            HighsModelStatusPRESOLVE_ERROR,
            HighsModelStatusSOLVE_ERROR,
            HighsModelStatusPOSTSOLVE_ERROR,
            HighsModelStatusPRIMAL_INFEASIBLE,
            HighsModelStatusPRIMAL_UNBOUNDED,
    ]:
        return {
            'status': <int> model_status,
            'message': highs.highsModelStatusToString(model_status).decode(),
        }
    # If the model status is such that the solution can be read
    elif model_status in [
            HighsModelStatusOPTIMAL,
            HighsModelStatusREACHED_DUAL_OBJECTIVE_VALUE_UPPER_BOUND,
            HighsModelStatusREACHED_TIME_LIMIT,
            HighsModelStatusREACHED_ITERATION_LIMIT,
    ]:
        info = highs.getHighsInfo()
        solution = make_unique[HighsSolution](highs.getSolution())
        return {
            'status': <int> model_status,
            'message': highs.highsModelStatusToString(model_status).decode(),
            'x': [solution.get().col_value[ii] for ii in range(numcol)],
            'slack': [solution.get().row_value[ii] for ii in range(numrow)],
            'fun': info.objective_function_value,
            'simplex_nit': info.simplex_iteration_count,
            'ipm_nit': info.ipm_iteration_count,
            'crossover_nit': info.crossover_iteration_count,
            'con': info.sum_primal_infeasibilities,
        }

# Export some things
from HConst cimport (
    HIGHS_CONST_I_INF,
    HIGHS_CONST_INF,
)
CONST_I_INF = HIGHS_CONST_I_INF
CONST_INF = HIGHS_CONST_INF
