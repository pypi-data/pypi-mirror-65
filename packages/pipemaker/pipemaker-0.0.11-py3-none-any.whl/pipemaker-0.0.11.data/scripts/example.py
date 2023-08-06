# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Simple example

# %% [markdown]
# ## Create the pipeline
#
# The example application is based on a pipeline to analyse online news media. It runs using pipemaker but uses minimal, dummy functions for illustration of pipemaker. The real application on which it was based is "compass" which can be installed separately if required.

# %%
# notebook settings
from pipemaker.utils.ipstartup import *
import shutil

# pipemaker package
from pipemaker.master import env, pipeline as p

# example application
from pipemaker import example
from pipemaker.example import *

# %%
p.stop()
p.start()

# %%
# reset the data so it runs from scratch
shutil.rmtree("pipedata", ignore_errors=True)

# %% [markdown]
# One line of code to create a pipeline from all the functions in the "example" module.

# %%
p.add(example)

# %% [markdown]
# Configure the job:
#
# * All files from this run will be under pipedata/sun
# * The web search will be carried out using the domain parameter

# %%
env.fvars.job = "sun"
env.params.domain = "sun.co.uk"

# %% [markdown]
# One line of code shows the upstream pipeline for any task using the current "pipe" variables
#
# * The pipeline has been created automatically linking inputs and outputs.
# * Known parameters and existing files are shown in green.
# * Missing parameters and files are shown in white.
# * When we run a function it will automatically run the upstream pipeline to generate input files

# %%
make_docs.view()

# %% [markdown]
# ## Run the pipeline

# %%
make_texts()

# %% [markdown]
# If we now look at the pipeline we see only what remains to be run; files already created are in green; and the upstream functions that are already completed are no longer shown

# %%
make_articles.view()

# %% [markdown]
# To see the full upstream pipeline set parents=True......which shows everything from "texts" upstream is green.

# %%
make_docs.view(parents=True)

# %% [markdown]
# We can load the contents of any item in green

# %%
p.load("articles")

# %% [markdown]
# Now when we run make_docs it only needs to run the functions that have not already been successful.

# %%
make_docs()

# %% [markdown]
# Now the final output is green and complete

# %%
make_docs.view()

# %%
