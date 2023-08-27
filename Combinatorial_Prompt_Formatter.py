import tkinter as tk

def format_string():
    first_tokens = [ent.get() for ent in first_ents if ent.get()]
    second_tokens = [[ent.get() for ent in ents if ent.get()] for ents in second_ents]
    if second_only_mode:
        formatted_string = '{' + '|'.join([f'{second_tokens_str(ent)}' for ent in second_tokens if ent]) + '}'
    else:
        formatted_string = '{' + '|'.join([f'{first}, {{{"|".join(second)}}}' for first, second in zip(first_tokens, second_tokens) if first and second]) + '}'
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, formatted_string)

def second_tokens_str(tokens):
    return '|'.join([token for token in tokens if token])
second_only_mode = False

def toggle_mode():
    global second_only_mode
    second_only_mode = not second_only_mode
    if second_only_mode:
        toggle_button.config(text="Current mode: Second Only")
    else:
        toggle_button.config(text="Current mode: First + Second")
    format_string()

def clear_all():
    for ent in first_ents:
        ent.delete(0, tk.END)
    for ents in second_ents:
        for ent in ents:
            ent.delete(0, tk.END)
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
        index = first_ents.index(event.widget) if event.widget in first_ents else None
        if index is not None and index > 0:
            first_ents[index-1].focus()
        else:
            index = [i for i, ents in enumerate(second_ents) if event.widget in ents]
            if index:
                row, col = index[0], second_ents[index[0]].index(event.widget)
                if row > 0:
                    second_ents[row-1][col].focus()
    elif event.keysym == 'Down':
        index = first_ents.index(event.widget) if event.widget in first_ents else None
        if index is not None and index < len(first_ents)-1:
            first_ents[index+1].focus()
        else:
            index = [i for i, ents in enumerate(second_ents) if event.widget in ents]
            if index:
                row, col = index[0], second_ents[index[0]].index(event.widget)
                if row < len(second_ents)-1:
                    second_ents[row+1][col].focus()
    return 'break'

def on_middle_click(event):
    if event.num == 2:
        event.widget.delete(0, tk.END)
        return "break"

root = tk.Tk()
root.minsize(1775, 225)
root.maxsize(1775, 380)
root.title("v1.03 - Dynamic Prompts: Combinatorial/Nested Formatter")

first_label = tk.Label(root, text="first Tokens")
first_label.grid(row=0, column=0, columnspan=2)

separator_label = tk.Label(root, text="  ")
separator_label.grid(row=0, column=2)

second_label = tk.Label(root, text="second Tokens")
second_label.grid(row=0, column=3, columnspan=2)

first_ents = []
second_ents = []

pastel_colors = ["#FFF2E6", "#F2F8E6", "#E6F2F8", "#F8E6F2", "#E6E6F8", "#F8E6E6"]

for i in range(6):
    first_ent = tk.Ent(root, width=50)
    first_ent.grid(row=i+1, column=0, columnspan=2)
    first_ent.configure(bg=pastel_colors[i])
    first_ent.bind("<FocusIn>", on_focus_in)
    first_ent.bind("<Tab>", on_tab)
    first_ent.bind("<Alt-Left>", on_alt_arrow)
    first_ent.bind("<Alt-Right>", on_alt_arrow)
    first_ent.bind("<Alt-Up>", on_alt_arrow)
    first_ent.bind("<Alt-Down>", on_alt_arrow)
    first_ents.append(first_ent)
    for first_ent in first_ents:
        first_ent.bind("<Button-2>", on_middle_click)
    for second_ent_row in second_ents:
        for second_ent in second_ent_row:
            second_ent.bind("<Button-2>", on_middle_click) 

    separator_label = tk.Label(root, text="  ")
    separator_label.grid(row=i+1, column=2)

    second_ent_frame = tk.Frame(root, width=75)
    second_ent_frame.grid(row=i+1, column=3, columnspan=2)
    root.columnconfigure(3, weight=1)
    second_ents_row = []
    for j in range(6):
        second_ent = tk.Ent(second_ent_frame, width=40)
        second_ent.pack(side=tk.LEFT)
        second_ent.configure(bg=pastel_colors[i])
        second_ent.bind("<FocusIn>", on_focus_in)
        second_ent.bind("<Tab>", on_tab)
        second_ent.bind("<Alt-Left>", on_alt_arrow)
        second_ent.bind("<Alt-Right>", on_alt_arrow)
        second_ent.bind("<Alt-Up>", on_alt_arrow)
        second_ent.bind("<Alt-Down>", on_alt_arrow)
        second_ents_row.append(second_ent)
    second_ents.append(second_ents_row)

button_frame = tk.Frame(root)
button_frame.grid(row=7,column=0,columnspan=4)

format_button = tk.Button(button_frame, text="Format String", command=format_string)
format_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all, fg='red')
clear_button.pack(side=tk.LEFT, padx=5)

copy_button = tk.Button(button_frame,text="Copy Output",command=copy_output)
copy_button.pack(side=tk.LEFT, padx=5)

toggle_button = tk.Button(button_frame, text="Current mode: First + Second", command=toggle_mode)
toggle_button.pack(side=tk.LEFT, padx=5)

result_text = tk.Text(root, height=12, width=None, wrap=tk.WORD)
result_text.grid(row=8, column=0, columnspan=4, sticky=tk.EW)
greeting_message = "Tips and Features\n\n" \
                   "Use ALT + Arrow Keys to quickly navigate between columns and rows.\n" \
                   "Middle Click in any row/column to quickly delete the text.\n" \
                   "Add multiple keywords/tokens to any field just like you would in a prompt.\n\n" \
                   "Switch between and First + Second or second only modes to control prompt formatting.\n\n" \
                   "First + Seconday will make a prompt that picks 1 First, and 1 Second. EXAMPLE: {first1, {thing1|thing2|thing3}}\n\n" \
                   "Second only will make a prompt that picks only 1 Second. EXAMPLE: {thing1|thing2|thing3}" \

result_text.insert(tk.END, greeting_message)

for i in range(4):
    root.columnconfigure(i, weight=1)

root.mainloop()
