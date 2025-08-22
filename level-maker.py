import dearpygui.dearpygui as dpg

win_width, win_height = 850, 300

dpg.create_context()
dpg.create_viewport(title="Level Maker", width=win_width, height=win_height)
dpg.setup_dearpygui()
dpg.show_viewport()

btn_names = ["W", "P", "K", "D", "F", ""]
btns = []

def save_callback():
  cols = []
  for col in btns:
    row = [dpg.get_item_label(r) for r in col]
    row = [cell if cell != "" else "I" for cell in row]
    cols.append(row)
  save_text = "\n".join("".join(row) for row in cols)
  with open("level.txt", "w", encoding="utf-8") as f:
    f.write(save_text)
  print(f"Saved level!\n{save_text}")

def change_type(sender, app_data, user_data):
  current_text = dpg.get_item_label(sender)
  try:
    idx = btn_names.index(current_text)
  except ValueError:
    idx = len(btn_names) - 1
  new_idx = (idx + 1) % len(btn_names)
  dpg.set_item_label(sender, btn_names[new_idx])

with dpg.window(tag="main",
                width=win_width,
                height=win_height,
                no_close=True,
                no_collapse=True,
                no_resize=True,
                no_move=True):
  dpg.add_text("Level Maker")
  dpg.add_text("How to:")
  for r in range(5):
    row_btns = []
    with dpg.group(horizontal=True):
      for c in range(30):
        tag = f"btn_{r}_{c}"
        if r == 0 or r == 4 or c == 0 or c == 29:
          btn_label = "W"
          enabled = False
        else:
          btn_label = ""
          enabled = True
        dpg.add_button(label=btn_label,
                       width=20,
                       height=20,
                       tag=tag,
                       callback=change_type if enabled else None)
        row_btns.append(tag)
    btns.append(row_btns)
  dpg.add_button(label="Save", callback=save_callback)

dpg.set_item_pos("main", [0, 0])

dpg.start_dearpygui()
dpg.destroy_context()