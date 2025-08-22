import fltk
import sys

window = fltk.Fl_Window(610, 300)
window.label("Level Maker")

btn_labels = ["W", "P", "K", "D", "F", ""]

def change_label(widget):
  current_label = widget.label()
  try:
    idx = btn_labels.index(current_label)
  except ValueError:
    idx = len(btn_labels) - 1
  new_idx = (idx + 1) % len(btn_labels)
  widget.label(btn_labels[new_idx])

title = fltk.Fl_Box(5, 5, 600, 25, "Level Maker")
title.box(fltk.FL_NO_BOX)
title.labelsize(24)

instructions = fltk.Fl_Box(5, 30, 600, 50, "W: Wall  P: Player\nK: Key  D: Door  F: Flag")
instructions.box(fltk.FL_NO_BOX)
instructions.labelsize(12)

btns = []

def save_level(widget):
  cols = []
  for col in btns:
    row = [w.label() for w in col]
    row = [cell if cell != "" else "I" for cell in row]
    cols.append(row)
  save_text = "\n".join("".join(row) for row in cols)
  with open("level.txt", "w", encoding="utf-8") as f:
    f.write(save_text)
  print(f"Saved level!\n{save_text}")

for r in range(5):
  row_btns = []
  for c in range(30):
    if r == 0 or r == 4 or c == 0 or c == 29:
      btn = fltk.Fl_Button(5 + (c * 20), 100 + 5 + (r * 20), 20, 20, "W")
      btn.deactivate()
    else:
      btn = fltk.Fl_Button(5 + (c * 20), 100 + 5 + (r * 20), 20, 20, "")
      btn.callback(change_label)
    btn.clear_visible_focus()
    row_btns.append(btn)
  btns.append(row_btns)

save_btn = fltk.Fl_Button(610 - 5 - 50, 300 - 5 - 30, 50, 30, "Save")
save_btn.callback(save_level)

window.end()
window.show(sys.argv)
fltk.Fl.run()