from ebuilder.ebuilder_core import *
from inspect import getsource

def page(func):
    def wrapper():
        file = func.__name__ # get name of the func
        code = getsource(func) # get source code of the func
        code = code.split("\n") # split the source code into a list by line
        del code[0] # delete the decorator so it doesn't call this again and again and again...
        code.insert(0, "from ebuilder.ebuilder_core import *") # Make sure it imports ebuilder core
        code.insert(2, f"    {file} = newpage('{file}')") # Add a line that will create a new html page with ebuilder core 'newpage'
        code.append(f"{file}()") # Append the function call so the code we edited will be called
        code.insert(-1, "    {file}.final_commit()") # Add the final commit line so it will close the html file
        code = '\n'.join(code) # Put the code back into a Python function format
        exec(code) # execute the edited code
        
    return wrapper() # Run the function with all the edits