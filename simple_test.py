from dolfin import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sps

# from block.iterative import *
# from block.algebraic.petsc import ML, collapse
#from fenics_ii.xii.linalg.bc_apply import apply_bc

import ctypes

hazmath_path = '/home/fenics/shared/Software/hazmath/lib/libhazmath.so'

# ---------------------------------------------------------------------------- #

def mixed():
    # Create mesh and define function space
    mesh = UnitSquareMesh(32, 32)
    V = FunctionSpace(mesh, "RT", 1)
    Q = FunctionSpace(mesh, "DG", 0)
    W = [V, Q]

    # Define variational problem
    u, p = list(map(TrialFunction, W))
    v, q = list(map(TestFunction, W))
    f = Expression("10*exp(-(pow(x[0] - 0.5, 2) + pow(x[1] - 0.5, 2)) / 0.02)",
                   degree=2)

    a00 = inner(u, v) * dx
    a01 = - div(v) * p * dx
    a10 = - div(u) * q * dx
    a11 = Constant(0) * inner(p, q) * dx

    nu = FacetNormal(mesh)

    L0 = Constant(0) * dot(v, nu) * ds
    L1 = f * q * dx

    # Assemble system
    A00, A01, A10, A11 = map(assemble, (a00, a01, a10, a11))
    b0, b1 = map(assemble, (L0, L1))
    
    as_petsc = lambda A: as_backend_type(A).mat()

    A00, A01, A10, A11 = map(as_petsc, (A00, A01, A10, A11))
    ###exi
    # compute solution with hazmath
    # A in csr format
    A00csr = sps.csr_matrix(A00.getValuesCSR()[::-1],
                            shape=A00.size)
    indptr_size00 = A00csr.shape[0] + 1
    nrow00 = ctypes.c_int(A00csr.shape[0])
    ncol00 = ctypes.c_int(A00csr.shape[1])
    nnz00 = ctypes.c_int(A00csr.nnz)

    # A in csr format
    A01csr = sps.csr_matrix(A01.getValuesCSR()[::-1],
                            shape=A01.size)
    indptr_size01 = A01csr.shape[0] + 1
    nrow01 = ctypes.c_int(A01csr.shape[0])
    ncol01 = ctypes.c_int(A01csr.shape[1])
    nnz01 = ctypes.c_int(A01csr.nnz)

    # A in csr format
    A10csr = sps.csr_matrix(A10.getValuesCSR()[::-1], shape=A10.size)
    indptr_size10 = A10csr.shape[0] + 1
    nrow10 = ctypes.c_int(A10csr.shape[0])
    ncol10 = ctypes.c_int(A10csr.shape[1])
    nnz10 = ctypes.c_int(A10csr.nnz)

    # A in csr format
    A11csr = sps.csr_matrix(A11.getValuesCSR()[::-1], shape=A11.size)
    indptr_size11 = A11csr.shape[0] + 1
    nrow11 = ctypes.c_int(A11csr.shape[0])
    ncol11 = ctypes.c_int(A11csr.shape[1])
    nnz11 = ctypes.c_int(A11csr.nnz)

    # Pressure mass matrix
    a11_mass = inner(p, q) * dx
    A11_mass = PETScMatrix()
    assemble(a11_mass, tensor=A11_mass)
    A11_masss = as_backend_type(A11_mass).mat()
    A11_masss_csr = sps.csr_matrix(A11_masss.getValuesCSR()[::-1],
                                  shape=A11_masss.size)
    A11_diag = A11_masss_csr.diagonal()

    # b as array
    b0.get_local()
    b1.get_local()
    b = np.concatenate((b0, b1))

    # allocate solution
    u_shape = A00csr.shape[0] + A11csr.shape[0]
    nrow_double = ctypes.c_double * u_shape
    u_haz = nrow_double()

    # parameters for the solver
    tol = ctypes.c_double(1e-6)
    maxit = ctypes.c_int(100)
    print_lvl = ctypes.c_int(3)
    iters = ctypes.c_int(-1)

    # load library
    libHAZMATHsolver = ctypes.cdll.LoadLibrary(hazmath_path)

    libHAZMATHsolver.python_wrapper_krylov_mixed_darcy(
        ctypes.byref(nrow00),
        ctypes.byref(ncol00),
        ctypes.byref(nnz00),
        (ctypes.c_int * indptr_size00)(*A00csr.indptr),
        (ctypes.c_int * A00csr.nnz)(*A00csr.indices),
        (ctypes.c_double * A00csr.nnz)(*A00csr.data),
        ctypes.byref(nrow01),
        ctypes.byref(ncol01),
        ctypes.byref(nnz01),
        (ctypes.c_int * indptr_size01)(*A01csr.indptr),
        (ctypes.c_int * A01csr.nnz)(*A01csr.indices),
        (ctypes.c_double * A01csr.nnz)(*A01csr.data),
        ctypes.byref(nrow10),
        ctypes.byref(ncol10),
        ctypes.byref(nnz10),
        (ctypes.c_int * indptr_size10)(*A10csr.indptr),
        (ctypes.c_int * A10csr.nnz)(*A10csr.indices),
        (ctypes.c_double * A10csr.nnz)(*A10csr.data),
        ctypes.byref(nrow11),
        ctypes.byref(ncol11),
        ctypes.byref(nnz11),
        (ctypes.c_int * indptr_size11)(*A11csr.indptr),
        (ctypes.c_int * A11csr.nnz)(*A11csr.indices),
        (ctypes.c_double * A11csr.nnz)(*A11csr.data),
        (ctypes.c_double * A11csr.shape[0])(*A11_diag),
        (ctypes.c_double * u_shape)(*b),
        ctypes.byref(u_haz),
        ctypes.byref(tol),
        ctypes.byref(maxit),
        ctypes.byref(print_lvl),
        ctypes.byref(iters)
    )


    import scipy as sp
    u2 = sp.array(u_haz)

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    mixed()
