# Simulated annealing implementation in `python` and `C++` for the solution of the Traveling Salesman Problem (TSP)

See the post <a href="https://mirkomiorelli.github.io/SA_TSP/">Simulated Annealing and vacation planning (solving the TSP with multiple constraints)</a> for a more detailed explanation of what I have done in this repo. All the figures and the python code of the post are in the `Simulated_annealing_notebook.ipynb` jupyter notebook. The folder `images` contains all the figures and gifs included in the post. The folder `generate_gifs` contains scripts to generate gifs at different steps of the annealing schedule.

The `C++` code is (obviously) in the folder `cpp`. The folder also includes a `makefile`. To be able to compile the code and then import the created package into `python` you need to install <a href="https://github.com/pybind/pybind11">`pybind11`</a>.

The folder `datasets` contains all the files used in the post. 

And just because it is cool, here it is a nice gif:

![](http://i.imgur.com/Ssfp7.gif)
