# -*- coding: utf-8 -*-
"""
@author: Anthony Soulain (University of Sydney)

--------------------------------------------------------------------
PREVIS: Python Request Engine for Virtual Interferometric Survey
--------------------------------------------------------------------

This file contains function to check the star observability with
each VLTI and CHARA instruments. The limiting magnitudes are extracted
from the ESO website or the CHARA website. In the case of MATISSE,
the limiting magnitude can be extracted automaticaly from the actual
performances (P106, 2020) or estimated performances (2017). Some mode
of MATISSE are not yet commissioned (UT with GRA4MAT), so only 
estimated performances are used.
"""

import os
import pickle
import urllib.request

import numpy as np
import pandas as pd

import previs

templates_dir = os.path.join(os.path.dirname(previs.__file__), 'files')

dirname = (previs.__file__.split('__init__'))[0]


def MagToJy(m, band, reverse=False):
    """
    Convert Johnson magnitudes into Jy.

    Parameters:
    -----------
        m (float):
            Johnson magnitude,
        band (str):
            Photometric band name (B, V, R, L, etc.).

    Returns:
    --------
        F (float):
            Converted flux in Jy unit.
    """

    conv_flux = {'B': {'wl': 0.44, 'F0': 4260},
                 # Allen's astrophysical quantities
                 'V': {'wl': 0.5556, 'F0': 3540},
                 'R': {'wl': 0.64, 'F0': 3080},
                 'I': {'wl': 0.79, 'F0': 2550},
                 'J': {'wl': 1.215, 'F0': 1630},
                 'H': {'wl': 1.654, 'F0': 1050},
                 'K': {'wl': 2.179, 'F0': 655},
                 'L': {'wl': 3.547, 'F0': 276},
                 'M': {'wl': 4.769, 'F0': 160},
                 # 10.2, 42.7 Johnson N (https://www.gemini.edu/?q=node/11119)
                 'N': {'wl': 10.2, 'F0': 42.7},
                 'Q': {'wl': 20.13, 'F0': 9.7}
                 }

    if not reverse:
        try:
            F0 = conv_flux[band]['F0']
            out = F0 * (10**(m / -2.5))
        except:
            out = np.nan
    else:
        out = -2.5*np.log10(m/conv_flux[band]['F0'])

    return out


