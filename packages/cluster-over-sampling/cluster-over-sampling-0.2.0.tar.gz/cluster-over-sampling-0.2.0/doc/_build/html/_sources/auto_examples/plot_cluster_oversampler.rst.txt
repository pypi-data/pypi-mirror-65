.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_plot_cluster_oversampler.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_plot_cluster_oversampler.py:


==============================
Clustering-based over-sampling
==============================

This example illustrates the data generation 
process and the performance of various 
over-samplers when clustering-based over-sampling 
is used.


.. code-block:: default


    # Author: Georgios Douzas <gdouzas@icloud.com>
    # Licence: MIT

    import matplotlib.pyplot as plt

    import pandas as pd
    from sklearn.base import clone
    from sklearn.datasets import make_classification
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.cluster import KMeans, AgglomerativeClustering
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import f1_score
    from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE
    from imblearn.pipeline import make_pipeline

    from clover.over_sampling import ClusterOverSampler

    print(__doc__)

    RANDOM_STATE = 0
    OVERSAMPLERS = [
        RandomOverSampler(random_state=RANDOM_STATE),
        SMOTE(random_state=RANDOM_STATE + 1),
        BorderlineSMOTE(random_state=RANDOM_STATE + 2),
    ]
    KMEANS = KMeans(random_state=RANDOM_STATE, n_clusters=100)


    def generate_imbalanced_data():
        """Generate imbalanced data."""
        X, y = make_classification(
            n_classes=3,
            class_sep=0.8,
            weights=[0.01, 0.05, 0.94],
            n_informative=2,
            n_redundant=0,
            n_repeated=0,
            n_features=2,
            n_clusters_per_class=1,
            n_samples=2000,
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
            if not isinstance(oversampler, ClusterOverSampler):
                ovs_name = oversampler.__class__.__name__
                title = f'Resampling using {ovs_name}'
            else:
                clusterer_name = oversampler.clusterer.__class__.__name__
                ovs_name = oversampler.oversampler_.__class__.__name__
                title = f'Resampling using {clusterer_name}-{ovs_name}'
        ax.scatter(X_res[:, 0], X_res[:, 1], c=y_res, alpha=0.8, edgecolor='k')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))
        ax.set_title(title)


    def compare_f1_scores(X_train, X_test, y_train, y_test, clf, oversampler, clusterer):
        """Compare F1 scores of oversamplers with and 
        without clustering."""
        ovs_clf = make_pipeline(clone(oversampler), clf)
        clr_ovs_clf = make_pipeline(ClusterOverSampler(clone(oversampler), clusterer), clf)
        y_pred = ovs_clf.fit(X_train, y_train).predict(X_test)
        y_pred_clr = clr_ovs_clf.fit(X_train, y_train).predict(X_test)
        ovs_name = oversampler.__class__.__name__
        clr_name = clusterer.__class__.__name__
        ovs_score = f1_score(y_test, y_pred, average='macro')
        clr_ovs_score = f1_score(y_test, y_pred_clr, average='macro')
        return pd.DataFrame(
            [[ovs_score, clr_ovs_score]],
            columns=['No clustering', clr_name],
            index=[ovs_name],
        )









Generate imbalanced data
##############################################################################

We are generating a highly imbalanced multi-class data set, using
``make_classification`` from scikit-learn.


.. code-block:: default


    X, y = generate_imbalanced_data()
    _, ax = plt.subplots(1, 1, figsize=(15, 7))
    plot_data(X, y, None, ax)




.. image:: /auto_examples/images/sphx_glr_plot_cluster_oversampler_001.png
    :class: sphx-glr-single-img





Effect of clustering to over-samplers
##############################################################################

Clustering based over-sampling allows to identify areas of the input space
which are appropriate to generate artificial data. Therefore, the generation
of noisy samples is avoided and the within-classes imbalanced issue is also
addressed. The next plots show the resampled data when clustering is applied,
comparing them to the resampled data of the initial over-samplers.


.. code-block:: default


    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    for (ax1, ax2), oversampler in zip(axs, OVERSAMPLERS):
        plot_data(X, y, clone(oversampler), ax1)
        plot_data(X, y, ClusterOverSampler(oversampler, KMEANS), ax2)
    fig.tight_layout()




.. image:: /auto_examples/images/sphx_glr_plot_cluster_oversampler_002.png
    :class: sphx-glr-single-img





Performance evaluation of clustering based over-sampling
##############################################################################

We are evaluating various over-samplers using F1-score as evaluation metric
on a test set. The scores with and without clustering are compared.


.. code-block:: default


    clf = GradientBoostingClassifier(random_state=RANDOM_STATE)
    data = train_test_split(X, y, random_state=RANDOM_STATE)
    scores = pd.DataFrame()
    for oversampler in OVERSAMPLERS:
        scores = scores.append(compare_f1_scores(*data, clf, oversampler, KMEANS))
    print(scores)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

                       No clustering    KMeans
    RandomOverSampler       0.755701  0.753091
    SMOTE                   0.611372  0.759189
    BorderlineSMOTE         0.755701  0.763755




We repeat the process for AgglomerativeClustering instead of KMeans.


.. code-block:: default


    aff_prop = AgglomerativeClustering(n_clusters=100)
    scores = pd.DataFrame()
    for oversampler in OVERSAMPLERS:
        scores = scores.append(compare_f1_scores(*data, clf, oversampler, aff_prop))
    print(scores)




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /Users/gdouzas/.pyenv/versions/miniconda3-latest/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
      return f(*args, **kwds)
                       No clustering  AgglomerativeClustering
    RandomOverSampler       0.755701                 0.746050
    SMOTE                   0.611372                 0.757699
    BorderlineSMOTE         0.755701                 0.776927





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  14.515 seconds)


.. _sphx_glr_download_auto_examples_plot_cluster_oversampler.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_cluster_oversampler.py <plot_cluster_oversampler.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_cluster_oversampler.ipynb <plot_cluster_oversampler.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
