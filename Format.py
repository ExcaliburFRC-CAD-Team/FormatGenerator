import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import pyperclip


class FormatId:
    class PartsName:
        PLATE = "PLATE"
        WHEELS = "WHEELS"
        PROFILE = "PROFILE"
        GEAR = "GEAR"
        PULLEY = "PULLEY"
        PLA = "PLA"
        SHAFTS = "SHAFTS"
        MOTOR = "MOTOR"
        SPROCKETS = "SPROCKETS"

    class Motor:
        NEO_MOTOR = "Neo_Motor"
        NEO_VORTEX = "Neo_Vortex"
        KRAKEN_MOTOR = "Kraken_motor"
        BABY_NEO = "Baby_NEO"

    class Plate:
        ALUMINIUM = "Aluminium"
        WOOD = "Wood"
        POLYCARBONATE = "Polycarbonate"

    class ManufactureMethod:
        CNC = "CNC"
        _3D = "3D"
        LASER = "LASER"
        MANUAL = "MANUAL"
        SPONSORS = "SPONSORS"

    def __init__(self, model_type, parts_name, motor, plate, manufacture_method, width):
        self.model_type = model_type
        self.parts_name = parts_name
        self.motor = motor
        self.plate = plate
        self.manufacture_method = manufacture_method
        self.width = width

    def get_format_id(self):
        if self.model_type != "Part":
            return ""
        part = self.get_part()
        manufacture = self.get_manufacture()
        result = f"{part}-{manufacture}" if part else manufacture
        return result.rstrip('-').rstrip('--')

    def get_part(self):
        if self.parts_name == self.PartsName.PLATE and self.plate == self.Plate.ALUMINIUM:
            return f"{self.parts_name} - {self.plate} - {self.width}"
        if self.parts_name == self.PartsName.MOTOR and self.motor:
            return f"{self.parts_name} - {self.motor}"
        if self.parts_name:
            return self.parts_name
        return ""

    def get_manufacture(self):
        return self.manufacture_method if self.model_type != "Main_Assembly" else ""

    class CadId:
        def __init__(self, system_name, model_type, model_order, model_version):
            self.system_name = system_name
            self.model_type = model_type
            self.model_order = model_order
            self.model_version = model_version

        def get_id(self):
            i = "0"
            ii = "0"

            if self.model_type == "Main_Assembly":
                return i + ii
            elif self.model_type == "Sub_Assembly":
                i = self.model_order
            elif self.model_type == "Part":
                ii = self.model_order

            return i + ii

        def get_cad_id(self):
            space = "-"
            year = datetime.now().year
            return f"{year}{space}{self.system_name}{space}{self.get_id()}{self.model_version}"


class FormatGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Format Generator")
        self.geometry("400x700")
        self.system_name_var = ctk.StringVar(value="Robot")
        self.model_type_var = ctk.StringVar(value="Main_Assembly")
        self.model_order_var = ctk.StringVar(value="1")
        self.model_version_var = ctk.StringVar(value="1")
        self.parts_name_var = ctk.StringVar(value="PLA")
        self.motor_var = ctk.StringVar(value="")
        self.plate_var = ctk.StringVar(value="")
        self.width_var = ctk.IntVar(value=-1)
        self.manufacture_method_var = ctk.StringVar(value="CNC")

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="System Name:").pack(pady=5, fill="x")
        ctk.CTkComboBox(self, variable=self.system_name_var,
                        values=["Robot", "Block_bots", "Prototype", "SYSTEMS1"]).pack(
            pady=5, fill="x"
        )

        ctk.CTkLabel(self, text="Model Type:").pack(pady=5, fill="x")
        ctk.CTkComboBox(
            self, variable=self.model_type_var, values=["Main_Assembly", "Sub_Assembly ", "Part"],
            command=self.update_widgets
        ).pack(pady=5, fill="x")

        ctk.CTkLabel(self, text="Model Order:").pack(pady=5, fill="x")
        ctk.CTkComboBox(self, variable=self.model_order_var, values=[str(i) for i in range(1, 10)]).pack(pady=5,
                                                                                                         fill="x")

        ctk.CTkLabel(self, text="Model Version:").pack(pady=5, fill="x")
        ctk.CTkComboBox(self, variable=self.model_version_var, values=[str(i) for i in range(1, 10)]).pack(pady=5,
                                                                                                           fill="x")

        self.parts_name_label = ctk.CTkLabel(self, text="Parts Name:")
        self.motor_label = ctk.CTkLabel(self, text="Motor:")
        self.plate_label = ctk.CTkLabel(self, text="Plate:")
        self.width_label = ctk.CTkLabel(self, text="Width:")
        self.manufacture_method_label = ctk.CTkLabel(self, text="Manufacture Method:")

        self.parts_name_combo = ctk.CTkComboBox(
            self, variable=self.parts_name_var, values=[
                "PLATE", "WHEELS", "PROFILE", "GEAR", "PULLEY", "PLA", "SHAFTS", "MOTOR", "SPROCKETS"
            ]
        )
        self.motor_combo = ctk.CTkComboBox(
            self, variable=self.motor_var, values=["Neo_Motor", "Neo_Vortex", "Kraken_motor", "Baby_NEO"]
        )
        self.plate_combo = ctk.CTkComboBox(
            self, variable=self.plate_var, values=["Aluminium", "Wood", "Polycarbonate"]
        )
        self.width_entry = ctk.CTkEntry(self, textvariable=self.width_var)
        self.manufacture_method_combo = ctk.CTkComboBox(
            self, variable=self.manufacture_method_var, values=["CNC", "3D", "LASER", "MANUAL", "SPONSORS"]
        )

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)
        self.generate_button = ctk.CTkButton(self.bottom_frame, text="Generate Format", command=self.generate_format)
        self.generate_button.pack(fill="x", padx=10)

        self.refresh_button = ctk.CTkButton(self.bottom_frame, text="Refresh", command=self.refresh)
        self.refresh_button.pack(fill="x", padx=10, pady=5)

        self.update_widgets()

    def update_widgets(self, *args):
        model_type = self.model_type_var.get()
        parts_name = self.parts_name_var.get()
        plate = self.plate_var.get()
        # Reset widgets
        self.parts_name_label.pack_forget()
        self.parts_name_combo.pack_forget()
        self.motor_label.pack_forget()
        self.motor_combo.pack_forget()
        self.plate_label.pack_forget()
        self.plate_combo.pack_forget()
        self.width_label.pack_forget()
        self.width_entry.pack_forget()
        self.manufacture_method_label.pack_forget()
        self.manufacture_method_combo.pack_forget()
        # Only show parts_name, motor, plate, and width if model_type is "Part"
        if model_type == "Part":
            self.parts_name_label.pack(pady=5, fill="x")
            self.parts_name_combo.pack(pady=5, fill="x")
            if parts_name == FormatId.PartsName.PLATE:
                # Show plate combo box if parts_name is PLATE
                self.plate_label.pack(pady=5, fill="x")
                self.plate_combo.pack(pady=5, fill="x")

                if plate == FormatId.Plate.ALUMINIUM:
                    # Show width entry if plate is ALUMINIUM
                    self.width_label.pack(pady=5, fill="x")
                    self.width_entry.pack(pady=5, fill="x")
                else:
                    # Hide width entry if plate is not ALUMINIUM
                    self.width_label.pack_forget()
                    self.width_entry.pack_forget()
            elif parts_name == FormatId.PartsName.MOTOR:
                # Show motor combo box if parts_name is MOTOR
                self.motor_label.pack(pady=5, fill="x")
                self.motor_combo.pack(pady=5, fill="x")

            self.manufacture_method_label.pack(pady=5, fill="x")
            self.manufacture_method_combo.pack(pady=5
                                               , fill="x")

    def generate_format(self):
        format_id = FormatId(
            self.model_type_var.get().strip(),
            self.parts_name_var.get().strip(),
            self.motor_var.get().strip(),
            self.plate_var.get().strip(),
            self.manufacture_method_var.get().strip(),
            self.width_var.get()
        )
        cad_id = FormatId.CadId(
            self.system_name_var.get(),
            self.model_type_var.get(),
            self.model_order_var.get(),
            self.model_version_var.get()
        )
        final_format = cad_id.get_cad_id() + "-" + format_id.get_format_id()
        output_text = f"Format ID: {final_format.rstrip('-')}"
        messagebox.showinfo("Generated IDs", output_text)

        pyperclip.copy(output_text)

    def refresh(self):
        self.update_widgets()


if __name__ == "__main__":
    app = FormatGeneratorApp()
    app.mainloop()