def limit_ESO_matisse_web(check):
    """ Extract limiting flux (Jy) from ESO MATISSE instrument descriptions and
    return magnitude (optimal 10% seeing conditions). """
    link = 'http://www.eso.org/sci/facilities/paranal/instruments/matisse/inst.html'

    if check:
        print('Check MATISSE limits from ESO web site...')
        url = link
        tables = pd.read_html(url)  # Returns list of all tables on page
        limit_MATISSE_abs = tables[4]  # Select table of interest
        limit_MATISSE_rel = tables[5]
        limit_MATISSE_gra4mat = tables[6]

        list_limit_abs = np.array(limit_MATISSE_abs)
        list_limit_rel = np.array(limit_MATISSE_rel)
        list_limit_gra4mat = np.array(limit_MATISSE_gra4mat)

        at_lim_good = np.array([x.split('Jy')[0]
                                for x in list_limit_abs[:, 1]]).astype(float)
        at_lim_mid = np.array([x.split('Jy')[0]
                               for x in list_limit_abs[:, 2]]).astype(float)
        ut_lim_good = np.array([x.split('Jy')[0]
                                for x in list_limit_abs[:, 3]]).astype(float)
        ut_lim_mid = np.array([x.split('Jy')[0]
                               for x in list_limit_abs[:, 4]]).astype(float)

        at_lim_good_rel = np.array([x.split('Jy')[0]
                                    for x in list_limit_rel[:, 1]]).astype(float)
        ut_lim_good_rel = np.array([x.split('Jy')[0]
                                    for x in list_limit_rel[:, 3]]).astype(float)

        at_L_gra4mat = np.array([x.split('Jy')[0]
                                 for x in list_limit_gra4mat[1:, 1]])
        at_M_gra4mat = np.array([x.split('Jy')[0]
                                 for x in list_limit_gra4mat[1:, 3]])

        at_noft_L = MagToJy(np.array(
            [at_lim_good[0], at_lim_good[2], at_lim_good_rel[3]]), 'L', reverse=True)
        at_noft_M = MagToJy(
            np.array([at_lim_good[1], at_lim_good_rel[2]]), 'M', reverse=True)
        at_noft_N = MagToJy(
            np.array([at_lim_good[4], at_lim_good_rel[4]]), 'N', reverse=True)

        ut_noft_L = MagToJy(np.array(
            [ut_lim_good[0], ut_lim_good_rel[1], ut_lim_good_rel[3]]), 'L', reverse=True)
        ut_noft_M = MagToJy(
            np.array([ut_lim_good[1], ut_lim_good_rel[2]]), 'M', reverse=True)
        ut_noft_N = MagToJy(
            np.array([ut_lim_good[4], ut_lim_good_rel[4]]), 'N', reverse=True)

        at_ft_L = MagToJy(np.array([at_L_gra4mat[0], at_L_gra4mat[1],
                                    at_L_gra4mat[2]]).astype(float), 'L', reverse=True)
        at_ft_M = MagToJy(np.array([at_M_gra4mat[0], at_M_gra4mat[1]]).astype(float),
                          'M', reverse=True)
        at_ft_N = []  # not commisionned (see estimated performance)

        dic_web = {'at': {'noft': {'L': at_noft_L, 'M': at_noft_M, 'N': at_noft_N, },
                          'ft': {'L': at_ft_L, 'M': at_ft_M, 'N': at_ft_N}
                          },
                   'ut': {'noft': {'L': ut_noft_L, 'M': ut_noft_M, 'N': ut_noft_N, },
                          'ft': {'L': [], 'M': [], 'N': []}
                          }
                   }
        file = open(dirname + 'files/eso_limits_matisse.dpy', 'wb')
        pickle.dump(dic_web, file, 2)
        file.close()
    else:
        file = open(dirname + 'files/eso_limits_matisse.dpy', 'rb')
        dic_web = pickle.load(file)
        file.close()

    return dic_web


def limit_commissioning_matisse():
    """ Estimated performance of MATISSE during testing and 
    commissioning.
    """
    at_noft_L = [4.2, 0.9, -1.5]
    at_noft_M = [3.24, 1]
    at_noft_N = [-0.35, -2.2]
    at_ft_L = [7.7, 6.1, 4.2]
    at_ft_M = [5.24, 1.6]
    at_ft_N = [1.6, 0.1]
    ut_noft_L = [7, 3.7, 1.3]
    ut_noft_M = [6.03, 3.83]
    ut_noft_N = [2.7, 0.8]
    ut_ft_L = [10.3, 8.8, 6.9]
    ut_ft_M = [5, 5]
    ut_ft_N = [4.6, 3.2]

    dic_consortium = {'at': {'noft': {'L': at_noft_L, 'M': at_noft_M, 'N': at_noft_N, },
                             'ft': {'L': at_ft_L, 'M': at_ft_M, 'N': at_ft_N}
                             },
                      'ut': {'noft': {'L': ut_noft_L, 'M': ut_noft_M, 'N': ut_noft_N, },
                             'ft': {'L': ut_ft_L, 'M': ut_ft_M, 'N': ut_ft_N}
                             }
                      }
    return dic_consortium


