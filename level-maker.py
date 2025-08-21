import tkinter as tk

root = tk.Tk()
root.title("Level Maker")

instructions_label = tk.Label(root, text="")

btn_names = ["W", "P", "K", "D", ""]

btns = []

def change_type(button):
  current_text = button["text"]
  try:
    idx = btn_names.index(current_text)
  except ValueError:
    idx = len(btn_names) - 1
  new_idx = (idx + 1) % len(btn_names)
  button.config(text=btn_names[new_idx])

for r in range(5):
  row_btns = []
  for c in range(30):
    btn = tk.Button(root, width=2, text="", justify="center", command=lambda btn=None: None)
    btn.grid(row=r+1, column=c, padx=2, pady=2)
    row_btns.append(btn)
  btns.append(row_btns)

for r in range(5):
  for c in range(30):
    btn = btns[r][c]
    if r == 0 or r == 4 or c == 0 or c == 29:
      btns[r][c].config(text="W", state=tk.DISABLED)
    else:
      btn.config(command=lambda b=btn: change_type(b))

root.mainloop()