"""Kernal basis functions for KDE calculations.
"""
import logging
import six
from collections import OrderedDict

import numpy as np
import scipy as sp   # noqa
import scipy.stats   # noqa

from kalepy import utils
from kalepy import _NUM_PAD, _TRUNCATE_INFINITE_KERNELS

'''
__all__ = ['Kernel', 'Distribution',
           'Gaussian', 'Box_Asym', 'Parabola',  # 'Triweight',
           'get_distribution_class', 'get_all_distribution_classes']
'''

_INTERP_NUM_PER_STD = int(1e4)


class Kernel(object):

    def __init__(self, distribution=None, bandwidth=None, covariance=None,
                 helper=False, chunk=1e5):
        self._helper = helper
        distribution = get_distribution_class(distribution)
        self._distribution = distribution()
        self._chunk = int(chunk)

        if bandwidth is None:
            bandwidth = 1.0
            logging.warning("No `bandwidth` provided, setting to 1.0!")

        if covariance is None:
            covariance = 1.0
            logging.warning("No `covariance` provided, setting to 1.0!")

        bandwidth = np.atleast_2d(bandwidth)
        covariance = np.atleast_2d(covariance)
        matrix = covariance * np.square(bandwidth)
        self._ndim = np.shape(matrix)[0]
        self._matrix = matrix
        self._bandwidth = bandwidth
        self._covariance = covariance
        self._matrix_inv = None
        self._norm = None
        return

    def pdf(self, points, data, weights, reflect=None, params=None):
        pnts = np.atleast_2d(points)
        ndim, nval = np.shape(data)
        # print("pnts.shape = {}, len(pnts) = {}".format(np.shape(pnts), len(pnts)))

        # Check shape if unput `edges`
        if (params is None):
            # Should be edges for all parameters
            if len(pnts) != ndim:
                err = ("`points` has length {}, but data has {} parameters. "
                       "Provide an arraylike of edges for each dim/param!")
                err = err.format(len(pnts), ndim)
                raise ValueError(err)
        else:
            params = np.atleast_1d(params)
            # Should only be as many edges as target parameters
            if len(params) != len(pnts):
                err = "length of `params` = '{}', but nparams in `points` = {}!".format(
                    len(params), len(pnts))
                raise ValueError(err)

        # Make sure shape/values of reflect look okay
        reflect = self._check_reflect(reflect, ndim, data, weights)

        if reflect is None:
            result = self._pdf_clear(pnts, data, weights, params=params)
        else:
            result = self._pdf_reflect(pnts, data, weights, reflect)

        # print("Kernel.pdf(): result.shape = {}".format(result.shape))
        return result

    def _pdf_clear(self, pnts, data, weights, params=None):
        """

        If parameters are being selected (i.e. `params` is not None):
          - `pnts` should reflect only the *target* parameters.

        """
        # print("Kernel._pdf_clear()::")
        matrix_inv = self.matrix_inv
        norm = self.norm

        # Select subset of parameters
        if params is not None:
            matrix = self.matrix
            params, data, matrix, norm = self._params_subset(data, matrix, params)
            matrix_inv = utils.matrix_invert(matrix, helper=self._helper)

        npar_pnts, num_points = np.shape(pnts)
        npar_data, num_data = np.shape(data)
        if npar_pnts != npar_data:
            err = "`data` nparams ({}) does not match `pnts` ({})!  `params` = '{}'".format(
                npar_data, npar_pnts, params)
            raise ValueError(err)

        whitening = sp.linalg.cholesky(matrix_inv)
        # print("pnts: ndim = {}, npnts = {}, whitening = {}, weights = {}".format(
        #     npar_pnts, num_points, np.shape(whitening), np.shape(weights)))

        # Construct the whitened sampling points
        white_points = np.dot(whitening, pnts)

        result = np.zeros((num_points,), dtype=float)
        # Construct the 'whitened' (independent) dataset
        white_dataset = np.dot(whitening, data)
        # print("data: ndim = {}, npnts = {}, white_dataset = {}, white_points = {}".format(
        #     npar_data, num_data, np.shape(white_dataset), np.shape(white_points)))

        for ii in range(num_data):
            yy = white_points - white_dataset[:, ii, np.newaxis]
            # print(ii, np.shape(yy), yy)
            temp = weights[ii] * self.distribution.evaluate(yy)
            result += temp.squeeze()

        result = result / norm
        # print(params, "result = ", np.shape(result))
        return result

    def _pdf_reflect(self, pnts, data, weights, reflect):
        matrix_inv = self.matrix_inv
        norm = self.norm

        ndim, num_data = np.shape(data)
        ndim, num_points = np.shape(pnts)
        result = np.zeros((num_points,), dtype=float)

        whitening = sp.linalg.cholesky(matrix_inv)
        # Construct the 'whitened' (independent) dataset
        white_dataset = np.dot(whitening, data)
        # Construct the whitened sampling points
        white_points = np.dot(whitening, pnts)

        for ii in range(num_data):
            yy = white_points - white_dataset[:, ii, np.newaxis]
            result += weights[ii] * self.distribution.evaluate(yy)

        for ii, reflect_dim in enumerate(reflect):
            if reflect_dim is None:
                continue

            for loc in reflect_dim:
                if loc is None:
                    continue

                # shape (D,N) i.e. (dimensions, data-points)
                refl_data = np.array(data)
                refl_data[ii, :] = 2*loc - refl_data[ii, :]
                white_dataset = np.dot(whitening, refl_data)
                # Construct the whitened sampling points
                #    shape (D,M) i.e. (dimensions, sample-points)
                pnts = np.array(pnts)
                white_points = np.dot(whitening, pnts)

                if num_points >= num_data:
                    for jj in range(num_data):
                        yy = white_points - white_dataset[:, jj, np.newaxis]
                        result += weights[jj] * self.distribution.evaluate(yy)
                else:
                    for jj in range(num_points):
                        yy = white_dataset - white_points[:, jj, np.newaxis]
                        res = weights * self.distribution.evaluate(yy)
                        result[jj] += np.sum(res, axis=0)

            lo = -np.inf if reflect_dim[0] is None else reflect_dim[0]
            hi = +np.inf if reflect_dim[1] is None else reflect_dim[1]
            idx = (pnts[ii, :] < lo) | (hi < pnts[ii, :])
            result[idx] = 0.0

        result = result / norm
        return result

    def resample(self, data, weights, size=None, keep=None, reflect=None, squeeze=True):
        """
        """
        ndim, nval = np.shape(data)
        if size is None:
            size = nval

        size = int(np.floor(size))

        # Check if the number of samples being drawn is near the limit imposed by truncation
        trunc_num = int(1/_TRUNCATE_INFINITE_KERNELS)
        if (size/10 > trunc_num) and (not self.FINITE):
            err = "kernel is being truncated, not accurate near {} samples!".format(trunc_num)
            logging.warning(err)

        # Make sure `reflect` matches
        if reflect is not None:
            # This is now either (D,) [and contains `None` values] or (D,2)
            reflect = self._check_reflect(reflect, ndim, data, weights)

        # Have `Distribution` class perform resampling
        # ---------------------------------------------------
        if reflect is None:
            samples = self._resample_clear(data, weights, size, keep=keep)
        else:
            samples = self._resample_reflect(data, weights, size, reflect, keep=keep)

        if (ndim == 1) and squeeze:
            samples = samples.squeeze()

        return samples

    def _resample_clear(self, data, weights, size, matrix=None, keep=None):
        if matrix is None:
            matrix = self.matrix

        if (self._chunk is not None) and (self._chunk < size):
            logging.warning("Chunk size: {:.2e}, requested size: {:.2e}".format(self._chunk, size))
            logging.warning("Chunking is not setup in `_resample_clear`!")

        ndim, nvals = np.shape(data)
        # Draw from the smoothing kernel, here the `bw_matrix` includes the bandwidth
        norm = self.distribution.sample(size, ndim=ndim, squeeze=False)
        norm = utils.add_cov(norm, matrix)

        if keep is not None:
            if keep is True:
                keep = np.arange(ndim)
            elif keep is False:
                keep = []
            keep = np.atleast_1d(keep)
            for pp in keep:
                norm[pp, :] = 0.0

        indices = np.random.choice(nvals, size=size, p=weights)
        means = data[:, indices]
        # Shift each re-drawn sample based on the kernel-samples
        samps = means + norm
        return samps

    def _resample_reflect(self, data, weights, size, reflect, keep=None):
        matrix = self.matrix
        # Modify covariance-matrix for any `keep` dimensions
        matrix = self._cov_keep_vars(matrix, keep, reflect=reflect)

        ndim, nvals = np.shape(data)

        # Actually 'reflect' (append new, mirrored points) around the given reflection points
        # Also construct bounding box for valid data
        data, weights, bounds = self._reflect_data(data, weights, reflect)

        # Remove data points outside of kernels (or truncated region)
        data, weights = self._truncate_reflections(data, weights, bounds)

        if (self._chunk is not None) and (self._chunk < size):
            num_chunks = int(np.ceil(size/self._chunk))
            chunk_size = int(np.ceil(size/num_chunks))
        else:
            chunk_size = size
            num_chunks = 1

        # print("size = {}".format(size))
        # print("chunk_size = {}, num_chunks = {}".format(chunk_size, num_chunks))

        # Draw randomly from the given data points, proportionally to their weights
        samps = np.zeros((size, ndim))
        num_good = 0
        cnt = 0
        MAX = 10
        draw = chunk_size
        fracs = []
        while (num_good < size) and (cnt < MAX * num_chunks):
            # print(cnt, "draw = {}".format(draw))
            # Draw candidate resample points
            #    set `keep` to None, `matrix` is already modified to account for it
            trial = self._resample_clear(data, weights, draw, matrix=matrix, keep=None)
            # print(trial)
            # Find the (boolean) indices of values within target boundaries
            idx = utils.bound_indices(trial, bounds)

            # Store good values to output array
            ngd = np.count_nonzero(idx)
            fracs.append(ngd/idx.size)

            if num_good + ngd <= size:
                samps[num_good:num_good+ngd, :] = trial.T[idx, :]
            else:
                ngd = (size - num_good)
                samps[num_good:num_good+ngd, :] = trial.T[idx, :][:ngd]

            # Increment counters
            num_good += ngd
            cnt += 1
            # Next time, draw twice as many as we need
            draw = np.minimum(size - num_good, chunk_size)
            draw = (2**ndim) * draw
            draw = np.minimum(draw, int(self._chunk))

        if num_good < size:
            err = "Failed to draw '{}' samples in {} iterations!".format(size, cnt)
            logging.error("")
            logging.error(err)
            logging.error("fracs = {}\n\t{}".format(utils.stats_str(fracs), fracs))
            logging.error("Obtained {} samples".format(num_good))
            logging.error("Reflect: {}".format(reflect))
            logging.error("Bandwidths: {}".format(np.sqrt(self.matrix.diagonal().squeeze())))
            logging.error("data = ")
            for dd in data:
                logging.error("\t{}".format(utils.stats_str(dd)))

            raise RuntimeError(err)

        samps = samps.T
        return samps

    # ==== Utilities ====

    def _reflect_data(self, data, weights, reflect):
        bounds = np.zeros((data.shape[0], 2))

        old_data = np.copy(data)
        old_weights = np.copy(weights)

        for ii, reflect_dim in enumerate(reflect):
            if reflect_dim is None:
                bounds[ii, 0] = -np.inf
                bounds[ii, 1] = +np.inf
                continue

            for jj, loc in enumerate(reflect_dim):
                if loc is None:
                    # j=0 : -inf,  j=1: +inf
                    bounds[ii, jj] = np.inf * (2*jj - 1)
                    continue

                bounds[ii, jj] = loc
                new_data = np.array(old_data)
                new_data[ii, :] = loc - (new_data[ii, :] - loc)
                # NOTE: this returns a copy, so original `data` is *not* changed in-place
                data = np.append(data, new_data, axis=-1)
                weights = np.append(weights, old_weights)

        # Re-normalize the weights
        weights = weights / np.sum(weights)
        return data, weights, bounds

    def _truncate_reflections(self, data, weights, bounds):
        # Determine the bounds outside of which we should truncate
        trunc = self._get_truncation_bounds(bounds)
        # Find the data-points outside of those bounds
        idx = utils.bound_indices(data, trunc)
        # Select only points within truncation bounds
        data = data[:, idx]
        weights = weights[idx]
        weights /= np.sum(weights)
        return data, weights

    def _get_truncation_bounds(self, bounds):
        trunc = np.zeros_like(bounds)

        bw = self.bandwidth.diagonal()
        # If this kernel has finite-support, we only need to go out to 'bandwidth' on each side
        if self.FINITE:
            bw = bw * (1 + _NUM_PAD)
            qnts = np.array([-bw, bw]).T
        # If kernel has infinite-support, go to the quantile reaching the desired precision
        else:
            tol = _TRUNCATE_INFINITE_KERNELS
            qnts = self.distribution.ppf([tol, 1-tol])
            qnts = qnts[np.newaxis, :] * bw[:, np.newaxis]

        # Expand the reflection bounds based on the bandwidth interval
        trunc = bounds + qnts
        return trunc

    def _check_reflect(self, reflect, ndim, data, weights):
        if reflect is None:
            return reflect

        if ndim == 1 and np.ndim(reflect) == 1:
            reflect = np.atleast_2d(reflect)

        if len(reflect) != ndim:
            msg = "`reflect` ({}) must have length (D,) = ({},)!".format(
                len(reflect), ndim)
            raise ValueError(msg)

        if not np.all([(ref is None) or len(ref) == 2 for ref in reflect]):
            raise ValueError("each row of `reflect` must be `None` or shape (2,)!")

        # Perform additional diagnostics
        for ii in range(ndim):
            if np.all(np.array(reflect[ii]) != None) and (reflect[ii][0] >= reflect[ii][1]): # noqa
                err = "Reflect has inverted order:  `reflect`[{}] = {}  !".format(ii, reflect[ii])
                raise ValueError(err)

            if self._helper:

                # Warn if any datapoints are outside of reflection bounds
                bads = utils.bound_indices(data[ii, :], reflect[ii], outside=True)
                if np.any(bads):
                    frac = np.sum(weights[bads]) / np.sum(weights)
                    msg = ("A fraction {:.2e} of data[{}] ".format(frac, ii) +
                           " are outside of `reflect` bounds!")
                    logging.warning(msg)
                    msg = (
                        "`reflect[{}]` = {}; ".format(ii, reflect[ii]) +
                        "`data[{}]` = {}".format(ii, utils.stats_str(data[ii], weights=weights))
                    )
                    logging.warning(msg)
                    logging.warning("I hope you know what you're doing.")

                # Warn if bandwidth is comparable to area in-bounds
                if np.all(np.array(reflect[ii]) != None):   # noqa
                    width = np.diff(reflect[ii])[0]
                    bw = np.sqrt(self.matrix[ii, ii])
                    rat = width / bw
                    thresh = 1.0 if self.FINITE else 2.0
                    if rat < thresh:
                        msg = (
                            "The bandwidth[{}] = {:.2e} is comparable ".format(ii, bw) +
                            "to the area within reflect = {:.2e}!".format(width)
                        )
                        logging.warning(msg)
                        msg = ""
                        if not self.FINITE:
                            msg += "consider using a kernel with finite-support, or "
                        msg += "consider setting `keep={}`".format(ii)
                        logging.warning(msg.capitalize())

        return reflect

    @classmethod
    def _cov_keep_vars(cls, matrix, keep, reflect=None):
        matrix = np.array(matrix)
        if (keep is None) or (keep is False):
            return matrix

        if keep is True:
            keep = np.arange(matrix.shape[0])

        keep = np.atleast_1d(keep)
        for pp in keep:
            matrix[pp, :] = 0.0
            matrix[:, pp] = 0.0
            # Make sure this isn't also a reflection axis
            if (reflect is not None) and (reflect[pp] is not None):
                err = "Cannot both 'keep' and 'reflect' about dimension '{}'".format(pp)
                raise ValueError(err)

        return matrix

    @classmethod
    def _params_subset(cls, data, matrix, params):
        if params is None:
            raise ValueError("Why is this method being called if `params` are 'None'?")
            # norm = np.sqrt(np.linalg.det(matrix))
            # return data, matrix, norm

        params = np.atleast_1d(params)
        # NOTE/WARNING: don't sort parameters (Changed 2020-04-07)
        # params = sorted(params)
        # Get rows corresponding to these parameters
        # sub_pnts = pnts[params, :]
        sub_data = data[params, :]
        # Get rows & cols corresponding to these parameters
        sub_mat = matrix[np.ix_(params, params)]
        # Recalculate norm
        norm = np.sqrt(np.linalg.det(sub_mat))
        return params, sub_data, sub_mat, norm

    # ==== Properties ====

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def covariance(self):
        return self._covariance

    @property
    def distribution(self):
        return self._distribution

    @property
    def matrix(self):
        return self._matrix

    @property
    def matrix_inv(self):
        try:
            if self._matrix_inv is None:
                raise AttributeError
        except AttributeError:
            self._matrix_inv = utils.matrix_invert(self.matrix, helper=self._helper)
        return self._matrix_inv

    @property
    def norm(self):
        try:
            if self._norm is None:
                raise AttributeError
        except AttributeError:
            self._norm = np.sqrt(np.fabs(np.linalg.det(self.matrix)))

        return self._norm

    @property
    def FINITE(self):
        return self.distribution.FINITE


