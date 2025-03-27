# streamlitTemplateMulti
 multi themed streamlit webApp

 **Basic Idea:**
 * template for [streamlit](https://streamlit.io) webApps

 Check requirements file for necessary libraries

 ---

## Structure pages

*mainApp*: main file to run

## Core code
in *core* directory

*app*: app class and basic structure

*page*: page class and basic structure

*stInfrastructure*: useful wrappers for streamlit functions

## Core pages:

in *corePages* directory

*appSettings*: Placeholder for app settings

*broomCupboard*: Debug page _a.k.a._ "Broom Cupboard" containing session state cache info

## User content pages:

in *userPages* directory

*themeA*: two example pages

 - page1 includes some *stInfrastructure* examples

*themeB*: three example pages

*themeC*: one example page

 - page1 includes *hack_file* uploader 

---

## Adding content

See example page for template structure.
The procedure is as follows:

1. make a sub-directory in *userPages* - this will be a new theme

2. add files to theme directory

---

## Running locally

Run webApp locally:

* get required libraries:
> python3 -m pip install -r requirements.txt

* run streamlit:
> streamlit run mainApp.py

* open browser at ''localhost:8501''

---

## Running via Docker

Either of two files can be used to build basic templates (structural files):

__build image__

> docker build . -f dockerFiles/Dockerfile -t new-app

The build will copy directories and files in the _userPages_ directory into the image and use these as content for the webApp.

__run container__

> docker run -p 8501:8501 new-app

* -p argument used to map ports (native:container)

Open browser at ''localhost:8501''

---

## Running with mounted volumes

This allows changes to files in mounted directory to be propagated to container immediately (*i.e.* without docker rebuilds) - useful for development!
**NB** this will overwrite any files in linked directory:

> docker run -p 8501:8501 -v $(pwd)/userPages:/code/userPages new-app

* -v argument used to map volumes (native:container)
