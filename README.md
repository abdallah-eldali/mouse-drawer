### NOTE

This project is still in progress, you can still run it by cloning the repository, and run `pipenv install requirements.txt` (to install the dependencies to run the program), and then execute `gui.py`


### TODO:

* Show the failed attemped at using a transparent hole in a window in the readme file and initial idea
* Remove the \mouse directory from git
* Explain why the whole window is translucent, and how you can't change the opacity of a specific widget in the window in tkinter
* NOTE: I was deciding to do a class for the whole cardinal points. but decided to scrap that idea and instead did a module since it's the Pythonic way while the former is more akin to Java style programs


PRIORITIES:

1. Work on `test2.py` (make it modular, maybe a class)
   1. WHY IS IT BEING DRAWN SO SMALL?
2. Create a way to stop the mouse script
3. Integrate it with the GUI, so the GUI can simply pass the picture and the location to start drawing from