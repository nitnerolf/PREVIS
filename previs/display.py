# -*- coding: utf-8 -*-
"""
@author: Anthony Soulain (University of Sydney)

--------------------------------------------------------------------
PREVIS: Python Request Engine for Virtual Interferometric Survey
--------------------------------------------------------------------

This file contains function use to plot, print and count the results
from previs.core function.
"""

import matplotlib.pyplot as plt
import numpy as np
from termcolor import cprint

color = {'True': 'g', 'False': '#e23449'}

plt.close('all')


def plot_mat(data, inst, tel, ft, band, x0, y0, off):
    """ Plot observability with MATISSE given spectral resolution:
        low (LR: 34/L and 30/N), medium (MR: 506/L and no N) and 
        high (HR: 959/L and 218/N) resolution."""
    ins = data['Ins']
    if inst == 'MATISSE':
        try:
            if (ins['MATISSE'][tel][ft][band]['LR'] & data['Observability']['VLTI']):
                c_L = True
            else:
                c_L = False
            plt.scatter(
                x0, y0, 100, color=color[str(c_L)], edgecolors='#364f6b')
        except:
            pass
        try:
            if (ins['MATISSE'][tel][ft][band]['MR'] & data['Observability']['VLTI']):
                c_M = True
            else:
                c_M = False
            plt.scatter(x0+0.5*off, y0, 100,
                        color=color[str(c_M)], edgecolors='#364f6b')
        except:
            pass
        try:
            if (ins['MATISSE'][tel][ft][band]['HR'] & data['Observability']['VLTI']):
                c_N = True
            else:
                c_N = False
            plt.scatter(x0+off, y0, 100,
                        color=color[str(c_N)], edgecolors='#364f6b')
        except:
            pass
    else:
        plt.plot(x0, y0, 'o', color=color[str(ins[inst][tel][band])], ms=10)
    return None


def patch_cube_fancy(x, y, ms=25, c='#d3d3d3', z=2):
    plt.plot(x, y, 'o', ms=ms, color=c, zorder=z)
    plt.plot(x+0.5, y, 's', ms=ms, color=c, zorder=z)
    plt.plot(x+0.7, y, 's', ms=ms, color=c, zorder=z)
    plt.plot(x+0.9, y, 's', ms=ms, color=c, zorder=z)
    plt.plot(x+0.3, y, 's', ms=ms, color=c, zorder=z)
    plt.plot(x+1.2, y, 'o', ms=ms, color=c, zorder=z)
    return None


def fancy_button(x, y, t, off=0.04, fs=12):
    plt.text(x, y, t, fontsize=fs, color='#364f6b', ha='center', va='center',
             bbox=dict(boxstyle='round', pad=1., edgecolor='#364f6b',
                       facecolor='#e8e8e8', alpha=1), zorder=50)
    plt.text(x-off, y, t, fontsize=fs, color='#364f6b', ha='center', va='center',
             bbox=dict(boxstyle='round', pad=1, edgecolor='none',
                       facecolor='#364f6b', alpha=1), zorder=49)


def fancy_button_rel(x, y, t, ax, fs=8):
    """ Function to plot nice button."""
    plt.text(x, y, t, ha='center', va='top', transform=ax.transAxes, fontsize=fs, color='#364f6b',
             bbox=dict(boxstyle='round', pad=1., edgecolor='#364f6b',
                       facecolor='#e8e8e8', alpha=1), zorder=50)
    plt.text(x-0.005, y, t, ha='center', va='top', transform=ax.transAxes, fontsize=fs, color='#364f6b',
             bbox=dict(boxstyle='round', pad=1, edgecolor='none',
                       facecolor='#364f6b', alpha=1), zorder=49)


def plot_diag(x0, x1, y, off=0, l=3, lw=1):
    if l == 3:
        plt.plot([x0, x1], [y, y+off], ls='-', c='#364f6b', lw=lw)
        plt.plot([x0, x1], [y, y], ls='-', c='#364f6b', lw=lw)
        plt.plot([x0, x1], [y, y-off], ls='-', c='#364f6b', lw=lw)
    elif l == 2:
        plt.plot([x0, x1], [y, y+off], ls='-', c='#364f6b', lw=lw, zorder=-1)
        plt.plot([x0, x1], [y, y-off], ls='-', c='#364f6b', lw=lw, zorder=-1)
    elif l == 1:
        plt.plot([x0, x1], [y, y], ls='-', c='#364f6b', lw=lw, zorder=-1)
    return None


def add_vs_mode_matisse(out, dic, star, cond_VLTI, cond_guid):
    """ Small function for count_survey. Counts MATISSE observability for each mode."""
    for tel in ['AT', 'UT']:
        for ft in ['noft', 'ft']:
            for band in ['L', 'N']:
                for res in ['LR', 'HR']:
                    cond_ins = out[star]['Ins']['MATISSE'][tel][ft][band][res]
                    if cond_VLTI and cond_guid and cond_ins:
                        dic['MATISSE'][tel][ft][band][res].append(star)
    return dic