def gravity_limit(magV, magK):
    """
    Return observability with GRAVITY instrument.
    """
    dic = {'UT': {'K': {'MR': False, 'HR': False}},
           'AT': {'K': {'MR': False, 'HR': False}}}
    if (magV <= 11):
        dic['V_cond'] = 'AT'
    elif (magV > 11) & (magV <= 16):
        dic['V_cond'] = 'UT'
    else:
        dic['V_cond'] = 'TooFaint'

    if (magK >= -4.) & (magK <= -1):
        dic['UT']['K'] = {'MR': False, 'HR': False}
        dic['AT']['K'] = {'MR': False, 'HR': True}
    elif (magK > -1) & (magK <= 1):
        dic['UT']['K'] = {'MR': False, 'HR': False}
        dic['AT']['K'] = {'MR': True, 'HR': True}
    elif (magK > 1) & (magK <= 4):
        dic['UT']['K'] = {'MR': False, 'HR': True}
        dic['AT']['K'] = {'MR': True, 'HR': True}
    elif (magK > 4) & (magK <= 8):
        dic['UT']['K'] = {'MR': True, 'HR': True}
        dic['AT']['K'] = {'MR': True, 'HR': True}
    elif (magK > 8) & (magK <= 9):
        dic['UT']['K'] = {'MR': True, 'HR': True}
        dic['AT']['K'] = {'MR': False, 'HR': False}
    else:
        dic['UT']['K'] = {'MR': False, 'HR': False}
        dic['AT']['K'] = {'MR': False, 'HR': False}

    return dic


