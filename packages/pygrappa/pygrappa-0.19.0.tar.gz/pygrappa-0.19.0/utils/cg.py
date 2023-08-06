'''CG methods.'''

def CG(forward_fun, b, tol=1e-5, maxiter=150):
    '''Conjugate gradient method.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Conjugate_gradient_method
    '''

    x0 = np.zeros(b.shape, dtype=b.dtype)

    # r = b - A @ x0
    r = b - forward_fun(x0)

    p = r.copy()
    rTr = r.conj().T @ r
    for _ii in range(maxiter):

        # Ap = A @ p
        Ap = forward_fun(p)
        alpha = rTr/(p.conj().T @ Ap)
        x += alpha*p
        r -= alpha*Ap

        if np.linalg.norm(p) < tol:
            break

        rTr_next = r.conj().T @ r
        beta = rTr_next/rTr
        rTr = rTr_next

        p = r + beta*p

    return x
