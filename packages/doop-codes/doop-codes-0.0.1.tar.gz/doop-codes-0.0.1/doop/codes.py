from IPython.core.magic import (register_line_magic, register_cell_magic)
from IPython.display import IFrame,display
import sys

__doop_python_version = sys.version_info[0]

if __doop_python_version == 2:
    import urllib as my_urllib
else:
    import urllib.parse as my_urllib

def prepare_doop():
    python_version = sys.version_info[0]
    if python_version == 2:
        import urllib as my_urllib
    else:
        import urllib.parse as my_urllib
        
        
def generate_query_url(command, query):
    escaped_query = my_urllib.quote_plus(query)
    return "http://doop.codes/search?q={}&cmd={}&python={}".format(escaped_query,command,__doop_python_version)


@register_line_magic
def doop(line):
    print("doop searching (just wait a second)")
    site_p = generate_query_url("jupyer_line_magic_doop", line)
    display(IFrame(site_p, width="100%",  height="600"))
        
@register_cell_magic
def doop(line, cell):
    print("doop searching (just wait a second)")
    site_p = generate_query_url("jupyer_cell_magic_doop", line + " " + cell)
    display(IFrame(site_p, width="100%",  height="600"))
        
prepare_doop()

# def doop(line, cell):
#     site_p = generate_query_url(command, line + cell)
#     display(IFrame(site_p, width="100%",  height="600"))
    
# def load_ipython_extension(ipython):
#     ipython.register_magic_function(doop, 'cell')
# #    ipython.register_magic_function(doop2, 'line')