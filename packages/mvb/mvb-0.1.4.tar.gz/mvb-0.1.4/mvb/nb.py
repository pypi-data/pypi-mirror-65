import os
# 3rd party modules
import papermill as pm
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
from IPython.core.display import display, HTML, Markdown
# internal modules
import mvb.pdh as pdh
import mvb.g as g

def defaults(**kwargs):
  """
  calls mvb.pdh.set_options() and passes along any arguments

  @input full_width: bool, default true
  @input show_all_rows: bool, default true
  @input show_all_cols: bool, default true
  @input show_full_col: bool, default true
  """
  full_width()
  pdh.set_options(**kwargs)

def full_width():
  """
  insert html to set container width to 100%
  """
  display(HTML("<style>.container { width:100% !important; }</style>"))

def nb_to_html(nb,
               exclude_input=True,
               exclude_prompts=True):
  """
  convert notebook to html
  
  @input nb : notebook
  @input exclude_input (bool default:True) : exclude input cells from output
  @input exclude_prompts (bool default:True) : exclude prompts from ouput
  
  @returns string : html body
  """
  html_exporter = HTMLExporter()
  html_exporter.exclude_input = exclude_input
  html_exporter.exclude_input_prompt = exclude_prompts
  html_exporter.exclude_output_prompt = exclude_prompts
  (body, _) = html_exporter.from_notebook_node(nb)
  return body

def publish(input_ipynb_path,
            output_dir=None,
            output_name=None,
            parameters={},
            output_html=True,
            output_ipynb=False,
            exclude_input=True,
            exclude_prompts=True):
  """
  "publish"es a notebook, by executing it with optional papermill `parameters`,
  converting result to html, 

  @input input_ipynb_path: path to input ipynb notebook to execute
  @input output_dir: string, optional: path to save output, defaults current directory
  @input output_name: string, optional: name for output ipynb and html files, defaults input notebook name + parameters
  @input parameters: dict, optional: values to override notebook values in cell tagged `parameters` (papermill)
  @input output_html: bool, optional, defaults True: option to create output html
  @input output_ipynb: bool, optional, default False: option to keep conveted ipynb
  @input exclude_input: bool, optional, default True: option to exclude ipython input (code) cells from html output
  @input exclude_prompts: bool, optional, default True: option to exclude prompts (In[ 1 ]) from html output
  
  @returns: dict of {name, output_ipynb_path, output_html_path}
  """
  if output_dir == None:
    output_dir = '.'# os path to current directory?
  if output_name == None:
    notebook_base_name = input_ipynb_path.split('/')[-1].replace('.ipynb','')
    params_string = g.dict_to_file_name(parameters)
    output_name = f"{notebook_base_name}.{params_string}"
  output_ipynb_path=f"{output_dir}/{output_name}.ipynb"
  pm.execute_notebook(
    input_ipynb_path,
    output_ipynb_path,
    parameters
  )
  if output_html:
    output_html_path = f"{output_dir}/{output_name}.html"
    output_ipynb_nb = nbformat.read(output_ipynb_path, as_version=4)
    html = nb_to_html(output_ipynb_nb,
                      exclude_input=exclude_input,
                      exclude_prompts=exclude_prompts)
    f = open(output_html_path, "w")
    f.write(html)
    f.close()
  if not output_ipynb:
    os.remove(output_ipynb_path)
  return dict(
    name=output_name,
    output_ipynb_path=output_ipynb_path if output_ipynb else None,
    output_html_path=output_html_path
  )

def index_item(item):
    """
    @item: tuple (id, name)
    """
    return f'<li><a href="#{item[0]}">{item[1]}</a></li>'

def index(items):
    """
    @input items: list of tuples: (id, name)
    """
    css = """
    <style>
    #index{
        position: fixed;
        display:block;
        top: 120px;
        left: 10px;
        z-index: 1000000;
        background-color: white;
        border: 1px solid black;
        padding: 1em;
    }
    </style>"""
    items_html = '\n'.join(list(map(index_item,items)))
    
    display(HTML(f"""
    {css}
    <div id="index">
        <h2>Index</h1>
        <ul>
            {items_html}
        </ul>
    </div>
    """))

def heading(item):
    """
    @item: tuple (id, name)
    """
    return display(HTML(f'<h1 id={item[0]}>{item[1]}</h1>'))
