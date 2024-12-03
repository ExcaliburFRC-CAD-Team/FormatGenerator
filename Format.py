import customtkinter as ctk
from tkinter import messagebox, StringVar
import pyperclip
from datetime import datetime

# Enum Assembly names
system_names = ["SHOT", "ARM", "BASE", "PLATE"]

def generate_id():
    year = datetime.now().year

    part_short = part_name_menu.get()

    try:
        system_type = system_type_menu.get()
        system_number = int(system_number_entry.get())
        part_order = int(part_order_entry.get()) if system_type == "Part" else 0
    except ValueError:
        messagebox.showerror("Error", "System number and part order must be valid numbers.")
        return

    part_full = part_full_entry.get()

    if system_type == "Part" and not part_full:
        messagebox.showerror("Error", "Part name (Full) cannot be empty for Part type.")
        return

    if system_type == "Main Assembly":
        base_number = 0  # Main assemblies have base number 000
        part_full = ""  # Do not include part name in the Format ID result
    elif system_type == "Sub-Assembly":
        base_number = system_number * 100  # Sub-assemblies increment by 100
    elif system_type == "Part":
        base_number = (system_number * 100) + part_order  # Add part order to sub-assembly base

    # Include part_full only for Sub-Assembly and Part types
    if part_full:
        id_generated = f"{year}-{part_short}-{base_number:03}-{system_number}-{part_full}"
    else:
        id_generated = f"{year}-{part_short}-{base_number:03}-{system_number}"

    pyperclip.copy(id_generated)
    messagebox.showinfo("CAD Format", f"Format Result: {id_generated}\n")

def update_part_order_visibility(*args):
    if system_type_var.get() == "Part":
        part_order_label.grid(row=7, column=0, pady=(10, 5), sticky="ew", columnspan=2)
        part_order_entry.grid(row=8, column=0, padx=20, sticky="ew", columnspan=2)
        part_full_label.grid(row=9, column=0, pady=(10, 5), sticky="ew", columnspan=2)
        part_full_entry.grid(row=10, column=0, padx=20, sticky="ew", columnspan=2)
    elif system_type_var.get() == "Sub-Assembly":
        part_order_label.grid_forget()
        part_order_entry.grid_forget()
        part_full_label.grid(row=9, column=0, pady=(10, 5), sticky="ew", columnspan=2)
        part_full_entry.grid(row=10, column=0, padx=20, sticky="ew", columnspan=2)
    else:
        part_order_label.grid_forget()
        part_order_entry.grid_forget()
        part_full_label.grid_forget()
        part_full_entry.grid_forget()

    if system_type_var.get() == "Main Assembly":
        part_full_label.grid_forget()
        part_full_entry.grid_forget()

app = ctk.CTk()
app.geometry("500x500")
app.title("CAD Format ID")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(list(range(10)), weight=1)

part_name_label = ctk.CTkLabel(app, text="System Name:", font=("Arial", 14))
part_name_label.grid(row=1, column=0, pady=(10, 5), sticky="ew", columnspan=2)

part_name_menu = ctk.CTkOptionMenu(app, values=system_names)
part_name_menu.set(system_names[0])
part_name_menu.grid(row=2, column=0, padx=20, sticky="ew", columnspan=2)

system_type_label = ctk.CTkLabel(app, text="Model Type:", font=("Arial", 15))
system_type_label.grid(row=3, column=0, pady=(10, 5), sticky="ew", columnspan=2)

system_type_var = StringVar(value="Main Assembly")  # def val
system_type_menu = ctk.CTkOptionMenu(app, variable=system_type_var, values=["Main Assembly", "Sub-Assembly", "Part"])
system_type_menu.grid(row=4, column=0, padx=20, sticky="ew", columnspan=2)

system_type_var.trace("w", update_part_order_visibility)

system_number_label = ctk.CTkLabel(app, text="Model Version:", font=("Arial", 14))
system_number_label.grid(row=5, column=0, pady=(10, 5), sticky="ew", columnspan=2)

system_number_entry = ctk.CTkEntry(app, placeholder_text="Enter Model number")
system_number_entry.grid(row=6, column=0, padx=20, sticky="ew", columnspan=2)

part_order_label = ctk.CTkLabel(app, text="Part Version:", font=("Arial", 14))
part_order_entry = ctk.CTkEntry(app, placeholder_text="Version - 1,2,3....")
part_order_label.grid_forget()
part_order_entry.grid_forget()

part_full_label = ctk.CTkLabel(app, text="Part Name:", font=("Arial", 14))
part_full_label.grid_forget()
part_full_entry = ctk.CTkEntry(app, placeholder_text="Example - Plate, Axis, Bearing")
part_full_entry.grid_forget()

generate_button = ctk.CTkButton(app, text="Create CAD format", command=generate_id, corner_radius=10)
generate_button.grid(row=11, column=0, pady=(20, 10), sticky="ew", columnspan=2)

for i in range(12):
    app.grid_rowconfigure(i, weight=1)
app.grid_columnconfigure(0, weight=1)

app.mainloop()

# TODO:
# Make part version + Model Version as enum
# Make enum for Part name (check the picture in whatsapp)
# Make a new enum of manufacture (3D,Sponsors, CNC, Manuel)
