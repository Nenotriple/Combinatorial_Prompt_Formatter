import tkinter as tk

def format_string():
    primary_tokens = [entry.get() for entry in primary_entries if entry.get()]
    secondary_tokens = [[entry.get() for entry in entries if entry.get()] for entries in secondary_entries]
    formatted_string = '{' + '|'.join([f'{primary}, {{{"|".join(secondary)}}}' for primary, secondary in zip(primary_tokens, secondary_tokens) if primary and secondary]) + '}'
    result_entry.delete(0, tk.END)
    result_entry.insert(0, formatted_string)

def clear_all():
    for entry in primary_entries:
        entry.delete(0, tk.END)
    for entries in secondary_entries:
        for entry in entries:
            entry.delete(0, tk.END)
    result_entry.delete(0, tk.END)

def on_focus_in(event):
    format_string()

def on_tab(event):
    format_string()
    event.widget.tk_focusNext().focus()
    return 'break'

root = tk.Tk()
root.minsize(1775, 210)
root.maxsize(1775, 210)
root.title("Dynamic Prompt - Combinatorial Formatter        --Additional tokens can be separated with a comma and space. 'token1, token2, token3'")

primary_label = tk.Label(root, text="Primary Tokens")
primary_label.grid(row=0, column=0, columnspan=2)

separator_label = tk.Label(root, text="  ")
separator_label.grid(row=0, column=2)

secondary_label = tk.Label(root, text="Secondary Tokens")
secondary_label.grid(row=0, column=3, columnspan=2)

primary_entries = []
secondary_entries = []

pastel_colors = ["#FFF2E6", "#F2F8E6", "#E6F2F8", "#F8E6F2", "#E6E6F8", "#F8E6E6"]

for i in range(6):
    primary_entry = tk.Entry(root, width=50)
    primary_entry.grid(row=i+1, column=0, columnspan=2)
    primary_entry.configure(bg=pastel_colors[i])
    primary_entry.bind("<FocusIn>", on_focus_in)
    primary_entry.bind("<Tab>", on_tab)
    primary_entries.append(primary_entry)

    separator_label = tk.Label(root, text="  ")
    separator_label.grid(row=i+1, column=2)

    secondary_entry_frame = tk.Frame(root, width=75)
    secondary_entry_frame.grid(row=i+1, column=3, columnspan=2)
    root.columnconfigure(3, weight=1)
    secondary_entries_row = []
    for j in range(6):
        secondary_entry = tk.Entry(secondary_entry_frame, width=40)
        secondary_entry.pack(side=tk.LEFT)
        secondary_entry.configure(bg=pastel_colors[i])
        secondary_entry.bind("<FocusIn>", on_focus_in)
        secondary_entry.bind("<Tab>", on_tab)
        secondary_entries_row.append(secondary_entry)
    secondary_entries.append(secondary_entries_row)

button_frame = tk.Frame(root)
button_frame.grid(row=7,column=0,columnspan=4)

format_button = tk.Button(button_frame, text="Format String", command=format_string)
format_button.pack(side=tk.LEFT)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all)
clear_button.pack(side=tk.LEFT)

result_entry = tk.Entry(root)
result_entry.grid(row=8, column=0, columnspan=4, sticky=tk.EW)

for i in range(4):
    root.columnconfigure(i, weight=1)

root.mainloop()