def matisse_limit(magL, magM, magN, magK, source='ESO', check=True):
    """
    Return observability with MATISSE instrument with different configurations (Spectral
    resolution, UTs or ATs, Fringe tracking, etc...).

    Parameters:
    -----------

    magL {float} : L-band magnitude (3.5micron).
    """
    dic = {}
    dic['AT'] = {'ft': {'L': {'LR': False}, 'M': {'LR': False}, 'N': {'LR': False}}, 'noft': {'L': {
        'LR': False, 'MR': False, 'HR': False}, 'M': {'LR': False, 'HR': False}, 'N': {'LR': False, 'HR': False}}}
    dic['UT'] = {'ft': {'L': {'LR': False}, 'M': {'LR': False}, 'N': {'LR': False}}, 'noft': {'L': {
        'LR': False, 'MR': False, 'HR': False}, 'M': {'LR': False, 'HR': False}, 'N': {'LR': False, 'HR': False}}}
    dic['limK'] = {'UT': False, 'AT': False}

    if source == 'ESO':
        dic_limit = limit_ESO_matisse_web(check=check)
        dic_eso = dic_limit
    else:
        dic_limit = limit_commissioning_matisse()

    dic_matisse = limit_commissioning_matisse()

    # Frange tracker K band limit
    if (magK <= 7.5):
        dic['limK']['UT'] = True
        dic['limK']['AT'] = True
    elif (magK > 7.5) & (magK <= 10.):
        dic['limK']['UT'] = True
        dic['limK']['AT'] = False
    else:
        dic['limK']['UT'] = False
        dic['limK']['AT'] = False

    # --------------------------------------------------------------------
    # UT, ft
    lim = dic_matisse['ut']['ft']['L']
    if (magL <= lim[2]):
        dic['UT']['ft']['L']['LR'] = True
        dic['UT']['ft']['L']['MR'] = True
        dic['UT']['ft']['L']['HR'] = True
    elif (magL > lim[2]) & (magL <= lim[1]):
        dic['UT']['ft']['L']['LR'] = True
        dic['UT']['ft']['L']['MR'] = True
        dic['UT']['ft']['L']['HR'] = False
    elif (magL > lim[1]) & (magL <= lim[0]):
        dic['UT']['ft']['L']['LR'] = True
        dic['UT']['ft']['L']['MR'] = False
        dic['UT']['ft']['L']['HR'] = False
    else:
        dic['UT']['ft']['L']['LR'] = False
        dic['UT']['ft']['L']['MR'] = False
        dic['UT']['ft']['L']['HR'] = False

    lim = dic_limit['ut']['ft']['M']
    if len(lim) == 0:
        #print('Not commisionned yet (M): use estimated sensitivity.')
        lim = limit_commissioning_matisse()['ut']['ft']['M']

    if (magM <= lim[0]):
        dic['UT']['ft']['M']['LR'] = True
        dic['UT']['ft']['M']['HR'] = True
    else:
        dic['UT']['ft']['M']['LR'] = False
        dic['UT']['ft']['M']['HR'] = False

    lim = dic_limit['ut']['ft']['N']
    if len(lim) == 0:
        #print('Not commisionned yet (N): use estimated sensitivity.')
        lim = limit_commissioning_matisse()['ut']['ft']['N']
    if (magN <= lim[1]):
        dic['UT']['ft']['N']['LR'] = True
        dic['UT']['ft']['N']['HR'] = True
    elif (magN > lim[1]) & (magN <= lim[0]):
        dic['UT']['ft']['N']['LR'] = True
        dic['UT']['ft']['N']['HR'] = False
    else:
        dic['UT']['ft']['N']['LR'] = False
        dic['UT']['ft']['N']['HR'] = False

    # --------------------------------------------------------------------
    # UT, noft
    lim = dic_limit['ut']['noft']['L']
    if (magL <= lim[2]):
        dic['UT']['noft']['L']['LR'] = True
        dic['UT']['noft']['L']['MR'] = True
        dic['UT']['noft']['L']['HR'] = True
    elif (magL > lim[2]) & (magL <= lim[1]):
        dic['UT']['noft']['L']['LR'] = True
        dic['UT']['noft']['L']['MR'] = True
        dic['UT']['noft']['L']['HR'] = False
    elif (magL > lim[1]) & (magL <= lim[0]):
        dic['UT']['noft']['L']['LR'] = True
        dic['UT']['noft']['L']['MR'] = False
        dic['UT']['noft']['L']['HR'] = False
    else:
        dic['UT']['noft']['L']['LR'] = False
        dic['UT']['noft']['L']['MR'] = False
        dic['UT']['noft']['L']['HR'] = False

    lim = dic_limit['ut']['noft']['M']
    if (magM <= lim[1]):
        dic['UT']['noft']['M']['LR'] = True
        dic['UT']['noft']['M']['HR'] = True
    elif (magM > lim[1]) & (magM <= lim[0]):
        dic['UT']['noft']['M']['LR'] = True
        dic['UT']['noft']['M']['HR'] = False
    else:
        dic['UT']['noft']['M']['LR'] = False
        dic['UT']['noft']['M']['HR'] = False

    lim = dic_limit['ut']['noft']['N']
    if (magN <= lim[1]):
        dic['UT']['noft']['N']['LR'] = True
        dic['UT']['noft']['N']['HR'] = True
    elif (magN > lim[1]) & (magN <= lim[0]):
        dic['UT']['noft']['N']['LR'] = True
        dic['UT']['noft']['N']['HR'] = False
    else:
        dic['UT']['noft']['N']['LR'] = False
        dic['UT']['noft']['N']['HR'] = False

    # AT, ft
    lim = dic_limit['at']['ft']['L']
    if (magL <= lim[2]):
        dic['AT']['ft']['L']['LR'] = True
        dic['AT']['ft']['L']['MR'] = True
        dic['AT']['ft']['L']['HR'] = True
    elif (magL > lim[2]) & (magL <= lim[1]):
        dic['AT']['ft']['L']['LR'] = True
        dic['AT']['ft']['L']['MR'] = True
        dic['AT']['ft']['L']['HR'] = False
    elif (magL > lim[1]) & (magL <= lim[0]):
        dic['AT']['ft']['L']['LR'] = True
        dic['AT']['ft']['L']['MR'] = False
        dic['AT']['ft']['L']['HR'] = False
    else:
        dic['AT']['ft']['L']['LR'] = False
        dic['AT']['ft']['L']['MR'] = False
        dic['AT']['ft']['L']['HR'] = False

    lim = dic_limit['at']['ft']['M']
    if (magM <= lim[1]):
        dic['AT']['ft']['M']['LR'] = True
        dic['AT']['ft']['M']['HR'] = True
    elif (magM > lim[1]) & (magM <= lim[0]):
        dic['AT']['ft']['M']['LR'] = True
        dic['AT']['ft']['M']['HR'] = False
    else:
        dic['AT']['ft']['M']['LR'] = False
        dic['AT']['ft']['M']['HR'] = False

    lim = dic_limit['at']['ft']['N']
    if len(lim) == 0:
        #print('Not commisionned yet (ft/N): use estimated sensitivity.')
        lim = limit_commissioning_matisse()['at']['ft']['N']
    if (magN <= lim[1]):
        dic['AT']['ft']['N']['LR'] = True
        dic['AT']['ft']['N']['HR'] = True
    elif (magN > lim[1]) & (magN <= lim[0]):
        dic['AT']['ft']['N']['LR'] = True
        dic['AT']['ft']['N']['HR'] = False
    else:
        dic['AT']['ft']['N']['LR'] = False
        dic['AT']['ft']['N']['HR'] = False

    # AT, noft
    lim = dic_limit['at']['noft']['L']
    if (magL <= lim[2]):
        dic['AT']['noft']['L']['LR'] = True
        dic['AT']['noft']['L']['MR'] = True
        dic['AT']['noft']['L']['HR'] = True
    elif (magL > lim[2]) & (magL <= lim[1]):
        dic['AT']['noft']['L']['LR'] = True
        dic['AT']['noft']['L']['MR'] = True
        dic['AT']['noft']['L']['HR'] = False
    elif (magL > lim[1]) & (magL <= lim[0]):
        dic['AT']['noft']['L']['LR'] = True
        dic['AT']['noft']['L']['MR'] = False
        dic['AT']['noft']['L']['HR'] = False
    else:
        dic['AT']['noft']['L']['LR'] = False
        dic['AT']['noft']['L']['MR'] = False
        dic['AT']['noft']['L']['HR'] = False

    lim = dic_limit['at']['noft']['M']
    if (magM <= lim[1]):
        dic['AT']['noft']['M']['LR'] = True
        dic['AT']['noft']['M']['HR'] = True
    elif (magM > lim[1]) & (magM <= lim[0]):
        dic['AT']['noft']['M']['LR'] = True
        dic['AT']['noft']['M']['HR'] = False
    else:
        dic['AT']['noft']['M']['LR'] = False
        dic['AT']['noft']['M']['HR'] = False

    lim = dic_limit['at']['noft']['N']
    if (magN <= lim[1]):
        dic['AT']['noft']['N']['LR'] = True
        dic['AT']['noft']['N']['HR'] = True
    elif (magN > lim[1]) & (magN <= lim[0]):
        dic['AT']['noft']['N']['LR'] = True
        dic['AT']['noft']['N']['HR'] = False
    else:
        dic['AT']['noft']['N']['LR'] = False
        dic['AT']['noft']['N']['HR'] = False

    return dic