def add_vs_mode_gravity(out, dic, star, cond_VLTI, cond_guid):
    """ Small function for count_survey. Counts GTAVITY observability for each mode."""
    for tel in ['AT', 'UT']:
        for res in ['MR', 'HR']:
            cond_ins = out[star]['Ins']['GRAVITY'][tel]['K'][res]
            if cond_VLTI and cond_guid and cond_ins:
                dic['GRAVITY'][tel][res].append(star)
    return dic


def autolabel(bars, add, ind, fontsize=11):
    """ Plot the number associated to each histogram column."""
    for ii, bar in enumerate(bars):
        height = bars[ii]
        plt.text(ind[ii]+add, height+0.1, '%s' % (str(bars[ii])),
                 ha='center', va='bottom', fontsize=fontsize,
                 zorder=30, color='#364f6b')


def count_survey(survey):
    """ Count the number of star observable with each HRA instrument."""
    list_star = survey.keys()
    n_star = len(list_star)

    n_chara, n_vlti = 0, 0
    for x in list_star:
        if survey[x]['Simbad']:
            if not survey[x]['SED'] == None:
                if survey[x]['Observability']['VLTI']:
                    n_vlti += 1
                if survey[x]['Observability']['CHARA']:
                    n_chara += 1

    cprint('\nYour list contain %i stars:' % n_star, 'cyan')
    cprint('-------------------------', 'cyan')
    print('Observability: %i (%2.1f %%) from the VLTI, %i (%2.1f %%) from the CHARA.\n' %
          (n_vlti, 100*float(n_vlti)/n_star, n_chara, 100*float(n_chara)/n_star))

    dic = {'MATISSE': {'UT': {'noft': {'L': {'LR': [], 'HR': []}, 'N': {'LR': [], 'HR': []}},
                              'ft': {'L': {'LR': [], 'HR': []}, 'N': {'LR': [], 'HR': []}}
                              },
                       'AT': {'noft': {'L': {'LR': [], 'HR': []}, 'N': {'LR': [], 'HR': []}},
                              'ft': {'L': {'LR': [], 'HR': []}, 'N': {'LR': [], 'HR': []}}
                              },
                       },
           'GRAVITY': {'UT': {'MR': [],
                              'HR': []},
                       'AT': {'MR': [],
                              'HR': []}
                       },
           'PIONIER': [],
           'PAVO': [],
           'CLASSIC': {'V': [], 'H': [], 'K': []},
           'CLIMB': [],
           'MYSTIC': [],
           'MIRC': {'H': [], 'K': []},
           'VEGA': {'LR': [], 'MR': [], 'HR': []},
           }

    list_no_simbad = []
    for star in list_star:
        if survey[star]['Simbad']:
            if type(survey[star]['Guiding_star']) == list:
                if (len(survey[star]['Guiding_star'][0]) > 0) or (len(survey[star]['Guiding_star'][1]) > 0):
                    guid = True
                else:
                    guid = False
            elif survey[star]['Guiding_star'] == 'Science star':
                guid = True
            else:
                guid = False

            cond_VLTI = survey[star]['Observability']['VLTI']
            cond_guid = guid
            cond_CHARA = survey[star]['Observability']['CHARA']
            cond_tilt = survey[star]['Ins']['CHARA']['Guiding']

            dic = add_vs_mode_matisse(survey, dic, star, cond_VLTI, cond_guid)
            dic = add_vs_mode_gravity(survey, dic, star, cond_VLTI, cond_guid)

            cond_ins = survey[star]['Ins']['PIONIER']['H']
            if (cond_VLTI and cond_guid and cond_ins):
                dic['PIONIER'].append(star)

            for band in ['H', 'K']:
                cond_ins = survey[star]['Ins']['CHARA']['MIRC'][band]

                if (cond_CHARA and cond_ins and cond_tilt):
                    dic['MIRC'][band].append(star)

            for res in ['LR', 'HR']:
                cond_ins = survey[star]['Ins']['CHARA']['VEGA'][res]
                if (cond_CHARA and cond_ins and cond_tilt):
                    dic['VEGA'][res].append(star)

            for band in ['V', 'H', 'K']:
                cond_ins = survey[star]['Ins']['CHARA']['CLASSIC'][band]
                if (cond_CHARA and cond_ins and cond_tilt):
                    dic['CLASSIC'][band].append(star)

            if (cond_CHARA and survey[star]['Ins']['CHARA']['PAVO']['R'] and cond_tilt):
                dic['PAVO'].append(star)

            if (cond_CHARA and survey[star]['Ins']['CHARA']['MYSTIC']['K'] and cond_tilt):
                dic['MYSTIC'].append(star)

            if (cond_CHARA and survey[star]['Ins']['CHARA']['CLIMB']['K'] and cond_tilt):
                dic['CLIMB'].append(star)
        else:
            list_no_simbad.append(star)

    return dic, list_no_simbad


