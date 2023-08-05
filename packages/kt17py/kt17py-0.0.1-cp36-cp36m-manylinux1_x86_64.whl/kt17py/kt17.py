from . import _kt17

import numpy as np
import logging


class Kt17:
    def __init__(self, rhel, idx):
        """ Initializes KT17 setting model's dynamic parameters

            :param rhel (float): heliocentric distance in astronomical units
            :param idx (float): disturbance index as defined by Anderson et al. (2013)

        """
        self.rhel = rhel
        self.idx = idx

        if type(self.rhel) not in [float]:
            raise TypeError("Heliocentric distance is not a float number")
        if type(self.idx) not in [float]:
            raise TypeError("Disturbance index is not a float number")

        self.logger = logging.getLogger('kt17py.Kt17')
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d-%(name)s-%(levelname)s %(message)s',
                                          "%Y-%m-%dT%H:%M:%S"))
        self.logger.addHandler(ch)

        _kt17.kt17_initialize(self.rhel, self.idx)

    def bfield(self, xyz_msm):
        """ Returns the magnetic field components  KT17 setting model's dynamic parameters

            :param xyz_msm: Mercury-centric Solar Magnetospheric coordinates in units of
                            the Mercury radius (2440 Km).
            :return the magnetic field components in Mercury-centric Solar Magnetospheric coordinates, in nT

        """
        self.logger.debug("KT17 Model: distance = {distance}UA, disturbance_index = {idx}"
                          .format(distance=self.rhel, idx=self.idx))

        if not isinstance(xyz_msm, np.ndarray) or xyz_msm.ndim != 2:
            raise TypeError("Input coordinates is not a valid 2d numpy array")

        m = np.shape(xyz_msm)[0]
        n = np.shape(xyz_msm)[1]

        if n != 3:
            raise TypeError("Input coordinates is not a valid ({m}, 3) numpy array".format(m=m))

        x_msm = np.reshape(xyz_msm[:, 0:1], (m,))
        y_msm = np.reshape(xyz_msm[:, 1:2], (m,))
        z_msm = np.reshape(xyz_msm[:, 2:], (m,))

        b_msm = _kt17.kt17_bfield(x_msm, y_msm, z_msm)

        return np.transpose(b_msm)