def pionier_limit(magH, magV):
    """ Return observability with PIONIER instrument."""
    dic = {}
    if (magH >= -1.) & (magH <= 9.):
        dic['H'] = True
    else:
        dic['H'] = False
    return dic


def chara_limit(magK, magH, magR, magV):
    """ Return observability of the different instruments of CHARA."""
    dic = {}
    dic['PAVO'] = {'R': 0}
    dic['CLASSIC'] = {'K': 0, 'H': 0, 'V': 0}
    dic['CLIMB'] = {'K': 0}
    dic['MIRC'] = {'H': 0, 'K': 0}
    dic['MYSTIC'] = {'K': 0}
    dic['VEGA'] = {'LR': 0, 'MR': 0, 'HR': 0}

    if np.min([magV, magR]) <= 10:
        dic['Guiding'] = True
    else:
        dic['Guiding'] = False

    # CLASSIC
    dic['CLASSIC']['K'] = (magK <= 6.5)
    dic['CLASSIC']['H'] = (magH <= 7)
    dic['CLASSIC']['V'] = (magV <= 10)

    # CLIMB
    dic['CLIMB']['K'] = (magK <= 6.)

    # PAVO
    dic['PAVO']['R'] = (magR <= 7.)

    # MIRC
    dic['MIRC']['H'] = (magH <= 6.5)
    dic['MIRC']['K'] = (magK <= 3)

    dic['MYSTIC']['K'] = (magK <= 6)

    # VEGA
    dic['VEGA']['HR'] = (magV <= 4.2)
    dic['VEGA']['MR'] = (magV <= 5.8)
    dic['VEGA']['LR'] = (magV <= 7.2)
    return dic