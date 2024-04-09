# Clustering Algorithms for the Study of Credit Ratings and of their Coherence with Raw Financial Data - Source Code

This project and its source code, the content of this repository, was realised in the context of my Final Year Individual Project as part of my Computer Science (AI) with Magement (BSc.) at King's College London. In this file, you will find a quick description of the paper, guides for installing, running, and testing its source code, and a qukc description of the raw analysis files present alongside the code in this repository.

## Project Presentation - Abstract

Credit ratings play a vital role in the Financial systems. They enable financial actors to raise financing through debt, Financial institutions to invest in such debt, and regulators to regulate the debt contract thereby created. In our paper, we will focus on corporate credit ratings.

This project explores the coherence of these corporate credit ratings with companies' credit-worthiness-related financial data. We leverage a diverse set of clustering algorithms in a strictly unsupervised manner thanks to two intrinsic measures of cluster quality. By analysing the results of these algorithms, we conclude on the important role of human judgment in the credit rating methodology and on the incoherence of its result (a partition of companies under a set of letter grades) with the results of our strictly data-based approaches. We additionally hint at the financial relevance of incorporating such unsupervised, explainable, methods into credit rating methodologies.

## Installation

To install the software, simply clone the repository. Once cloned, you can download all required dependencies by running:

```
pip install -r requirements.txt
```

(We recommend doing so after both creating and activating a virtual environment).

## Running the system

### System Requirements

We require a version of Python 3.11. We personally used Python 3.11.5.

### Command-Line Interface

We designed a minimal user interface that enables you to interact with our program through the command line. This interface presents key information and progress tracking while our system is running. Additionally, it enables you to select the set of data configurations they want to study as well as the depth of said study thanks to the following commands:

- To run the system in its default configuration, you should set up the virtual environment (see Code appendix) and run `python main.py`
- To set which set of DataConfiguration objects to run without applying PCA to them, they can append the `-non_pca_configs` command followed by the name of a set of data configurations (see below).
  - To set which set of DataConfiguration objects to run with prior application of PCA, they can append the `-pca__configs` command followed by the name of a set of data configurations (see below).
  - To run only the Cluster Analysis and skip the Hyperparameter Search, they can append the `-analysis_only` command
  - To skip the running of PCA, they can apply the `-skip_pca` command.

As part of this interface, you can choose amongst different sets of data configurations. These sets are:

- RAW NUMBERS AND RATIOS: several configurations are then used presenting a combination of raw financial data and financial ratios about each company. We consider these configurations as less relevant.
- CREDIT HEALTH AND CREDIT MODEL: several configurations are then used presenting a combination of raw financial data and ratios used by S\&P to assess Credit Health and run their Credit Model. We consider these configurations as more relevant.
- INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL: several configurations are then used presenting a combination of raw financial data and ratios used by S\&P to assess Credit Health and run their Credit Model. Only the data sets created are specific to a single industry
- ALL: the combination of the two sets mentioned above.
- CREDIT HEALTH AND CREDIT MODEL - COMPLEX: the combination of the ``CREDIT HEALTH AND CREDIT MODEL" set of configurations and of configurations presenting raw financial data and ratios used by S\&P to assess Credit Health and run their Credit Model then aggregated by key pillars of credit rating (see technique in 6.1.1).
- INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL - COMPLEX: the combination of the ``INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL" set of configurations and of configurations applied on the same industry-specific data sets but aggregating features by key pillars of credit ratings.
- INDUSTRY SPECIFIC \& CREDIT HEALTH AND CREDIT MODEL: a combination of the `INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL" and `CREDIT HEALTH AND CREDIT MODEL" sets of configurations.
- INDUSTRY SPECIFIC \& CREDIT HEALTH AND CREDIT MODEL - COMPLEX: a combination of the `INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL - COMPLEX" and `CREDIT HEALTH AND CREDIT MODEL" sets of configurations.
- ALL - COMPLEX: the combination of `CREDIT HEALTH AND CREDIT MODEL - COMPLEX", `INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL - COMPLEX" and ``RAW NUMBERS AND RATIOS"

By default, analysis is conducted both on the `INDUSTRY SPECIFIC \& CREDIT HEALTH AND CREDIT MODEL" configurations after the application of PCA, and on the `INDUSTRY SPECIFIC \& CREDIT HEALTH AND CREDIT MODEL - COMPLEX" without application of PCA. This will lead to the hyperparameter optimisation and cluster analysis for 1184 different combinations of algorithms, data configurations, and optimisation condition (optimal objective function, constrained to number cluster equal to the number of credit ratings, or constrained to number cluster greater than the number of credit ratings)

> **_NOTE:_** Do not pay attention to the "Mean of empty slice" runtime warnings, they are the consequence of having too many undefiend values in a row but the issue is automaitcally erased by our mechanism for removing undefined values.

## Testing the system

You can run the entire test suite with the command:

```
coverage run -m unittest discover -p 'test_*'
```

This command will also generate an analysis of the test coverage, which we recommend accesssing by first executing:

```
coverage html
```

Before opening the `htmlcov/index.html` file.

If you want to run only a particular test file. You can do so with the command

```
python unittest tests/unit_tests/<rest of the path to the file>
```

## Quick Descrption of Analysis Files

This folders in this repository also hold an important number of files (both textual and images) which were produced during our last run of the system in its default configurations. Should you wish to consult them, here is some key information:

- The `/hyperparameter_optimisation_results` contains the results of our Hyperparemeter Optimisation process. These results are divided in 2 folders, one containg the results for all those data configurations which required the running of PCA, the other for all others data configurations. In each one of them you will find folders, each containing the graphs produced during the optimal hyperparameter search process for a given data configuration (giving its name to the particular folder). You will additionally find a `performance_metrics.json` file presenting all the final results.
- The `/clusters_content_analyses` contains the results of our Cluster Analysis. These results are divided in 2 folders, one containg the results for all those data configurations which required the running of PCA, the other for all others data configurations. They each contain a series of folders, one for each data configuration studied. In each one of these subfolders, you will find:
  - a `.json` file containing the analysis of the clusters produced by a given algorithm (which name is specified in the file name), possibly under a specific set of optimal hyperparameters (for BIRCH and DBSCAN). During the analysis of these files, you may struggle to make the connection between the cluster numbers as expressed throughout the files and those expressed in the `Incoherencies explanations` section. The cluster numbering in this section is based on the list of all those clusters that are signficant or that have a significant range and not on the list of all clusters produced by the algorithm (which is the case everywhere else in the file). We will be working on a fix to make reading the file easier.
  - a `.jpeg` for each such analysis presenting a visualisation of the clusters produced
