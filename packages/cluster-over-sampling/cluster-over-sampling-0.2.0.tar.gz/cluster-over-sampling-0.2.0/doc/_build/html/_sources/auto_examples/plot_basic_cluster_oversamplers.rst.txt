.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_plot_basic_cluster_oversamplers.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_plot_basic_cluster_oversamplers.py:


================
Basic algorithms
================

This example illustrates the data generation 
process and the performance of KMeans-SMOTE, SOMO
and Geometric SOMO.


.. code-block:: default


    # Author: Georgios Douzas <gdouzas@icloud.com>
    # Licence: MIT

    import matplotlib.pyplot as plt

    import pandas as pd
    from sklearn.base import clone
    from sklearn.datasets import make_classification
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import f1_score
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import make_pipeline

    from clover.over_sampling import KMeansSMOTE, SOMO, GeometricSOMO

    print(__doc__)

    RANDOM_STATE = 2
    OVERSAMPLERS = [
        SMOTE(random_state=RANDOM_STATE),
        KMeansSMOTE(random_state=RANDOM_STATE + 3),
        SOMO(random_state=RANDOM_STATE + 9),
        GeometricSOMO(random_state=RANDOM_STATE + 15),
    ]


    def generate_imbalanced_data():
        """Generate imbalanced data."""
        X, y = make_classification(
            n_classes=3,
            flip_y=0.05,
            weights=[0.15, 0.6, 0.25],
            n_informative=2,
            n_redundant=0,
            n_repeated=0,
            n_features=2,
            n_clusters_per_class=1,
            n_samples=1000,
            random_state=RANDOM_STATE,
        )
        return X, y


    def plot_data(X, y, oversampler, ax):
        """Plot original or resampled data."""
        if oversampler is None:
            X_res, y_res = X, y
            title = 'Original data'
        else:
            oversampler = clone(oversampler)
            X_res, y_res = oversampler.fit_resample(X, y)
            ovs_name = oversampler.__class__.__name__
            title = f'Resampling using {ovs_name}'
        ax.scatter(X_res[:, 0], X_res[:, 1], c=y_res, alpha=0.8, edgecolor='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))
        ax.set_title(title)


    def compare_f1_scores(X_train, X_test, y_train, y_test, clf, oversampler):
        """Compare F1 scores of oversamplers."""
        ovs_clf = make_pipeline(clone(oversampler), clf)
        y_pred = ovs_clf.fit(X_train, y_train).predict(X_test)
        ovs_name = oversampler.__class__.__name__
        ovs_score = f1_score(y_test, y_pred, average='macro')
        return pd.DataFrame([[ovs_score]], columns=['F-score'], index=[ovs_name],)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /Users/gdouzas/.pyenv/versions/miniconda3-latest/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
      return f(*args, **kwds)
    /Users/gdouzas/.pyenv/versions/miniconda3-latest/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
      return f(*args, **kwds)





Generate imbalanced data
##############################################################################

We are generating an imbalanced multi-class data set, using
``make_classification`` from scikit-learn.


.. code-block:: default


    X, y = generate_imbalanced_data()
    _, ax = plt.subplots(1, 1, figsize=(15, 7))
    plot_data(X, y, None, ax)




.. image:: /auto_examples/images/sphx_glr_plot_basic_cluster_oversamplers_001.png
    :class: sphx-glr-single-img





Plot resampled data
##############################################################################

KMeans-SMOTE, SOMO and Geometric SOMO allow to identify areas of the input
space which are appropriate to generate artificial data. Therefore, the
generation of noisy samples is avoided and the within-classes imbalanced issue
is also addressed. The next plots show the resampled data when the above
clustering-based over-samplers are applied comparing them to the resampled data
of SMOTE over-sampler.


.. code-block:: default


    fig, axs = plt.subplots(1, 4, figsize=(15, 5))
    for ax, oversampler in zip(axs, OVERSAMPLERS):
        plot_data(X, y, clone(oversampler), ax)
    fig.tight_layout()




.. image:: /auto_examples/images/sphx_glr_plot_basic_cluster_oversamplers_002.png
    :class: sphx-glr-single-img





Performance evaluation
##############################################################################

We are evaluating the performance of KMeans-SMOTE, SOMO and Geometric SOMO
using F1-score as evaluation metric on a test set. SMOTE's performance is
also included.


.. code-block:: default


    clf = GradientBoostingClassifier(random_state=RANDOM_STATE)
    data = train_test_split(X, y, random_state=RANDOM_STATE)
    scores = pd.DataFrame()
    for oversampler in OVERSAMPLERS:
        scores = scores.append(compare_f1_scores(*data, clf, oversampler))
    print(scores)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

                    F-score
    SMOTE          0.848706
    KMeansSMOTE    0.885831
    SOMO           0.878631
    GeometricSOMO  0.888823





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  3.693 seconds)


.. _sphx_glr_download_auto_examples_plot_basic_cluster_oversamplers.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_basic_cluster_oversamplers.py <plot_basic_cluster_oversamplers.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_basic_cluster_oversamplers.ipynb <plot_basic_cluster_oversamplers.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
