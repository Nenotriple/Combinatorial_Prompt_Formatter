import tkinter as tk

def format_string():
    primary_tokens = [entry.get() for entry in primary_entries if entry.get()]
    secondary_tokens = [[entry.get() for entry in entries if entry.get()] for entries in secondary_entries]
    if secondary_only_mode:
        formatted_string = '{' + '|'.join([f'{secondary_tokens_str(entry)}' for entry in secondary_tokens if entry]) + '}'
    else:
        formatted_string = '{' + '|'.join([f'{primary}, {{{"|".join(secondary)}}}' for primary, secondary in zip(primary_tokens, secondary_tokens) if primary and secondary]) + '}'
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, formatted_string)

def secondary_tokens_str(tokens):
    return '|'.join([token for token in tokens if token])

secondary_only_mode = False

def toggle_mode():
    global secondary_only_mode
    secondary_only_mode = not secondary_only_mode
    if secondary_only_mode:
        toggle_button.config(text="Current mode: Secondary Only")
    else:
        toggle_button.config(text="Current mode: Primary + Secondary")
    format_string()

def clear_all():
    for entry in primary_entries:
        entry.delete(0, tk.END)
    for entries in secondary_entries:
        for entry in entries:
            entry.delete(0, tk.END)
    result_text.delete('1.0', tk.END)

def on_focus_in(event):
    format_string()

def on_tab(event):
    format_string()
    event.widget.tk_focusNext().focus()
    return 'break'

def copy_output():
    root.clipboard_clear()
    result = result_text.get("1.0", tk.END)
    root.clipboard_append(result.rstrip('\n'))

def on_alt_arrow(event):
    if event.keysym == 'Left':
        event.widget.tk_focusPrev().focus()
    elif event.keysym == 'Right':
        event.widget.tk_focusNext().focus()
    elif event.keysym == 'Up':
        index = primary_entries.index(event.widget) if event.widget in primary_entries else None
        if index is not None and index > 0:
            primary_entries[index-1].focus()
        else:
            index = [i for i, entries in enumerate(secondary_entries) if event.widget in entries]
            if index:
                row, col = index[0], secondary_entries[index[0]].index(event.widget)
                if row > 0:
                    secondary_entries[row-1][col].focus()
    elif event.keysym == 'Down':
        index = primary_entries.index(event.widget) if event.widget in primary_entries else None
        if index is not None and index < len(primary_entries)-1:
            primary_entries[index+1].focus()
        else:
            index = [i for i, entries in enumerate(secondary_entries) if event.widget in entries]
            if index:
                row, col = index[0], secondary_entries[index[0]].index(event.widget)
                if row < len(secondary_entries)-1:
                    secondary_entries[row+1][col].focus()
    return 'break'

root = tk.Tk()
root.minsize(1775, 225)
root.maxsize(1775, 380)
root.title("Dynamic Prompt - Combinatorial Formatter        --Alt+arrow keys quickly shift between columns/rows--  --Add multiple tokens to any field seperated by a comma and space--")

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
    primary_entry.bind("<Alt-Left>", on_alt_arrow)
    primary_entry.bind("<Alt-Right>", on_alt_arrow)
    primary_entry.bind("<Alt-Up>", on_alt_arrow)
    primary_entry.bind("<Alt-Down>", on_alt_arrow)
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
        secondary_entry.bind("<Alt-Left>", on_alt_arrow)
        secondary_entry.bind("<Alt-Right>", on_alt_arrow)
        secondary_entry.bind("<Alt-Up>", on_alt_arrow)
        secondary_entry.bind("<Alt-Down>", on_alt_arrow)
        secondary_entries_row.append(secondary_entry)
    secondary_entries.append(secondary_entries_row)

button_frame = tk.Frame(root)
button_frame.grid(row=7,column=0,columnspan=4)

format_button = tk.Button(button_frame, text="Format String", command=format_string)
format_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all, fg='red')
clear_button.pack(side=tk.LEFT, padx=5)

copy_button = tk.Button(button_frame,text="Copy Output",command=copy_output)
copy_button.pack(side=tk.LEFT, padx=5)

toggle_button = tk.Button(button_frame, text="Current mode: Primary + Secondary", command=toggle_mode)
toggle_button.pack(side=tk.LEFT, padx=5)

result_text = tk.Text(root,height=12,width=None,wrap=tk.WORD)
result_text.grid(row=8, column=0, columnspan=4, sticky=tk.EW)

for i in range(4):
    root.columnconfigure(i, weight=1)

root.mainloop()
