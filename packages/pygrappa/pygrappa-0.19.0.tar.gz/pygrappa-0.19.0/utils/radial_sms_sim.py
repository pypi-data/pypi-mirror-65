'''Simulate a radial SMS acquisiton.'''

import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan
from phantominator import kspace_shepp_logan, radial
from phantominator.kspace import _modified_shepp_logan_params_2d

from utils import gridder

def cartesian_sms_sim(N, nSMS, phi=None):
    '''Cartesian simulation of SMS acquisiton.

    Notes
    -----
    Implements generalized Cartesian example as shown in Figure 2 in
    [1]_.

    References
    ----------
    .. [1] Yutzy, Stephen R., et al. "Improvements in multislice
           parallel imaging using radial CAIPIRINHA." Magnetic
           resonance in medicine 65.6 (2011): 1630-1637.
    '''

    # Get slices of 3D Shepp-Logan phantom
    ph = shepp_logan((N, N, nSMS), zlims=(-.3, 0))
    kspace = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(
        ph, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))

    # Construct CAIPI phase cycling
    if phi is None:
        phi = [ii*2*np.pi/nSMS for ii in range(nSMS)]

    # Apply phase
    for sl in range(nSMS):
        for ii in range(N):
            kspace[ii, ..., sl] *= np.exp(
                1j*np.mod(ii*phi[sl], 2*np.pi))

    # Simulate SMS
    kspace = np.sum(kspace, -1)

    im = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        kspace, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))
    plt.imshow(np.abs(im))
    plt.show()

    # Isolate slices
    res = np.zeros(kspace.shape + (nSMS,), dtype=kspace.dtype)
    for sl in range(nSMS):
        res[..., sl] = kspace.copy()
        for ii in range(N):
            res[ii, ..., sl] *= np.exp(
                -1j*np.mod(ii*phi[sl], 2*np.pi))

    # See what we did
    im = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        res, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))
    for sl in range(nSMS):
        plt.subplot(1, nSMS, sl+1)
        plt.imshow(np.abs(im[..., sl]))
    plt.show()


def radial_sms_sim(N, spokes, nSMS, phi=None):
    '''Radial simulation of SMS acquisiton.

    Notes
    -----
    Implements generalized radial example as shown in Figure 2 of
    [1]_.
    '''

    E = _modified_shepp_logan_params_2d()
    kx, ky = radial(N, spokes)
    kx = np.reshape(kx, (N, spokes), order='F').flatten()
    ky = np.reshape(ky, (N, spokes), order='F').flatten()

    k = []
    for sl in range(nSMS):
        E0 = E.copy()
        E0[:, 1] *= (sl+1)/nSMS
        E0[:, 2] *= (sl+1)/nSMS
        E0[:, 3] *= (sl+1)/nSMS
        E0[:, 4] *= (sl+1)/nSMS
        k.append(kspace_shepp_logan(kx/2, ky/2, E=E0)[..., None])
    k = np.concatenate(k, axis=-1)

    im = gridder(kx, ky, k, N, N)
    for sl in range(nSMS):
        plt.subplot(1, nSMS, sl+1)
        plt.imshow(np.abs(im[..., sl]))
    plt.show()

    # Construct CAIPI phase cycling
    if phi is None:
        phi = [ii*2*np.pi/nSMS for ii in range(nSMS)]

    # Apply phase
    k = np.reshape(k, (N, spokes, nSMS))
    for sl in range(nSMS):
        for ii in range(spokes):
            k[:, ii, sl] *= np.exp(
                1j*np.mod(ii*phi[sl], 2*np.pi))
    k = np.reshape(k, (-1, nSMS))

    im = gridder(kx, ky, k, N, N)
    for sl in range(nSMS):
        plt.subplot(1, nSMS, sl+1)
        plt.imshow(np.abs(im[..., sl]))
    plt.show()

    # Simulate SMS
    k = np.sum(k, -1)

    im = gridder(kx, ky, k[..., None], N, N).squeeze()
    plt.imshow(np.abs(im))
    plt.show()

    # Isolate slices
    res = np.zeros((N, spokes, nSMS,), dtype=k.dtype)
    for sl in range(nSMS):
        res[..., sl] = np.reshape(k, (N, spokes))
        for ii in range(spokes):
            res[:, ii, sl] *= np.exp(
                -1j*np.mod(ii*phi[sl], 2*np.pi))

    im = gridder(kx, ky, res.reshape((-1, nSMS)), N, N)
    for sl in range(nSMS):
        plt.subplot(1, nSMS, sl+1)
        plt.imshow(np.abs(im[..., sl]))
    plt.show()


if __name__ == '__main__':

    cartesian_sms_sim(128, nSMS=3, phi=None)
    radial_sms_sim(288, 72, nSMS=3, phi=None)
