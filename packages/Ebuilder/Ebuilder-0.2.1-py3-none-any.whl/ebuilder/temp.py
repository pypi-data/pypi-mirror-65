from ebuilder_core import *
def index():
    index = newpage('index')
    header(index, "OOF")
    index.commit()
    print(index.buffer)

index()