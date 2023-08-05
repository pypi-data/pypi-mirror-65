
![medium_logo](https://raw.githubusercontent.com/rediscovery-io/remo-python/master/img/remo_normal.png)

# Remo annotation tool


Remo is a web-application for managing and visualising images and annotations.

It was developed for data scientists, engineers and ML researchers to facilitate
the exploration, sharing and management of datasets and annotations for Computer Vision.

Remo can be called from code or used directly from the User Interface.

Use Remo to:

- **visualise and inspect** datasets, annotations and predictions
- **search and organise images** by classes or tags
- **visualise statistics** like # objects per class
- **quickly annotate** your images

Remo runs on Windows, Linux and Mac.
It is written using Python and React.JS and uses a lightweight database to store metadata.

- - -

## Python commands
Here is an example of using the Python library to:

- crate a dataset
- upload annotations
- visualise statistics on annotations
- search for specific images

Simple workflow:

``` python
import remo

# create dataset
my_dataset = remo.create_dataset(name = 'open images test',
                            urls = ["https://remo-scripts.s3-eu-west-1.amazonaws.com/open_images_sample_dataset.zip"],
                            annotation_task="Object detection")

# list existing datasets                
remo.list_datasets()

# browse the dataset
my_dataset.view()

my_dataset.list_images()

# view stats
my_dataset.view_annotation_statistics()

# annotate
my_dataset.view_annotate()



```

---

## Installation
Remo is compatible with **Python 3.6+** and runs on **Linux, macOS and Windows**. The latest remo releases are available over <a href="https://pypi.org/project/remo/" target="_blank">pip</a>.


!!! info
    Remo is a web-server running on your local machine.
    Once Remo is running, you can call it from code in most programming languages through the REST API.
    We provide an <a href="https://github.com/rediscovery-io/remo-python" target="_blank">open source Python SDK]</a> to facilitate calling remo from Python 3.5+ environments.


### 1. Pip install
You can install remo using `pip`, preferably in a conda environment.

``` bash
# Optional - create and activate a python 3.6 conda environment
conda create -n remo_env python=3.6
conda activate remo_env

pip install remo
```

When installed in a <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">conda environment</a>, remo will launch automatically when calling  `import remo`.

Conda also comes pre-installed with SQLlite binaries, and allows you to easily specify the right python version.
If you install remo outside a conda environment, remo will check whether you have SQLlite binaries installed and install them otherwise.

###2. Initialise
To complete the installation, run:

``` bash
python -m remo_app init
```

This will create a folder .remo in your home directory. By default, this is the location where Remo looks for its configuration file, **remo.json**.


###3. Optional: separate python library

Remo comes pre-installed with our python library. Optionally, you can also install the python library in a separate Python environment from where you installed remo

``` bash
# First activate your Python work environment
pip install remo-sdk
```

---
## Launch remo

To launch the web app, run from command line:

``` bash
python -m remo_app
```

Alternatively, if you have installed Remo in a conda environment, from python you can directly call `#!python import remo`. This will check if the app is running, or launch it otherwise.

Remo will be served by default in its own Electron app. But you can also access it through your browser at localhost:8123

![](https://remo.ai/docs/img/remo_preview.PNG)

---
## Support

In case you need support or want to give us some precious feedback, you can get in touch with us at:

 `#!css hello AT remo DOT ai`
