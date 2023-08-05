# I know this looks like Tkinter, its kinda hard not to make it look Tk, and I was kind of inspired by Tk....

class newpage: # The VERY base class in Ebuilder Ultra Core, This handles all the HTML in a page and all other Ebuilder Components are associated with it
    def __init__(self, name, title=None):
        # Inititate All the variables and write boilerplate HTML to the file
        if title==None:
            title = f"{name}.html"

        self.title = title
        self.page = f"{name}.html"
        self.buffer = []
        self.buffer.append(f"""<!DOCTYPE html> 
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>{title}</title>
  </head>
  <body>
  """)
        open(self.page, "w+").close()

    def commit(self): # My fancy way of letting the user empty and add the buffer to a file (Inspired by git)
        with open(self.page, "a+") as f:
            f.write(''.join(self.buffer))
            self.buffer = []

    def final_commit(self):
        self.buffer.append('''
  </body>
</html>
    ''')
        self.commit()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.final_commit()
        
class EbuilderTextComponent: # A simple class used to define text components
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, page, text):
        self.page = page
        self.text = text
        self.html = f"<{self.tag}>{text}</{self.tag}>"
        page.buffer.append(self.html)
        self.index = page.buffer.index(self.html)
        self.style = ""
        return self

    def style_it(self):
        self.html = f'<{self.tag} style="{self.style}">{self.text}</{self.tag}>'
        self.page.buffer[self.index] = self.html

    def center(self):
        self.style += 'text-align: center; '
        self.style_it()

    def font(self, font):
        self.style += f"font-family: {font}; "
        self.style_it()

    def color(self, color):
        self.style += f"color: {color}; "
        self.style_it()

header = EbuilderTextComponent("h1") # VERY SIMPLE COMPONENT DEFINITIONS
paragraph = EbuilderTextComponent("p")