class Distribution(object):
    """

    `Distribution` positional arguments (`xx` or `yy`) must be shaped as `(D, N)`
    for 'D' dimensions and 'N' data-points.

    """

    _FINITE = None
    _SYMMETRIC = True
    _CDF_INTERP = True
    _INTERP_KWARGS = dict(kind='cubic', fill_value=np.nan)

    def __init__(self):
        self._cdf_grid = None
        self._cdf_func = None
        self._ppf_func = None
        return

    @classmethod
    def name(cls):
        name = cls.__name__
        return name

    @classmethod
    def _parse(cls, xx):
        squeeze = (np.ndim(xx) < 2)
        xx = np.atleast_2d(xx)
        ndim, nval = np.shape(xx)
        return xx, ndim, squeeze

    @classmethod
    def evaluate(cls, xx):
        yy, ndim, squeeze = cls._parse(xx)
        zz = cls._evaluate(yy, ndim)
        if squeeze:
            zz = zz.squeeze()
        return zz

    @classmethod
    def _evaluate(cls, yy, ndim):
        err = "`_evaluate` must be overridden by the Distribution subclass!"
        raise NotImplementedError(err)

    @classmethod
    def grid(cls, edges, **kwargs):
        coords = np.meshgrid(*edges, indexing='ij')
        shp = np.shape(coords)[1:]
        coords = np.vstack([xx.ravel() for xx in coords])
        pdf = cls.evaluate(coords, **kwargs)
        pdf = pdf.reshape(shp)
        return pdf

    def sample(self, size, ndim=None, squeeze=None):
        if ndim is None:
            ndim = 1
            if squeeze is None:
                squeeze = True

        if squeeze is None:
            squeeze = (ndim == 1)

        samps = self._sample(size, ndim)
        if squeeze:
            samps = samps.squeeze()
        return samps

    def _sample(self, size, ndim):
        grid, cdf = self.cdf_grid
        samps = np.random.uniform(0.0, 1.0, ndim*size)
        samps = sp.interpolate.interp1d(cdf, grid, kind='quadratic')(samps).reshape(ndim, size)
        return samps

    def cdf(self, xx):
        if self._cdf_func is None:
            self._cdf_func = sp.interpolate.interp1d(
                *self.cdf_grid, fill_value=(0.0, 1.0), **self._INTERP_KWARGS)

        zz = self._cdf_func(xx)
        return zz

    def ppf(self, cd):
        """Percentile Point Function - the inverse of the cumulative distribution function.

        NOTE: for symmetric kernels, this (effectively) uses points only with cdf in [0.0, 0.5],
        which produces better numerical results (unclear why).

        """
        if self._ppf_func is None:
            x0, y0 = self.cdf_grid
            self._ppf_func = sp.interpolate.interp1d(
                y0, x0, kind='cubic', fill_value='extrapolate')  # **self._INTERP_KWARGS)

        # Symmetry can be utilized to get better accuracy of results, see 'note' above
        if self.SYMMETRIC:
            cd = np.atleast_1d(cd)
            idx = (cd > 0.5)
            cd = np.copy(cd)
            cd[idx] = 1 - cd[idx]

        try:
            xx = self._ppf_func(cd)
        except ValueError:
            logging.error("`_ppf_func` failed!")
            logging.error("input `cd` = {}  <===  {}".format(
                utils.stats_str(cd), utils.array_str(cd)))
            for vv in self.cdf_grid:
                logging.error("\tcdf_grid: {} <== {}".format(
                    utils.stats_str(vv), utils.array_str(vv)))
            raise

        if self.SYMMETRIC:
            xx[idx] = -xx[idx]

        return xx

    @property
    def cdf_grid(self):
        if self._cdf_grid is None:
            if self._FINITE:
                pad = (1 + _NUM_PAD)
                args = [-pad, pad]
            else:
                args = [-6, 6]

            num = np.diff(args)[0] * _INTERP_NUM_PER_STD
            args = args + [int(num), ]

            xc = np.linspace(*args)
            if self._CDF_INTERP:
                yy = self.evaluate(xc)
                csum = utils.cumtrapz(yy, xc, prepend=False)
            else:
                csum = self.cdf(xc)

            norm = csum[-1]
            if not np.isclose(norm, 1.0, rtol=1e-5):
                err = "Failed to reach unitarity in CDF grid norm: {:.4e}!".format(norm)
                raise ValueError(err)

            # csum = csum / norm
            # xc = np.concatenate([[args[0]], [args[0]], xc, [args[1]], [args[1]]], axis=0)
            # csum = np.concatenate([[0.0 - _NUM_PAD], [0.0], csum, [1.0], [1.0+_NUM_PAD]], axis=0)
            self._cdf_grid = [xc, csum]

        return self._cdf_grid

    @property
    def FINITE(self):
        return self._FINITE

    @property
    def SYMMETRIC(self):
        return self._SYMMETRIC

    @classmethod
    def inside(cls, pnts):
        idx = (cls.evaluate(pnts) > 0.0)
        return idx


