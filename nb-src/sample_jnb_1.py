# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python [conda env:.conda-cf1]
#     language: python
#     name: conda-env-.conda-cf1-py
# ---

# %% [markdown]
# # Sample Jupyter Notebook

# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
# %matplotlib notebook

# %% [markdown]
# ## Plot something

# %%
plt.plot(np.sin(np.linspace(0, 10, 100)));

# %% [markdown]
# ## Another heading

# %%
print('hello')

# %% [markdown]
# ## Some math

# %% [markdown]
# $$
# \sum_i^\infty
# $$

# %% [markdown]
# ## Interactive plot

# %%
import holoviews as hv
hv.extension('bokeh')

# %%
# example taken from http://holoviews.org/reference/containers/bokeh/HoloMap.html
frequencies = [0.5, 0.75, 1.0, 1.25]

def sine_curve(phase, freq):
    xvals = [0.1* i for i in range(100)]
    return hv.Curve((xvals, [np.sin(phase+freq*x) for x in xvals]))

curve_dict = {f:sine_curve(0,f) for f in frequencies}

hmap = hv.HoloMap(curve_dict, kdims='frequency')
hmap
