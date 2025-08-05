import FreeCAD, FreeCADGui, PySide
from PySide import QtWidgets  # Ensure you're importing the necessary modules

class RepetitionTool(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RepetitionTool, self).__init__(parent)
        self.setWindowTitle("Répétition linéaire")
        self.setGeometry(50, 50, 350, 450)


        # Create layout and widgets
        layout = QtWidgets.QVBoxLayout(self)

        # Create execute button
        self.execute_button = QtWidgets.QPushButton("Executer", self)
        self.execute_button.clicked.connect(self.execute_repetitions)
        layout.addWidget(self.execute_button)

        # Create other necessary widgets (e.g., spinboxes, checkboxes)
        self.spinbox = QtWidgets.QSpinBox(self)
        self.label = QtWidgets.QLabel("exemplaires (max. 1 Milliard):", self)
        layout.addWidget(self.label)               
        self.name_checkbox = QtWidgets.QCheckBox("grouper dans un dossier", self)
        layout.addWidget(self.spinbox)
        layout.addWidget(self.name_checkbox)

        self.label = QtWidgets.QLabel("espacement X(mm):", self)
        layout.addWidget(self.label)
        self.spinbox1 = QtWidgets.QDoubleSpinBox(self)
        self.spinbox1.setRange(-float('inf'), float('inf'))
        layout.addWidget(self.spinbox1)

        self.label = QtWidgets.QLabel("espacement Y(mm):", self)
        layout.addWidget(self.label)        
        self.spinbox2 = QtWidgets.QDoubleSpinBox(self)
        self.spinbox2.setRange(-float('inf'), float('inf'))
        layout.addWidget(self.spinbox2)

        self.label = QtWidgets.QLabel("espacement Z(mm):", self)
        layout.addWidget(self.label)
        self.spinbox3 = QtWidgets.QDoubleSpinBox(self)
        self.spinbox3.setRange(-float('inf'), float('inf'))
        layout.addWidget(self.spinbox3)

        self.label = QtWidgets.QLabel("espacement rotatif X(°):", self)
        layout.addWidget(self.label)
        self.spinbox6 = QtWidgets.QDoubleSpinBox(self)
        self.spinbox6.setRange(-float('inf'), float('inf'))
        layout.addWidget(self.spinbox6)

        self.label = QtWidgets.QLabel("espacement rotatif Y(°):", self)
        layout.addWidget(self.label)
        self.spinbox5 = QtWidgets.QDoubleSpinBox(self)
        self.spinbox5.setRange(-float('inf'), float('inf'))
        layout.addWidget(self.spinbox5)

        self.label = QtWidgets.QLabel("espacement rotatif Z(°):", self)
        layout.addWidget(self.label)
        self.spinbox4 = QtWidgets.QDoubleSpinBox(self)
        self.spinbox4.setRange(-float('inf'), float('inf'))
        layout.addWidget(self.spinbox4)

        # Set layout
        self.setLayout(layout)

    def execute_repetitions(self):
        """Executes the repetition logic based on user input."""
        try:
            # Gather values from the spinbox
            repetition_value = self.spinbox.value()
            name_individually = self.name_checkbox.isChecked()

            # Get spacing and rotation values
            spacing_1 = self.spinbox1.value()
            spacing_2 = self.spinbox2.value()
            spacing_3 = self.spinbox3.value()
            rotation_angle_1 = self.spinbox4.value()
            rotation_angle_2 = self.spinbox5.value()
            rotation_angle_3 = self.spinbox6.value()

            # Placeholder for the actual repetition logic
            FreeCAD.Console.PrintMessage(f"Repetition: {repetition_value}, Name Individually: {name_individually}\n")

            # Get the selection from the GUI
            sel = FreeCAD.Gui.Selection.getSelection()

            # Check if the selection is empty
            if not sel:
                FreeCAD.Console.PrintError("❌ Please select a Part object.\n")
                return

            base = sel[0]

            # Ensure that the selected object has a shape
            if not hasattr(base, 'Shape'):
                FreeCAD.Console.PrintError("❌ The selected object does not have a Shape.\n")
                return

            # Create a folder for individually named objects if the checkbox is checked
            if name_individually:
                folder = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", "GeneratedCopies")
                FreeCAD.ActiveDocument.recompute()

            # Create copies with spacing
            for i in range(repetition_value):
                new_shape = base.Shape.copy()  # Copy the shape of the base object
                new_obj = FreeCAD.ActiveDocument.addObject("Part::Feature", f"Copy_{i + 1}" if name_individually else "Copy")  # Conditional naming
                new_obj.Shape = new_shape
                
                # Set the placement based on the spacing and rotation
                new_obj.Placement = FreeCAD.Placement(
                    FreeCAD.Vector(i * spacing_1, i * spacing_2, i * spacing_3),  # Only using spacing_1 for demonstration
                    FreeCAD.Rotation(rotation_angle_1 * i, rotation_angle_2 * i, rotation_angle_3 * i)  # Incremental rotation
                )

                # If naming individually, add the object to the folder
                if name_individually:
                    folder.addObject(new_obj)

            # Recompute the document to apply changes
            FreeCAD.ActiveDocument.recompute()
            FreeCAD.Console.PrintMessage("✅ Repetition complete.\n")
            self.accept()  # Close the dialog after execution

        except Exception as e:
            FreeCAD.Console.PrintError(f"Error executing repetitions: {str(e)}\n")

def show_repetition_tool():
    """Shows the repetition tool dialog."""
    dialog = RepetitionTool(FreeCADGui.getMainWindow())
    dialog.exec_()

# Ensure the GUI runs in FreeCAD environment
if __name__ == "__main__":
    show_repetition_tool()
