# Uncertainty Modelling Coursework
Completed in 2023 for year 1, teaching block 1 of my Interactive Artificial Intelligence PhD. 

The coursework is to implement some basic concepts from Fuzzy Set Theory in Python. 

## Using this Repo
To see the code being used, you can simply open the [demo.ipynb](https://github.com/JonathanRaines/phd-um-coursework-fuzzy-sets/blob/main/demo.ipynb) Jupyter Notebook. GitHub renders this statically, although you won't be able to run the cells. 

The notebook uses the [fuzzy_sets package](https://github.com/JonathanRaines/phd-um-coursework-fuzzy-sets/tree/main/fuzzy_sets) (written for this coursework). The [documentation](https://jonathanraines.github.io/phd-um-coursework-fuzzy-sets/) is hosted here on GitHub pages. You can look through the source code in the "fuzzy_sets" folder of this repo. 

If you want to use the code, follow one of the options in the Installations section.
[main.py](https://github.com/JonathanRaines/phd-um-coursework-fuzzy-sets/blob/main/main.py) runs all the functions in [demo.ipynb](https://github.com/JonathanRaines/phd-um-coursework-fuzzy-sets/blob/main/demo.ipynb) and prints the output. 

# Installation
Clone this repo, there are no external dependencies. `requirements-dev.txt` only lists [pytest](https://docs.pytest.org/en/7.4.x/) which is only needed for running unit tests, not for using the code itself. 

Alternatively, 

`pip install git+https://github.com/JonathanRaines/phd-um-coursework-fuzzy-sets.git@main`