def print_list_survey(result_survey):
    """ Plot list of stars observable with CHARA and VLTI interferometers."""
    cprint('\nVLTI:', 'green')
    cprint('-----', 'green')
    print('MATISSE (AT):', result_survey['MATISSE']['AT']['noft']['L']['LR'])
    print('        (UT):', result_survey['MATISSE']['UT']['noft']['L']['LR'])
    print('GRAVITY (AT):', result_survey['GRAVITY']['AT']['HR'])
    print('        (UT):', result_survey['GRAVITY']['UT']['HR'])
    print('PIONIER (AT/UT):', result_survey['PIONIER'])
    cprint('\nCHARA:', 'green')
    cprint('------', 'green')
    print('VEGA:', result_survey['VEGA']['LR'])
    print('PAVO:', result_survey['PAVO'])
    print('MIRC:', result_survey['MIRC']['H'])
    print('CLIMB:', result_survey['CLIMB'])
    print('CLASSIC:', result_survey['CLASSIC']['H'])
    return None


def plot_histo_survey(dic, setlog=False):
    """ Plot histogram of the result from count_survey fonction.
    Show the number of stars observable which each instruments. 

    Parameters:
    -----------
    `dic`: {dict}
        Dictionnary from count_survey fonction,\n
    `setlog`: {boolean},
        If True, set the y-scale to log (default=False).

    """
    w = 0.4
    xmin, xmax = 0, 10.

    dataL_ft = [len(dic['MATISSE']['AT']['ft']['L']['LR']),
                len(dic['MATISSE']['UT']['ft']['L']['LR'])]
    dataL_noft = [len(dic['MATISSE']['AT']['noft']['L']['LR']),
                  len(dic['MATISSE']['UT']['noft']['L']['LR'])]
    dataN_ft = [len(dic['MATISSE']['AT']['ft']['N']['LR']),
                len(dic['MATISSE']['UT']['ft']['N']['LR'])]
    dataN_noft = [len(dic['MATISSE']['AT']['noft']['N']['LR']),
                  len(dic['MATISSE']['UT']['noft']['N']['LR'])]

    dataL_ft_hr = [len(dic['MATISSE']['AT']['ft']['L']['HR']),
                   len(dic['MATISSE']['UT']['ft']['L']['HR'])]
    dataL_noft_hr = [len(dic['MATISSE']['AT']['noft']['L']['HR']),
                     len(dic['MATISSE']['UT']['noft']['L']['HR'])]
    dataN_ft_hr = [len(dic['MATISSE']['AT']['ft']['N']['HR']),
                   len(dic['MATISSE']['UT']['ft']['N']['HR'])]
    dataN_noft_hr = [len(dic['MATISSE']['AT']['noft']['N']['HR']),
                     len(dic['MATISSE']['UT']['noft']['N']['HR'])]

    data_grav = [len(dic['GRAVITY']['AT']['MR']),
                 len(dic['GRAVITY']['UT']['MR'])]
    data_grav_hr = [len(dic['GRAVITY']['AT']['HR']),
                    len(dic['GRAVITY']['UT']['HR'])]

    ymax = np.max([np.max(dataL_ft), np.max(data_grav), np.max(data_grav_hr),
                   len(dic['PIONIER']), len(dic['VEGA']['LR']),
                   len(dic['CLIMB']), len(dic['CLASSIC']['H']),
                   len(dic['PAVO']), len(dic['MYSTIC']),
                   len(dic['MIRC']['H'])])

    x_mat = 1
    x_gra = 2.6
    x_pio = 3.9
    x_pavo = 5
    x_vega = 6
    x_climb = 7
    x_mirc = 8
    x_classic = 9.2

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    plt.text(0.07, 1.02, '  VLTI  ', fontsize=12, weight="bold", ha='center',
             verticalalignment='top', transform=ax.transAxes,
             bbox=dict(boxstyle='circle', edgecolor='#364f6b',
                       facecolor='w', alpha=1), zorder=5)
    plt.text(0.53, 1.02, 'CHARA', fontsize=12, weight="bold", ha='center',
             verticalalignment='top', transform=ax.transAxes,
             bbox=dict(boxstyle='circle', edgecolor='#364f6b',
                       facecolor='w', alpha=1), zorder=5)
    y = -0.04

    fancy_button_rel(x_mat/xmax, y, 'MATISSE', ax, fs=8)
    fancy_button_rel(x_gra/xmax, y, 'GRAVITY', ax, fs=8)
    fancy_button_rel(x_pio/xmax, y, 'PIONIER', ax, fs=8)
    fancy_button_rel(x_pavo/xmax, y, 'PAVO', ax, fs=8)
    fancy_button_rel(x_vega/xmax, y, 'VEGA', ax, fs=8)
    fancy_button_rel(x_climb/xmax, y, 'CLIMB', ax, fs=8)
    fancy_button_rel(x_mirc/xmax, y, 'MIRC', ax, fs=8)
    fancy_button_rel(x_classic/xmax, y, 'CLASSIC', ax, fs=8)

    # ---------------------------------
    # MATISSE
    ind = np.array([x_mat-((2*w)-0.15), x_mat+(w-0.15)])
    ax.bar(ind, dataL_ft, width=w, color='#5ab2dd',
           edgecolor='#364f6b', align='center', alpha=0.4)
    ax.bar(ind, dataL_noft, width=w, color='#5ab2dd', label='L band (3.5 µm)',
           align='center', edgecolor='#364f6b')
    ax.bar(ind+w, dataN_ft, width=w, color='#124a67',
           edgecolor='#364f6b', align='center', alpha=0.4)
    ax.bar(ind+w, dataN_noft, width=w, color='#124a67', label='N band (10 µm)',
           align='center', edgecolor='#364f6b')

    ax.scatter(ind, dataL_ft_hr, s=30, marker='s', zorder=10,
               color='#cee2e6', alpha=.5, edgecolors='#364f6b')
    ax.scatter(ind, dataL_noft_hr, s=30, marker='s', zorder=10,
               color='#cee2e6', alpha=1, edgecolors='#364f6b')
    ax.scatter(ind+w, dataN_ft_hr, s=30, marker='s', zorder=10,
               color='#cee2e6', alpha=.5, edgecolors='#364f6b')
    ax.scatter(ind+w, dataN_noft_hr, s=30, marker='s', zorder=10,
               color='#cee2e6', alpha=1, edgecolors='#364f6b')

    plt.text(ind[0]+w/2, 0.5, 'AT', ha='center', va='center', c='w',
             zorder=50, fontsize=8)
    plt.text(ind[1]+w/2, 0.5, 'UT', ha='center', va='center', c='w',
             zorder=50, fontsize=8)
    plt.scatter(ind[0]+w/2, 0.5, 300, edgecolors='#364f6b',
                color='#00b08b', zorder=10, marker="H")
    plt.scatter(ind[1]+w/2, 0.5, 300, edgecolors='#364f6b',
                color='#00b08b', zorder=10, marker="H")

    autolabel(dataL_ft, 0, ind)
    autolabel(dataN_ft, 0, ind+w)
    autolabel(dataL_noft, 0, ind)
    autolabel(dataN_noft, 0, ind+w)

    # ---------------------------------
    # GRAVITY
    p_grav = [x_gra-(w/2. + 0.05), x_gra + (w/2. + 0.05)]
    ax.bar(p_grav, data_grav, width=w, color='#d91552', label='K band (2.2 µm)',
           align='center', edgecolor='#364f6b')
    ax.scatter(p_grav, data_grav_hr, s=30, marker='s', zorder=10,
               color='#cee2e6', alpha=1, edgecolors='#364f6b')

    plt.text(p_grav[0], 0.5, 'AT', ha='center', va='center', c='w',
             zorder=50, fontsize=8)
    plt.text(p_grav[1], 0.5, 'UT', ha='center', va='center', c='w',
             zorder=50, fontsize=8)
    plt.scatter(p_grav[0], 0.5, 300, edgecolors='#364f6b',
                color='#00b08b', zorder=10, marker="H")
    plt.scatter(p_grav[1], 0.5, 300, edgecolors='#364f6b',
                color='#00b08b', zorder=10, marker="H")

    autolabel(data_grav, 0, p_grav)

    # ---------------------------------
    # PIONIER
    p_pio = [x_pio]
    ax.bar(p_pio, len(dic['PIONIER']), width=w, color='#f38630', label='H band (1.6 µm)',
           align='center', edgecolor='#364f6b')
    autolabel([len(dic['PIONIER'])], 0, p_pio)

    # ---------------------------------
    # PAVO
    p = [x_pavo]
    y = [len(dic['PAVO'])]
    ax.bar(p, y, width=w, color='gold', label='R band (0.8 µm)',
           align='center', edgecolor='#364f6b')
    autolabel(y, 0, p)

    # ---------------------------------
    # VEGA
    p = [x_vega]
    y = [len(dic['VEGA']['LR'])]
    ax.bar(p, y, width=w, color='#55d655', label='V band (0.6 µm)',
           align='center', edgecolor='#364f6b')
    ax.scatter(p, len(dic['VEGA']['HR']), s=30, marker='s', zorder=10,
               color='#cee2e6', alpha=1, edgecolors='#364f6b', label='High spectal res.')
    autolabel(y, 0, p)

    # ---------------------------------
    # CLIMB
    p = [x_climb]
    y = [len(dic['CLIMB'])]
    ax.bar(p, len(dic['CLIMB']), width=w, color='#d91552',
           align='center', edgecolor='#364f6b')
    autolabel(y, 0, p)

    # ---------------------------------
    # MIRC
    p = np.array([x_mirc-(w/2. + 0.05)])
    ax.bar(p, len(dic['MIRC']['H']), width=w, color='#f38630',
           align='center', edgecolor='#364f6b')
    ax.bar(p+w + 0.1, len(dic['MIRC']['K']), width=w, color='#d91552',
           align='center', edgecolor='#364f6b')
    ax.bar(p+w + 0.1, len(dic['MYSTIC']), width=w, color='#d91552',
           align='center', edgecolor='#364f6b', alpha=.4)
    autolabel([len(dic['MIRC']['H'])], 0, p)
    autolabel([len(dic['MIRC']['K'])], 0, p+w+0.1)
    autolabel([len(dic['MYSTIC'])], 0, p+w+0.1)

    # ---------------------------------
    # CLASSIC
    p = [x_classic-w/2.-0.05, x_classic+w/2.+0.05]
    ax.bar(p[0], len(dic['CLASSIC']['H']), width=w, color='#f38630',
           align='center', edgecolor='#364f6b')
    ax.bar(p[1], len(dic['CLASSIC']['K']), width=w, color='#d91552',
           align='center', edgecolor='#364f6b')
    autolabel([len(dic['CLASSIC']['H'])], 0, [p[0]])
    autolabel([len(dic['CLASSIC']['K'])], 0, [p[1]])

    plt.vlines((x_pio/xmax)+0.058, 0, 1, transform=ax.transAxes, color='w')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    handles, labels = ax.get_legend_handles_labels()
    handles1 = [handles[6], handles[5], handles[4],
                handles[3], handles[1], handles[2], handles[0]]
    labels1 = [labels[6], labels[5], labels[4],
               labels[3], labels[1], labels[2], labels[0]]

    # plt.ylabel('# stars')
    ax.legend(handles1, labels1, fontsize=8, loc='best')
    plt.xlim(xmin, xmax)
    if setlog == True:
        ax.set_yscale('log')
        plt.ylim(0, ymax*2)
    else:
        plt.ylim(0, ymax+3)
    ax.patch.set_facecolor('#dfe4ed')
    plt.subplots_adjust(top=0.920,
                        bottom=0.090,
                        left=0.02,
                        right=0.98,
                        hspace=0.2,
                        wspace=0.2)
    plt.show(block=False)


