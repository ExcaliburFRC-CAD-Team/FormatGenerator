import customtkinter as ctk
from datetime import datetime

# Define the FormatId class
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
        return f"{part} - {manufacture}" if part else manufacture

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

# Define the CadId class
class CadId:
    def __init__(self, type, model_type, model_order, model_version):
        self.type = type
        self.model_type = model_type
        self.model_order = model_order
        self.model_version = model_version

    def get_cad_id(self):
        year = datetime.now().year
        id_part = "0"
        if self.model_type == "Main_Assembly":
            id_part = "0"
        elif self.model_type == "Sub_Assembly":
            id_part = self.model_order
        elif self.model_type == "Part":
            id_part = self.model_order
        return f"{year} - {self.type} - {id_part} - {self.model_version}"

# Define the main application class
class FormatGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Format Generator")
        self.geometry("400x400")

        # Create input fields
        self.system_name_var = ctk.StringVar(value="SYSTEMS1")
        self.model_type_var = ctk.StringVar(value="Part")
        self.model_order_var = ctk.StringVar(value="1")
        self.model_version_var = ctk.StringVar(value="1")
        self.parts_name_var = ctk.StringVar(value="PLA")
        self.motor_var = ctk.StringVar(value="")
        self.plate_var = ctk.StringVar(value="")
        self.width_var = ctk.IntVar(value=-1)
        self.manufacture_method_var = ctk.StringVar(value="CNC")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="System Name:").pack(pady=5)
        ctk.CTkComboBox(self, variable=self.system_name_var, values=["SYSTEMS1", "SYSTEMS2", "SYSTEMS3"]). pack(pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text="Model Type:").pack(pady=5)
        ctk.CTkComboBox(self, variable=self.model_type_var, values=["Main_Assembly", "Part", "Sub_Assembly"], command=self.update_widgets).pack(pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text="Model Order:").pack(pady=5)
        ctk.CTkComboBox(self, variable=self.model_order_var, values=[str(i) for i in range(1, 10)]).pack(pady=5, fill='x', expand=True)

        ctk.CTkLabel(self, text="Model Version:").pack(pady=5)
        ctk.CTkComboBox(self, variable=self.model_version_var, values=[str(i) for i in range(1, 10)]).pack(pady=5, fill='x', expand=True)

        self.parts_name_label = ctk.CTkLabel(self, text="Parts Name:")
        self.motor_label = ctk.CTkLabel(self, text="Motor:")
        self.plate_label = ctk.CTkLabel(self, text="Plate:")
        self.width_label = ctk.CTkLabel(self, text="Width:")
        self.manufacture_method_label = ctk.CTkLabel(self, text="Manufacture Method:")

        self.parts_name_combo = ctk.CTkComboBox(self, variable=self.parts_name_var, values=[
            "PLATE", "WHEELS", "PROFILE", "GEAR", "PULLEY", "PLA", "SHAFTS", "MOTOR", "SPROCKETS"])
        self.motor_combo = ctk.CTkComboBox(self, variable=self.motor_var, values=[
            "Neo_Motor", "Neo_Vortex", "Kraken_motor", "Baby_NEO"])
        self.plate_combo = ctk.CTkComboBox(self, variable=self.plate_var, values=[
            "Aluminium", "Wood", "Polycarbonate"])
        self.width_entry = ctk.CTkEntry(self, textvariable=self.width_var)
        self.manufacture_method_combo = ctk.CTkComboBox(self, variable=self.manufacture_method_var, values=[
            "CNC", "3D", "LASER", "MANUAL", "SPONSORS"])

        self.generate_button = ctk.CTkButton(self, text="Generate Format", command=self.generate_format)
        self.result_label = ctk.CTkLabel(self, text="")

        self.update_widgets()

    def update_widgets(self, *args):
        model_type = self.model_type_var.get()
        if model_type == "Part":
            self.parts_name_label.pack(pady=5)
            self.parts_name_combo.pack(pady=5, fill='x', expand=True)
            self.motor_label.pack(pady=5)
            self.motor_combo.pack(pady=5, fill='x', expand=True)
            self.plate_label.pack(pady=5)
            self.plate_combo.pack(pady=5, fill='x', expand=True)
            self.width_label.pack(pady=5)
            self.width_entry.pack(pady=5, fill='x', expand=True)
            self.manufacture_method_label.pack(pady=5)
            self.manufacture_method_combo.pack(pady=5, fill='x', expand=True)
        else:
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

        self.generate_button.pack(pady=20, fill='x', expand=True)
        self.result_label.pack(pady=5)

    def generate_format(self):
        try:
            cad_id = CadId(
                self.system_name_var.get(),
                self.model_type_var.get(),
                self.model_order_var.get(),
                self.model_version_var.get()
            )
            format_id = FormatId(
                self.model_type_var.get(),
                self.parts_name_var.get(),
                self.motor_var.get() if self.motor_var.get() else None,
                self.plate_var.get() if self.plate_var.get() else None,
                self.manufacture_method_var.get(),
                self.width_var.get() if self.width_var.get() != -1 else None
            )
            format_result = format_id.get_format_id()
            cad_result = cad_id.get_cad_id ()
            combined_result = f"{format_result} | {cad_result}"
            self.result_label.configure(text=combined_result)
        except Exception as e:
            self.result_label.configure(text=f"Error: {str(e)}")

if __name__ == "__main__":
    app = FormatGeneratorApp()
    app.mainloop()