class Gaussian(Distribution):

    _FINITE = False
    _CDF_INTERP = False

    @classmethod
    def _evaluate(self, yy, ndim):
        energy = np.sum(yy * yy, axis=0) / 2.0
        norm = self.norm(ndim)
        result = np.exp(-energy) / norm
        return result

    @classmethod
    def norm(self, ndim=1):
        norm = np.power(2*np.pi, ndim/2)
        return norm

    def cdf(self, yy):
        zz = sp.stats.norm.cdf(yy)
        return zz

    def _sample(self, size, ndim):
        cov = np.eye(ndim)
        samps = np.random.multivariate_normal(np.zeros(ndim), cov, size=size).T
        return samps

    @classmethod
    def inside(cls, pnts):
        ndim, nvals = np.shape(np.atleast_2d(pnts))
        return np.ones(nvals, dtype=bool)


class Box_Asym(Distribution):

    _FINITE = True
    _CDF_INTERP = False

    @classmethod
    def _evaluate(self, yy, ndim):
        norm = np.power(2, ndim)
        zz = (np.max(np.fabs(yy), axis=0) < 1.0) / norm
        return zz

    @classmethod
    def _sample(self, size, ndim):
        samps = np.random.uniform(-1.0, 1.0, size=ndim*size).reshape(ndim, size)
        return samps

    @classmethod
    def cdf(self, xx):
        zz = 0.5 + np.minimum(np.maximum(xx, -1), 1)/2
        return zz

    @classmethod
    def inside(cls, pnts):
        pnts = np.atleast_2d(pnts)
        ndim, nvals = np.shape(pnts)
        bounds = [[-1.0, 1.0] for ii in range(ndim)]
        idx = utils.bound_indices(pnts, bounds)
        return idx


