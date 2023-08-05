# -*- coding: utf-8 -*-
# Copyright (c) 2020 Stephen Wasilewski
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""dat parsing and statistical analysis."""
from scipy import stats
import numpy as np
import sys

from hdrstats import __version__


def corr_header(lin=True, spearman=False, pearson=False, pvals=True, **kwargs):
    """generate headers for corr_calc"""
    out = []
    if lin:
        out += ['r^2', 'p']
    if spearman:
        out += ['spearman_rho', 'spearman_pval']
    if pearson:
        out += ['pearson_rho', 'pearson_pval']
    if pvals:
        return out
    else:
        return out[0::2]


def corr_calc(x, y, lin=True, spearman=False, pearson=False, pvals=True,
              **kwargs):
    """calculate correlations between pairs of data"""
    out = []
    if lin:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        out += [r_value**2, p_value]
    if spearman:
        rho, pval2 = stats.spearmanr(x,y)
        out += [rho, pval2]
    if pearson:
        rho, pval2 = stats.pearsonr(x,y)
        out += [rho**2, pval2]
    # if rbc:
    #     T, p = stats.wilcoxon(x, y)
    #     rbc = abs(2*(T/sum(range(len(y)+1))-.5))
    #     out += [rbc, p]
    if pvals:
        return out
    else:
        return out[0::2]


def g_err(a, b, c, sigma, scale=1.0, conf=.95):
    """apply kernel density estimate from b to c at a"""
    n = stats.norm(loc=a, scale=sigma)
    weights = n.pdf(b)
    if np.sum(weights) > 1e-8:
        mu = np.average(c, weights=weights)
        sigma2 = np.sqrt(np.average(np.square(c - mu), weights=weights))
        interval = stats.norm.interval(conf, loc=mu, scale=sigma2)
        ssize = np.sum(weights)*scale*len(b)/np.sum(b)
        err = (interval[1]- interval[0])/(2*np.sqrt(ssize))
    else:
        mu = 0
        ssize = 0
        err = 1
        print(f'KD is insufficient at {a}', file=sys.stderr)
    return mu, mu - err, mu + err, ssize


def g_ssize(a, b, sigma):
    n = stats.norm(loc=a, scale=sigma)
    ssize = np.sum(n.pdf(b))*len(b)/np.sum(b)
    return ssize


def kde_cont(b, resample=None):
    sigma = np.sqrt(np.cov(b)*len(b)**(-.4))
    if resample is None:
        samples = b.reshape(-1, 1)
    else:
        samples = np.asarray(resample).reshape(-1, 1)
    ssize = np.apply_along_axis(g_ssize, 1, samples, b, sigma)
    return np.vstack((samples.flatten(), ssize)).T

def error_cont(b, adif, rdif, scale=1, resample=None):
    """calculate continuous moving average of error (adif, rdif)
    based on the kernel density estimate of b, at b or if resample, at resample
    """
    # gaussian kernel selection by Scott's rule, see:
    # https://docs.scipy.org/doc/scipy/reference/generated/
    # scipy.stats.gaussian_kde.html
    sigma = np.sqrt(np.cov(b)*len(b)**(-.4))
    print(sigma)
    if resample is None:
        samples = b.reshape(-1, 1)
    else:
        samples = np.asarray(resample).reshape(-1, 1)
    MSD = np.apply_along_axis(g_err, 1, samples, b, rdif, sigma, scale)
    MAD = np.apply_along_axis(g_err, 1, samples, b, adif, sigma, scale)
    i = samples.flatten()
    result = np.stack((i, MAD[:,0], np.maximum(MAD[:,1], 0), MAD[:,2],
                          MSD[:,0], MSD[:,1], MSD[:,2], MSD[:,3])).T
    return result
