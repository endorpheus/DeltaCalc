import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QDoubleSpinBox, QVBoxLayout,
    QGridLayout, QFrame, QPushButton, QMainWindow, QStatusBar,
    QSizePolicy
)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QTimer
from decimal import Decimal, InvalidOperation

class ClickableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_text = ""
        self.setCursor(Qt.PointingHandCursor)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setToolTip("Click to copy value")
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setWordWrap(True)  # Enable word wrapping
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.text():
            text = self.text()
            number = ''.join(c for c in text if c.isdigit() or c in '.-,%')
            number = number.rstrip('%')
            
            clipboard = QApplication.clipboard()
            clipboard.setText(number)
            
            self.original_text = self.text()
            self.setText("Copied!")
            
            QTimer.singleShot(1000, self.restore_text)
            self.setStyleSheet("color: #008000;")
            QTimer.singleShot(1000, self.reset_style)

    def restore_text(self):
        self.setText(self.original_text)
        
    def reset_style(self):
        self.setStyleSheet("")

class PercentageDifferenceCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Δ% Calculator")
        
        # Create central widget with size policies
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Input section
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        input_layout = QGridLayout(input_frame)
        input_layout.setSpacing(10)

        # Configure fonts
        font = self.font()
        font.setPointSize(10)
        
        # Labels
        self.value1_label = QLabel("First Value:")
        self.value2_label = QLabel("Second Value:")
        for label in (self.value1_label, self.value2_label):
            label.setFont(font)
            label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Spinboxes
        self.value1_spin = QDoubleSpinBox()
        self.value2_spin = QDoubleSpinBox()
        for spinbox in (self.value1_spin, self.value2_spin):
            spinbox.setRange(-1000000, 1000000)
            spinbox.setDecimals(4)
            spinbox.setValue(0)
            spinbox.setMinimumHeight(30)
            spinbox.setFont(font)
            spinbox.setAlignment(Qt.AlignRight)
            spinbox.setMinimumWidth(150)
            spinbox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Layout input section
        input_layout.addWidget(self.value1_label, 0, 0)
        input_layout.addWidget(self.value1_spin, 0, 1)
        input_layout.addWidget(self.value2_label, 1, 0)
        input_layout.addWidget(self.value2_spin, 1, 1)

        # Results section
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        result_layout = QVBoxLayout(result_frame)
        result_layout.setSpacing(10)

        # Configure result labels
        font.setBold(True)
        font.setPointSize(11)
        
        self.larger_label = ClickableLabel()
        self.smaller_label = ClickableLabel()
        self.delta_label = ClickableLabel()
        self.proportion_label = ClickableLabel()

        for label in (self.larger_label, self.smaller_label, self.delta_label, self.proportion_label):
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            result_layout.addWidget(label)

        # Clear button
        self.clear_button = QPushButton("Clear")
        font.setPointSize(10)
        self.clear_button.setFont(font)
        self.clear_button.setMinimumHeight(30)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Add widgets to main layout
        main_layout.addWidget(input_frame)
        main_layout.addWidget(result_frame)
        main_layout.addWidget(self.clear_button)

        # Connect signals
        self.value1_spin.valueChanged.connect(self.calculate_difference)
        self.value2_spin.valueChanged.connect(self.calculate_difference)
        self.clear_button.clicked.connect(self.clear_values)

        # Initial states
        self.statusBar.showMessage("Click any result to copy its value", 3000)
        self.clear_values()
        
        # Set size policies for the main window
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setMinimumWidth(400)
        
        # Adjust size to content
        self.adjustSize()

    def clear_values(self):
        self.value1_spin.setValue(0)
        self.value2_spin.setValue(0)
        self.larger_label.setText("Enter values to calculate Δ%")
        self.smaller_label.setText("")
        self.delta_label.setText("")
        self.proportion_label.setText("")
        self.statusBar.showMessage("Values cleared", 2000)
        self.adjustSize()

    def calculate_difference(self):
        try:
            val1 = Decimal(str(self.value1_spin.value()))
            val2 = Decimal(str(self.value2_spin.value()))

            if val1 == 0 and val2 == 0:
                self.larger_label.setText("Both values are zero")
                self.smaller_label.setText("")
                self.delta_label.setText("")
                self.proportion_label.setText("")
                self.adjustSize()
                return

            # Determine larger and smaller values
            if abs(val1) > abs(val2):
                larger = abs(val1)
                smaller = abs(val2)
            else:
                larger = abs(val2)
                smaller = abs(val1)

            # Calculate percentage difference
            if larger == 0:
                self.larger_label.setText("Cannot divide by zero")
                self.smaller_label.setText("")
                self.delta_label.setText("")
                self.proportion_label.setText("")
                self.adjustSize()
                return

            delta_percent = (1 - smaller/larger) * 100

            # Display results
            self.larger_label.setText(f"Larger value: {larger:,.4f}")
            self.smaller_label.setText(f"Smaller value: {smaller:,.4f}")
            self.delta_label.setText(f"Δ% = {delta_percent:.2f}%")
            self.proportion_label.setText(
                f"The smaller value is {100-delta_percent:.2f}% of the larger value"
            )
            
            # Show formula in status bar
            self.statusBar.showMessage(
                f"Δ% = (1 - {smaller:,.4f}/{larger:,.4f}) × 100", 
                5000
            )
            
            self.adjustSize()

        except (InvalidOperation, ValueError, ZeroDivisionError) as e:
            self.larger_label.setText("Invalid input")
            self.smaller_label.setText("")
            self.delta_label.setText("")
            self.proportion_label.setText("")
            self.statusBar.showMessage("Error in calculation", 2000)
            self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    calculator = PercentageDifferenceCalculator()
    calculator.show()
    sys.exit(app.exec_())