def plot_VLTI(data):
    """ 
    Display a synthetic plot with observability of the target with each
    instruments of the VLTI array. The spectral resolutions are included 
    if exists.
    """

    star = data['Name']

    if data['Ins'] != None:
        pass
    else:
        cprint('## Error: %s not in Simbad!' % star, 'red')
        return None

    ins = data['Ins']
    if (data['Gaia_dr2']['check']):
        display_gaia = '(D = %2.1f kpc)' % (data['Gaia_dr2']['Dkpc'])
    else:
        display_gaia = '(Not in Gaia)'

    # Observability from VLTI site lattitude and guiding limit
    if (type(data['Guiding_star']) == str):
        aff_guide = 'Science'
    elif (type(data['Guiding_star']) == list):
        if len(data['Guiding_star'][0] > 0):
            aff_guide = 'Off axis'
        else:
            if len(data['Guiding_star'][1]) > 0:
                aff_guide = 'Off axis*'
            else:
                aff_guide = 'X'
    else:
        aff_guide = 'X'

    if aff_guide == 'X':
        c_guid = '#ed929d'
    elif aff_guide == 'Science':
        c_guid = '#8ee38e'
    else:
        c_guid = '#fbe570'

    # Do not change the display.
    x_ins, x_tel, x_ft, x_band, x_res = 2, 3.2, 4, 5, 5.5
    y_pionier, y_gravity, y_matisse = -3.8, -0.2, 8

    xmin, xmax = x_ins-1, x_res+0.8

    # Limit the star name lenght (display purposes)
    name_star = star.upper()
    if len(star) > 7:
        name_star = star.upper()[:7] + '.'
    else:
        name_star = star.upper()

    # Positions in the figure
    x_star, y_star = 0.15, 0.9
    x_mag, y_mag, fs_mag = 3, 16, 9
    y_tel_mat, y_tel_grav = 3, 0.8
    off_button, off_res = 0.06, 0.5
    dec_res, dec_label = 0.5, 1.7
    lw = 1

    fig = plt.figure(figsize=(4, 6))
    ax = plt.subplot(111)

    # -------------------
    # Observavility from site and guiding limit
    plt.text(x_star, y_star, name_star, fontsize=11, weight="bold", ha='center', va='center', transform=ax.transAxes,
             bbox=dict(boxstyle='circle', edgecolor=color[str(data['Observability']['VLTI'])],
                       facecolor='w', alpha=0.6), zorder=50)

    plt.text(x_star, y_star-0.1, 'Guiding star:\n%s' % aff_guide, fontsize=8,
             va='center', ha='center', transform=ax.transAxes,
             bbox=dict(boxstyle='round', facecolor=c_guid, alpha=1), zorder=50)

    # -------------------
    # Relevant magnitudes
    plt.text(x_mag, y_mag, 'G=%2.1f' % data['Mag']['magG'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round', facecolor='#55d655', alpha=0.6), zorder=50)

    plt.text(x_mag+0.8, y_mag, 'H=%2.1f' % data['Mag']['magH'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round', facecolor='#f38630', alpha=0.8), zorder=50)

    plt.text(x_mag+1.6, y_mag, 'K=%2.1f' % data['Mag']['magK'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round', facecolor='#d91552', alpha=0.8), zorder=50)

    plt.text(x_mag, y_mag-1, 'L=%2.1f' % data['Mag']['magL'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round', facecolor='#5ab2dd', alpha=0.8), zorder=50)

    plt.text(x_mag+0.8, y_mag-1, 'M=%2.1f' % data['Mag']['magM'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round', facecolor='#187bb0', alpha=0.8), zorder=50)

    plt.text(x_mag+1.6, y_mag-1, 'N=%2.1f' % data['Mag']['magN'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round', facecolor='#124a67', alpha=0.8), zorder=50)

    # -------------------
    # Instruments
    fancy_button(x_ins, y_matisse, 'MATISSE ')
    fancy_button(x_ins, y_pionier, 'PIONIER ')
    fancy_button(x_ins, y_gravity, 'GRAVITY ')

    # -------------------
    # Telescopes
    pos_y_tel = [y_matisse+y_tel_mat, y_matisse-y_tel_mat,
                 y_gravity+y_tel_grav, y_gravity-y_tel_grav, y_pionier]
    l_tel = ['AT', 'UT', 'AT', 'UT', 'AT']

    for i in range(len(pos_y_tel)):
        plt.scatter(x_tel, pos_y_tel[i], 700, edgecolors='#364f6b',
                    color='#00b08b', zorder=10, marker="H")
        plt.text(x_tel, pos_y_tel[i], l_tel[i], va='center',
                 ha='center', zorder=15, color='w')

    # -------------------
    # Fringe tracker
    pos_y_ft = [y_matisse-4.5, y_matisse-1.5, y_matisse+1.5, y_matisse+4.5]
    l_ft = ['noft', 'ft', 'noft', 'ft']
    for i in range(4):
        plt.text(x_ft, pos_y_ft[i], l_ft[i], color='w',
                 va='center', ha='center', zorder=50)
        plt.scatter(x_ft, pos_y_ft[i], 8e2, c='#ea779d',
                    zorder=10, edgecolors='#364f6b')

    # -------------------
    # Photometric bands
    plt.text(x_band, y_gravity+y_tel_grav, 'K', ha='center', va='center', color='w',
             bbox=dict(boxstyle='square', edgecolor='#364f6b',
                       facecolor='#d91552', alpha=1), zorder=50)
    plt.text(x_band, y_gravity-y_tel_grav, 'K', ha='center', va='center', color='w',
             bbox=dict(boxstyle='square', edgecolor='#364f6b',
                       facecolor='#d91552', alpha=1), zorder=50)
    plt.text(x_band, y_pionier, 'H', ha='center', va='center', color='w',
             bbox=dict(boxstyle='square', edgecolor='#364f6b',
                       facecolor='#f38630', alpha=1), zorder=50)

    y_band_matisse = [y_matisse-5+0.5, y_matisse -
                      2+0.5, y_matisse+1+0.5, y_matisse+4+0.5]
    dec_x_band = 0.05
    for y in y_band_matisse:
        plt.text(x_band, y+1, 'L', ha='center', va='center', color='w',
                 bbox=dict(boxstyle='square', edgecolor='#364f6b',
                           facecolor='#5ab2dd', alpha=1), zorder=50)
        plt.text(x_band, y, 'M', ha='center', va='center', color='w',
                 bbox=dict(boxstyle='square', edgecolor='#364f6b',
                           facecolor='#187bb0', alpha=1), zorder=50)
        plt.text(x_band, y-1, 'N', ha='center', va='center', color='w',
                 bbox=dict(boxstyle='square', edgecolor='#364f6b',
                           facecolor='#124a67', alpha=1), zorder=50)
        plot_diag(x_ft, x_band, y, 1, lw=lw)

    # -------------------
    # Observabilities
    plot_mat(data, 'MATISSE', 'AT', 'ft', 'L',
             x_res, y_band_matisse[3]+1, off_res)
    plot_mat(data, 'MATISSE', 'AT', 'ft', 'M',
             x_res, y_band_matisse[3], off_res)
    plot_mat(data, 'MATISSE', 'AT', 'ft', 'N',
             x_res, y_band_matisse[3]-1, off_res)
    plot_mat(data, 'MATISSE', 'AT', 'noft', 'L',
             x_res, y_band_matisse[2]+1, off_res)
    plot_mat(data, 'MATISSE', 'AT', 'noft', 'M',
             x_res, y_band_matisse[2], off_res)
    plot_mat(data, 'MATISSE', 'AT', 'noft', 'N',
             x_res, y_band_matisse[2]-1, off_res)
    plot_mat(data, 'MATISSE', 'UT', 'ft', 'L',
             x_res, y_band_matisse[1]+1, off_res)
    plot_mat(data, 'MATISSE', 'UT', 'ft', 'M',
             x_res, y_band_matisse[1], off_res)
    plot_mat(data, 'MATISSE', 'UT', 'ft', 'N',
             x_res, y_band_matisse[1]-1, off_res)
    plot_mat(data, 'MATISSE', 'UT', 'noft', 'L',
             x_res, y_band_matisse[0]+1, off_res)
    plot_mat(data, 'MATISSE', 'UT', 'noft', 'M',
             x_res, y_band_matisse[0], off_res)
    plot_mat(data, 'MATISSE', 'UT', 'noft', 'N',
             x_res, y_band_matisse[0]-1, off_res)

    plt.scatter(x_res+0.25, y_gravity+y_tel_grav, 100,
                color=color[str(ins['GRAVITY']['AT']['K']['MR'] and data['Observability']['VLTI'])], edgecolors='#364f6b')
    plt.scatter(x_res+0.25, y_gravity-y_tel_grav, 100,
                color=color[str(ins['GRAVITY']['UT']['K']['MR'] and data['Observability']['VLTI'])], edgecolors='#364f6b')
    plt.scatter(x_res+0.5, y_gravity+y_tel_grav, 100,
                color=color[str(ins['GRAVITY']['AT']['K']['HR'] and data['Observability']['VLTI'])], edgecolors='#364f6b')
    plt.scatter(x_res+0.5, y_gravity-y_tel_grav, 100,
                color=color[str(ins['GRAVITY']['UT']['K']['HR'] and data['Observability']['VLTI'])], edgecolors='#364f6b')

    plt.scatter(x_res, y_pionier, 100, color=color[str(
        ins['PIONIER']['H'] and data['Observability']['VLTI'])], edgecolors='#364f6b')

    # -------------------
    # Link lines
    plot_diag(x_ins, x_tel, y_matisse, y_tel_mat, l=2, lw=lw)
    plot_diag(x_ins, x_tel, y_gravity, y_tel_grav, l=2, lw=lw)
    plot_diag(x_tel, x_ft, y_matisse+y_tel_mat, 1.5, l=2, lw=lw)
    plot_diag(x_tel, x_ft, y_matisse-y_tel_mat, 1.5, l=2, lw=lw)
    plot_diag(x_tel, x_band, y_gravity+y_tel_grav, lw=lw, l=1)
    plot_diag(x_tel, x_band, y_gravity-y_tel_grav, lw=lw, l=1)
    plot_diag(x_ins, x_band, y_pionier, lw=lw, l=1)

    # -------------------
    # Resolution labels
    plt.text(x_res, np.max(y_band_matisse) + dec_label, 'LR',
             va='center', ha='center', fontsize=8, style='italic')
    plt.text(x_res+0.5*off_res, np.max(y_band_matisse)+dec_label, 'MR',
             va='center', ha='center', fontsize=8, style='italic')
    plt.text(x_res+off_res, np.max(y_band_matisse)+dec_label, 'HR',
             va='center', ha='center', fontsize=8, style='italic')

    # -------------------
    # Separating lines
    plt.hlines(y_gravity+1.8, xmin, xmax, color='w')
    plt.hlines(y_gravity-1.8, xmin, xmax, color='w')

    # -------------------
    # Figure parameters
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.patch.set_facecolor('#dfe4ed')
    ax.patch.set_alpha(1)
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    plt.axis([xmin, xmax, y_pionier-1.8, np.max(y_band_matisse)+5])
    plt.subplots_adjust(top=0.994,
                        bottom=0.011,
                        left=0.008,
                        right=0.992,
                        hspace=0.2,
                        wspace=0.2)
    plt.show(block=False)

    return fig


def plot_CHARA(data):
    """ 
    Display a synthetic plot with observability of the target with each
    instrument of the CHARA array. The spectral resolutions are included if exists.
    """
    star = data['Name']

    if data['Ins'] != None:
        pass
    else:
        cprint('## Error: %s not in Simbad!' % star, 'red')
        return None

    ins = data['Ins']['CHARA']

    # Observability from CHARA site lattitude and guiding/tip/tilt limit
    cond_CHARA = data['Observability']['CHARA']
    cond_tilt = ins['Guiding']  # Limit by the V mag.
    if cond_tilt:
        c_guid = '#8ee38e'
    else:
        c_guid = '#ed929d'

    # Do not change the display.
    x_ins, x_band, x_res = 1.5, 3.5, 4.5
    y_classic, y_climb, y_mirc, y_pavo, y_vega = 1, 2, 3, 4, 5

    xmin, xmax = 0, x_res+1.7

    # Limit the star name lenght (display purposes)
    name_star = star.upper()
    if len(star) > 7:
        name_star = star.upper()[:7] + '.'
    else:
        name_star = star.upper()

    # Positions in the figure
    x_star, y_star = 0.22, 0.9
    x_mag, y_mag, fs_mag = 2.6, 6.5, 9
    off_button = 0.06
    dec_res, dec_label = 0.5, 0.2
    lw = 1

    fig = plt.figure(figsize=(3, 6))
    ax = plt.subplot(111)

    # -------------------
    # Observavility from site and guiding limit
    plt.text(x_star, y_star, name_star, fontsize=11, weight="bold", ha='center', va='center', transform=ax.transAxes,
             bbox=dict(boxstyle='circle', edgecolor=color[str(cond_CHARA)],
                       facecolor='w', alpha=0.6), zorder=50)
    plt.text(x_star, y_star-0.1, 'Guiding/tip-tilt', fontsize=8,
             ha='center', va='center', transform=ax.transAxes, bbox=dict(boxstyle='round',
                                                                         facecolor=c_guid, alpha=1), zorder=50)

    # -------------------
    # Relevant magnitudes
    plt.text(x_mag, y_mag, 'V=%2.1f' % data['Mag']['magV'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round',
                                    facecolor='#8ee38e', alpha=1), zorder=50)

    plt.text(x_mag+1.2, y_mag, 'H=%2.1f' % data['Mag']['magH'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round',
                                    facecolor='#f38630', alpha=0.8), zorder=50)

    plt.text(x_mag+2.4, y_mag, 'K=%2.1f' % data['Mag']['magK'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round',
                                    facecolor='#d91552', alpha=0.8), zorder=50)
    plt.text(x_mag, y_mag-0.3, 'R=%2.1f' % data['Mag']['magR'], fontsize=fs_mag,
             va='center', bbox=dict(boxstyle='round',
                                    facecolor='#fcd667', alpha=0.8), zorder=50)

    # -------------------
    # Instruments
    fancy_button(x_ins, y_vega, 'VEGA ', off=off_button)
    fancy_button(x_ins, y_pavo, 'PAVO ', off=off_button)
    fancy_button(x_ins, y_mirc, 'MIRC ', off=off_button)
    fancy_button(x_ins, y_climb, 'CLIMB ', off=off_button)
    fancy_button(x_ins, y_classic, 'CLASSIC ', off=off_button)

    # -------------------
    # Photometric bands
    plt.text(x_band, y_vega, 'V', ha='center', va='center', color='w', bbox=dict(boxstyle='square', edgecolor='#364f6b',
                                                                                 facecolor='#8ee38e', alpha=1), zorder=50)
    plt.text(x_band, y_pavo, 'R', ha='center', va='center', color='w', bbox=dict(boxstyle='square', edgecolor='#364f6b',
                                                                                 facecolor='#fcd667', alpha=1), zorder=50)
    plt.text(x_band, y_mirc, 'H', ha='center', va='center', color='w', bbox=dict(boxstyle='square', edgecolor='#364f6b',
                                                                                 facecolor='#f38630', alpha=1), zorder=50)
    plt.text(x_band, y_climb, 'K', ha='center', va='center', color='w', bbox=dict(boxstyle='square', edgecolor='#364f6b',
                                                                                  facecolor='#d91552', alpha=1), zorder=50)
    plt.text(x_band, y_classic+0.15, 'H', ha='center', va='center', color='w', bbox=dict(boxstyle='square', edgecolor='#364f6b',
                                                                                         facecolor='#f38630', alpha=1), zorder=50)
    plt.text(x_band, y_classic-0.15, 'K', ha='center', va='center', color='w', bbox=dict(boxstyle='square', edgecolor='#364f6b',
                                                                                         facecolor='#d91552', alpha=1), zorder=50)

    # -------------------
    # Observabilities
    plt.scatter(x_res, y_vega, 100, color=color[str(
        ins['VEGA']['LR'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res+dec_res, y_vega, 100, color=color[str(
        ins['VEGA']['MR'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res+2*dec_res, y_vega, 100, color=color[str(
        ins['VEGA']['HR'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res, y_pavo, 100, color=color[str(
        ins['PAVO'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res, y_mirc, 100, color=color[str(
        ins['MIRC']['H'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res, y_climb, 100, color=color[str(
        ins['CLIMB'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res, y_classic+0.15, 100, color=color[str(
        ins['CLASSIC']['H'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')
    plt.scatter(x_res, y_classic-0.15, 100, color=color[str(
        ins['CLASSIC']['K'] and cond_CHARA and cond_tilt)], edgecolors='#364f6b')

    # -------------------
    # Link lines
    plot_diag(x_ins, x_band, y_classic, off=0.15, l=2, lw=lw)
    plt.plot([x_ins, x_band], [y_vega, y_vega], '-', color='#364f6b', lw=lw)
    plt.plot([x_ins, x_band], [y_climb, y_climb], '-', color='#364f6b', lw=lw)
    plt.plot([x_ins, x_band], [y_mirc, y_mirc], '-', color='#364f6b', lw=lw)
    plt.plot([x_ins, x_band], [y_pavo, y_pavo], '-', color='#364f6b', lw=lw)

    # -------------------
    # Resolution labels
    plt.text(x_res, y_vega + dec_label, 'LR', fontsize=8,
             style='italic', va='center', ha='center')
    plt.text(x_res+dec_res, y_vega + dec_label, 'MR', fontsize=8,
             style='italic', va='center', ha='center')
    plt.text(x_res+2*dec_res, y_vega + dec_label, 'HR', fontsize=8,
             style='italic', va='center', ha='center')

    # -------------------
    # Separating lines
    plt.hlines(y_classic+0.5, xmin, xmax, color='w')
    plt.hlines(y_pavo+0.5, xmin, xmax, color='w')
    plt.hlines(y_mirc+0.5, xmin, xmax, color='w')
    plt.hlines(y_climb+0.5, xmin, xmax, color='w')

    # -------------------
    # Figure parameters
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.patch.set_facecolor('#dfe4ed')
    ax.patch.set_alpha(1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.axis([0., 6, 0.5, 7])
    plt.subplots_adjust(top=0.994,
                        bottom=0.011,
                        left=0.008,
                        right=0.992,
                        hspace=0.2,
                        wspace=0.2)
    plt.show(block=False)
    return fig