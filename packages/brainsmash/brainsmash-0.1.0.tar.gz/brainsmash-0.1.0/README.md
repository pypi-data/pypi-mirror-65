BrainSMASH
==========

BrainSMASH (Brain Surrogate Maps with Autocorrelated Spatial Heterogeneity) is a 
Python-based computational platform for statistical testing of spatially
autocorrelated brain maps. At the heart of BrainSMASH is the ability to 
simulate surrogate brain maps with spatial autocorrelation that is matched
to spatial autocorrelation in a target brain map. Additional utilities are provided
for users using Connectome Workbench style surface-based neuroimaging files.

Exhaustive documentation can be found [here](https://brainsmash.readthedocs.io).

Dependencies
============
Installing BrainSMASH requires:

- Python 3+
- [numpy](http://www.numpy.org)
- [scipy](https://www.scipy.org/)
- [pandas](https://pandas.pydata.org)
- [nibabel](http://nipy.org/nibabel)
- [matplotlib](https://matplotlib.org)
- [scikit-learn](http://scikit-learn.org/stable/index.html)

If you wish to use the additional utilities provided for Connectome Workbench users, you must have
[Connectome Workbench](https://www.humanconnectome.org/software/get-connectome-workbench) installed with the ``wb_command`` executable locatable in your
system PATH environment variable.

Installation
============
---

BrainSMASH is most easily installed using pip:

    pip install brainsmash

You may also clone and install the source files manually:

    git clone https://github.com/murraylab/brainsmash.git
    cd brainsmash
    python setup.py install

License
-------
The BrainSMASH source code is available under the GNU General Public License v3.0.

Preprint
--------
Please cite the following preprint if you use BrainSMASH in your research:

Burt, J.B., Helmer, M., Shinn, M.W., Anticevic, A., Murray, J.D. (2020). Generative modeling of brain maps with spatial autocorrelation. bioRxiv doi: 10.1101/2020.02.18.955054v1


Core development team
---------------------

* Joshua B Burt, Murray Lab - Yale University
* John D Murray, Murray Lab - Yale University

Change Log
==========
---

* 0.1.0 Added goodness-of-fit metrics to stats module.
* 0.0.9 Fixed bug in Sampled.sampled.permute_map().
* 0.0.8 Relaxed nibabel version dependency.
* 0.0.7 Removed console print statements.
* 0.0.6 Fixed masked dense array handling.
* 0.0.1 Initial beta release.