class Parabola(Distribution):

    _FINITE = True
    _CDF_INTERP = False

    @classmethod
    def _evaluate(self, yy, ndim):
        norm = 2 * _nball_vol(ndim) / (ndim + 2)
        dist = np.sum(yy**2, axis=0)
        zz = np.maximum(1 - dist, 0.0) / norm
        # zz = np.product(np.maximum(1 - yy**2, 0.0), axis=0) / norm
        return zz

    def _sample(self, size, ndim):
        # Use the median trick to draw from the Epanechnikov distribution
        samp = np.random.uniform(-1, 1, 3*ndim*size).reshape(ndim, size, 3)
        samp = np.median(samp, axis=-1)
        return samp

    @classmethod
    def cdf(self, xx):
        xx = np.minimum(np.maximum(xx, -1), 1)
        zz = 0.5 + (3/4)*(xx - xx**3 / 3)
        return zz


'''
NOTE: THIS ISN"T WORKING!  NON-UNITARY for ND > 1.  Something wrong with normalization?  NBall?

class Triweight(Distribution):

    _FINITE = True
    _CDF_INTERP = False

    @classmethod
    def _evaluate(self, yy, ndim):
        norm = (32.0 / 35.0) * _nball_vol(ndim) / (ndim + 1)
        dist = np.sum(yy**2, axis=0)
        # dist = np.linalg.norm(yy, 2, axis=0) ** 2
        zz = np.maximum((1 - dist)**3, 0.0)
        # zz = np.product(np.maximum((1 - yy*yy)**3, 0.0), axis=0)
        zz = zz / norm
        return zz

    @classmethod
    def cdf(self, xx):
        yy = np.minimum(np.maximum(xx, -1), 1)
        coeffs = [35/32, -35/32, 21/32, -5/32]
        powers = [1, 3, 5, 7]
        zz = 0.5 + np.sum([aa*np.power(yy, pp) for aa, pp in zip(coeffs, powers)], axis=0)
        return zz
'''


