import fltk
import sys

window = fltk.Fl_Window(300, 180)
window.label("Level Maker")

def button_callback(widget):

button_test = fltk.Fl_Button(5, 5, 20, 20, "W")

window.end()
window.show(sys.argv)
fltk.Fl.run()