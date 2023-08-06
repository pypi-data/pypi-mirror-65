'''Try kernel training using kd-tree.'''

import numpy as np

def grappa(kspace, calib, kernel_size=(5, 5)):
    '''GRAPPA.'''

    mask = np.abs(kspace[..., 0]) > 0


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from phantominator import shepp_logan
    from utils import gaussian_csm

    N, nc = 32, 4
    ph = shepp_logan(N)
    csm = gaussian_csm(N, N, nc)
    ph = ph[..., None]*csm

    kspace = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(
        ph, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))

    # Get calibration region
    pd = 10
    ctr = int(N/2)
    calib = kspace[ctr-pd:ctr+pd, ctr-pd:ctr+pd, ...].copy()

    # undersample by a factor of 2 in both kx and ky
    kspace[::2, 1::2, ...] = 0
    kspace[1::2, ::2, ...] = 0
    kspace[ctr-pd:ctr+pd, ctr-pd:ctr+pd, ...] = calib

    res = grappa(kspace, calib)

    plt.imshow(np.abs(res[..., 0]))
    plt.show()

    res = np.fft.ifftshift(np.fft.ifft2(np.fft.fftshift(
        res, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))
    sos = np.sqrt(np.sum(np.abs(res)**2, axis=-1))

    plt.imshow(sos)
    plt.show()