_DEFAULT_DISTRIBUTION = Gaussian

_index_list = [
    ['gaussian', Gaussian],
    ['box', Box_Asym],
    ['parabola', Parabola],
    ['epanechnikov', Parabola],
    # ['triweight', Triweight],
]

_all_skip = []
# _all_skip = [Triweight]

_index = OrderedDict([(nam, val) for nam, val in _index_list])


def get_distribution_class(arg=None):
    if arg is None:
        return _DEFAULT_DISTRIBUTION

    if isinstance(arg, six.string_types):
        arg = arg.lower().strip()
        names = list(_index.keys())
        if arg not in names:
            err = "`Distribution` '{}' is not in the index.  Choose one of: '{}'!".format(
                arg, names)
            raise ValueError(err)

        return _index[arg]

    # This will raise an error if `arg` isn't a class at all
    try:
        if issubclass(arg, Distribution):
            return arg
    except:
        pass

    raise ValueError("Unrecognized `Distribution` type '{}'!".format(arg))


def get_all_distribution_classes():
    kerns = []
    for kk in _index.values():
        if kk not in kerns:
            if kk in _all_skip:
                logging.warning("WARNING: skipping `Distribution` '{}'!".format(kk))
                continue
            kerns.append(kk)
    return kerns


def _nball_vol(ndim, rad=1.0):
    vol = np.pi**(ndim/2)
    vol = (rad**ndim) * vol / sp.special.gamma((ndim/2) + 1)
    return vol
