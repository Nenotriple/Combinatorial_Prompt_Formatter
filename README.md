# Combinatorial_Prompt_Formatter
Formats individual (or grouped) tokens for use with the popular [Dynamic Prompts extension](https://github.com/adieyal/sd-dynamic-prompts)

![Combinatorial_Prompt_Formatter](https://github.com/Nenotriple/Combinatorial_Prompt_Formatter/assets/70049990/ec60f200-fb45-4ea4-bc18-f32f3cae5c7a)

# Running this code
Simply download the latest release and double click the .pyw file to launch the script.

Or clone/download the latest commit and change the file extension from .py to .pyw *(Bugs or broken features may be present)*

# General Usage

Add your "primary tokens" to the fields on the left. Add your "secondary tokens" to the fields on the right.

ALT + Arrow keys quickly shifts between columns/rows.

Middle Click to quickly delete text in any column/row.

You can seperate additional tokens with a comma and space in any field like so: token1, token2, token3

**Primary+Secondary mode:** {primary1, {thing1|thing2|thing3}}

Picks a primary token, and a secondary token.

Primary 1, thing1

Primary 1, thing2

Primary 1, thing3

**Secondary only mode:** {thing1|thing2|thing3}

Only picks a secondary token.

thing1

thing2

thing3

__________________________________________________

Check out [the official syntax documentation](https://github.com/adieyal/sd-dynamic-prompts/blob/main/docs/SYNTAX.md) for the Dynamic Prompts extension, there's way more info and ideas for you there.

# Requirements
Python 3.10.6 or greater

tkinter (Comes preinstalled with Python)
