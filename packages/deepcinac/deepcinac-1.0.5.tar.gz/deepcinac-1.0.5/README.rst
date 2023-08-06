=========
DeepCINAC
=========

We have developed a Graphical User Interface (GUI) that offers various tools to visually evaluate
inferred neuronal activity from inference methods and to build a eye inspection-based ground truth on calcium imaging data.

Then, we have designed a deep-learning based method, named DeepCINAC (Calcium  Imaging  Neuronal  Activity  Classifier).
Instead  of  basing  activity  inference  on  the extracted fluorescence signal,
DeepCINAC builds up on the visual inspection of each cell from the raw movie using the GUI.

This toolbox being very flexible, it can be adapted to any kind of calcium imaging dataset, in-vivo or in-vitro.

This toolbox can also be used to predict cell type.

.. image:: images/graphical_abstract_deep_cinac.png
    :width: 400px
    :align: center
    :alt: DeepCINAC workflow


To train a classifier, the first step is to annotate data using the GUI. See the GUI `tutorial <https://deepcinac.readthedocs.io/en/latest/tutorial_gui.html>`_ for more information. 

Then using the .cinac files produced, follow the instructions to train your classifier.

Note that .cinac files don’t contain the full original calcium imaging movie,
only patches surrounding the cells you have annotated, 
so you can share the files without fearing that your data will be used by someone 
else other than to train a classifier.

To predict data, you can either use one of our pre-trained classifier or one you have trained (see instructions below).

Please let us know if you encounter any issue, we will be glad to help you.

Contact us at julien.denis3{at}gmail.com

BioRxiv paper
------------- 

https://www.biorxiv.org/content/10.1101/803726v1


Installation
------------

See the `installation page <https://deepcinac.readthedocs.io/en/latest/install.html>`_ of our documentation.


Documentation
-------------

Documentation of DeepCINAC can be found `here <https://deepcinac.readthedocs.io/en/latest/index.html>`_.


Establishing ground truth and visualising predictions
-----------------------------------------------------

.. image:: images/exploratory_GUI.png
    :width: 400px
    :align: center
    :alt: DeepCINAC screenshot


A GUI (Graphical User Interface) offers the tools to carefully examine the activity of each cell
over the course of the recording.

Allows the user to:

* Play the calcium imaging movie between any given frames, zoomed on a cell, with the traces scrolling.

* Display the source and transient profiles of cells and correlation of any transient profile with the source profiles of overlapped cells, such as described in `Gauthier et al. <https://www.biorxiv.org/content/10.1101/473470v1.abstract>`_.

* Select / deselect active periods, allowing to establish a ground truth.

* Indicate the cell type of any cell

* Display the predictions of the classifier (regarding neuronal activity or cell type)

* Diplay neuronal activity inferred using other methods.

* Save ground truth segments in the cinac file format.


Check-out this video for a quick overview of the GUI: https://youtu.be/BZS22bt6YOc


**Follow our** `tutorial <https://deepcinac.readthedocs.io/en/latest/tutorial_gui.html>`_ **to get to know how to use the GUI.**

To launch the GUI execute this command in a terminal :

.. code::

    python -m deepcinac


Training your classifier to infer neuronal activity
---------------------------------------------------

Using the annotated .cinac files created with the GUI, you can now train your classifier.

Below are the few lines of codes needed to train the classifier:

.. code::

    cinac_model = CinacModel(results_path="/media/deepcinac/results",
                             n_epochs=20, batch_size=8)
    cinac_model.add_input_data_from_dir(dir_name="/media/deepcinac/data/cinac_ground_truth/for_training")
    cinac_model.prepare_model()
    cinac_model.fit()


Input data are the cinac files, you can either load all files in a directory 
or load files one by one. 

**On google colab**

If  you don't possess a GPU or don't want to go through the process of configuring your environment to make use of it,
you can run this `notebook <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/notebooks/demo_deep_cinac_training.ipynb>`_
using `google colab <https://colab.research.google.com>`_.

Google provides free virtual machines for you to use: with about 12GB RAM and 50GB hard drive space, and TensorFlow is pre-installed.

You will need a google account. Upload the notebook on google colab, then just follow the instructions in the notebook to go through.

Note that with google colab you won't probably be able to train an efficient classifier has the run time is limited to 12h. However, it will let you test the code. 
You'll then need a local GPU or HPC access to train it with enough data to get good results. 

