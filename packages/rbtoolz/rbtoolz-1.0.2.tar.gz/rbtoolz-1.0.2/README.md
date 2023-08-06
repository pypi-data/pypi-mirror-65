# RBToolz

RBToolz is a package of generic analytics tools for use in Jupyter Notebooks that currently cover:

  - Postprocessing
  - Timeseries Manipulation
  - Data Sources

### Tech

RBToolz uses a number of open source projects to work properly:

* Jupyter Notebook
* Pandas
* Numpy
* Plotly
* Yahoo Finance

### Installation
Install uning regular pip 3.7

```sh
$ pip install rbtoolz
```
### Notebook Setup and Plotting Example

Following steps are required to setup notebook and use postprocessing tools

* Notebook Cell HTML changes

```python
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
```

* Plotly offline functions
```python
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
```
* Import auto_plot from RBToolz
```python
from rbtoolz.plotting import auto_plot
```
* Finally run a demo
```python
df = pd.DataFrame([1,2,3],['A','B','C'])
fig = auto_plot(df)
iplot(fig)
```

License
----

MIT




