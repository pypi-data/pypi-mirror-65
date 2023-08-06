# class viz:

from cycler import cycler
import matplotlib as mpl
import cmocean as cmo
import seaborn as sns
from matplotlib import rcParams
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import scipy.stats as stats
# # from pandas import rolling
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# look up keys
# rcParams.keys()
def darkmode(clamp,cmap,lines):
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
      rcParams[param] = '#111111'  # bluish dark grey
    for param in ['text.color', 'axes.labelcolor']:
      rcParams[param] = '0.95'  # very light grey
    for param in ['xtick.color', 'ytick.color']:
        rcParams[param] = '0.8'
    for param in ['grid.color','axes.edgecolor']:
        rcParams[param] = '0.55'  # bluish dark grey, but slightly lighter than background
    nmap  = []
    for i in np.linspace(cmap.N-(256*clamp),0,lines).round():
      nmap.append(mpl.colors.rgb2hex(cmap(int(i))[:3]))
    rcParams['axes.prop_cycle'] = cycler(color=(nmap))

def colabprettyplot(mode = 'd', clamp = 0.5, cmapp = 'matter', lines=10, figsize=[10,5.5]):
    prettyplot(mode = mode, clamp=clamp, cmapp=cmapp, lines=lines, figsize=figsize)
    rcParams['text.usetex']=False


def prettyplot(mode = 'l', clamp = 0.5, cmapp = 'matter',rev='', lines=10, figsize=[10,5.5]):
    rcParams.update(mpl.rcParamsDefault)
    # method_name = 'install' # set by the command line options
    sns.set()
    if rev == 'r':
        cmapp = cmapp + '_r'
    cmap = eval('cmo.cm.'+cmapp)
    # plt.set_cmap('cmo.'+cmapp)
    rcParams['mathtext.fontset'] = 'stix'
    rcParams['font.family'] = 'STIXGeneral'
    rcParams['mathtext.fontset'] = 'cm'
    rcParams['mathtext.rm'] = 'serif'
    rcParams['figure.figsize'] = figsize
    rcParams['figure.dpi'] = 200
    rcParams['savefig.dpi'] = 200
    rcParams['lines.linewidth'] = 2.5
    rcParams['text.usetex'] = True
    rcParams["image.cmap"] = 'cmo.'+cmapp
    if mode == 'd':
      darkmode(clamp,cmap,lines)
    else:
        nmap  = []
        for i in np.linspace(cmap.N,(256*clamp),lines).round():
            nmap.append(mpl.colors.rgb2hex(cmap(int(i))[:3]))
        rcParams['axes.prop_cycle'] = cycler(color=(nmap))