**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/general/demo_deepcinac_training.py>`_. 


See code below to see how to infer neuronal activity after you have trained a classifier or using the one we provide. 

More information in our `documentation <https://deepcinac.readthedocs.io/en/latest/tutorial_training.html>`_.


Training your classifier to predict cell type
---------------------------------------------

Training a classifier to predict cell type follow the same process as for 
predicting cell activity. 

You will need .cinac files with cell type annotated.

Here are the few lines of code to train it:

.. code::

    cinac_model = CinacModel(results_path="/media/deepcinac/results", 
                             n_epochs=10, 
                             verbose=1, batch_size=4,
                             cell_type_classifier_mode=True,
                             window_len=1000, max_n_transformations=1,
                             max_height=10, max_width=10, 
                             lstm_layers_size=[64], bin_lstm_size=64,
                             overlap_value=0)
    cinac_model.add_input_data_from_dir(dir_name="/media/deepcinac/data/cinac_cell_type_ground_truth/for_training")
    cinac_model.prepare_model()
    cinac_model.fit()

**On google colab**

You can run this `notebook <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/notebooks/demo_deep_cinac_training.ipynb>`_
using `google colab <https://colab.research.google.com>`_.

**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/general/demo_deepcinac_training.py>`_. 


See code below to see how to predict cell type after you have trained a classifier or using the one we provide. 

More information in our `documentation <https://deepcinac.readthedocs.io/en/latest/tutorial_training.html>`_.


Inferring neuronal activity
---------------------------

The classifier takes as inputs the motion corrected calcium imaging movie and spatial footprints of the sources (cells).

The outputs are float values between 0 and 1 for each frame and each source,
representing the probability for a cell to be active at that given frame.

The classifier we provide was trained to consider a cell as active during the rise time of its transients.

**On google colab**

you can run this `notebook <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/notebooks/demo_deepcinac_predictions.ipynb>`_.


**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/general/demo_deepcinac_predictions.py>`_. 

More information in our `documentation <https://deepcinac.readthedocs.io/en/latest/tutorial_predictions.html>`_.


Predicting cell type
--------------------

The classifier takes as inputs the motion corrected calcium imaging movie and spatial footprints of the sources (cells).

The outputs are float values between 0 and 1 for each cell type,
representing the cell type probability of a given cell.

We have trained a classifier on two cell type interneurons and pyramidal cells. For training, interneurons were identified using GadCre mouse while pyramidal cell were putative. 

A .yaml file allows the user to set the cell types he wants to use.

We are currently improving the classifier. 

**On google colab**

you can run this `notebook <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/notebooks/demo_deepcinac_predictions.ipynb>`_.


**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/general/demo_deepcinac_predictions.py>`_. 

More information in our `documentation <https://deepcinac.readthedocs.io/en/latest/tutorial_predictions.html>`_.


Evaluating the performance of your classifier
---------------------------------------------

To evaluate a classifier, you will need some .cinac files (produced using the GUI) with ground truth that have not been used to train your classifier.

An overview of the code for evaluating the cell type classifier performance is provided below. 

.. code::

    cinac_dir_name = os.path.join(data_path, "cinac_cell_type_ground_truth", "for_testing")

    evaluate_cell_type_predictions(cinac_dir_name, cell_type_yaml_file, results_path,
                               json_file_name, weights_file_name, 
                               save_cell_type_distribution=True)



The code for evaluating the activity classifier performance will be provided soon. 


**On google colab**

you can run this `notebook <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/notebooks/demo_deepcinac_predictions.ipynb>`_.


**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/-/blob/master/demos/general/demo_deepcinac_predictions.py>`_. 

More informations in our `documentation <https://deepcinac.readthedocs.io/>`_.


Generating simulated calcium imaging movies
-------------------------------------------

**On google colab**

If you just want to generate simulated calcium imaging movie you can run
`this notebook <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/notebooks/deepcinac_simulated_movie_generator.ipynb>`_
using `google colab <https://colab.research.google.com>`_.

**On your local device**

You can follow the steps described in `this demo file <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/general/demo_deepcinac_simulated_movie_generator.py>`_.

**Examples**
You can download examples of simulated movies `here <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/data/simulated_movies>`_.


