'''Test that VC-GRAPPA doesn't break with different sizes.'''

import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan
from skimage.metrics import normalized_root_mse as compare_nrmse # pylint: disable=E0611,E0401

from pygrappa import cgrappa, vcgrappa
from utils import gaussian_csm

if __name__ == '__main__':

    # Simple phantom
    N, ncoil = 128, 8
    _, phi = np.meshgrid( # background phase variation
        np.linspace(-np.pi, np.pi, N),
        np.linspace(-np.pi, np.pi, N))
    phi = np.exp(1j*phi)
    ph = shepp_logan(N)*phi
    ph = ph[..., None]*gaussian_csm(N, N, ncoil)

    trims = [(0, 0), (0, 1), (1, 0), (1, 1)]
    ax = (0, 1)
    for trim in trims:

        ph0 = ph[:N-trim[0], :N-trim[1], :]
        print(ph0.shape[0], ph0.shape[1])

        # Throw into k-space
        kspace = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(
            ph0, axes=ax), axes=ax), axes=ax)

        # 20x20 ACS region
        pad = 10
        ctr0, ctr1 = int(kspace.shape[0]/2), int(kspace.shape[1]/2)
        calib = kspace[
            ctr0-pad:ctr0+pad, ctr1-pad:ctr1+pad, :].copy()

        # R=2x2
        kspace[::2, 1::2, :] = 0
        kspace[1::2, ::2, :] = 0

        # Make sure VC-GRAPPA does better
        res_grappa = cgrappa(kspace, calib)
        res_vcgrappa = vcgrappa(kspace, calib)

        # Bring back to image space
        imspace_vcgrappa = np.fft.fftshift(np.fft.ifft2(
            np.fft.ifftshift(
                res_vcgrappa, axes=ax), axes=ax), axes=ax)
        imspace_grappa = np.fft.fftshift(np.fft.ifft2(
            np.fft.ifftshift(
                res_grappa, axes=ax), axes=ax), axes=ax)

        # Coil combine (sum-of-squares)
        cc_vcgrappa = np.sqrt(
            np.sum(np.abs(imspace_vcgrappa)**2, axis=-1))
        cc_grappa = np.sqrt(
            np.sum(np.abs(imspace_grappa)**2, axis=-1))
        cc_ph0 = np.sqrt(np.sum(np.abs(ph0)**2, axis=-1))

        # Normalize
        cc_vcgrappa /= np.max(cc_vcgrappa.flatten())
        cc_grappa /= np.max(cc_grappa.flatten())
        cc_ph0 /= np.max(cc_ph0.flatten())

        # Take a look
        nx, ny = 1, 2
        plt.subplot(nx, ny, 1)
        plt.imshow(cc_vcgrappa, cmap='gray')
        plt.title('VC-GRAPPA')
        plt.xlabel('NRMSE: %g' % compare_nrmse(cc_ph0, cc_vcgrappa))

        plt.subplot(nx, ny, 2)
        plt.imshow(cc_grappa, cmap='gray')
        plt.title('GRAPPA')
        plt.xlabel('NRMSE: %g' % compare_nrmse(cc_ph0, cc_grappa))

        plt.show()

        print(compare_nrmse(
            cc_ph0, cc_vcgrappa) < compare_nrmse(cc_ph0, cc_grappa))
