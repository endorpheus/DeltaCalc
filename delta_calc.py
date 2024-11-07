import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QDoubleSpinBox, QVBoxLayout,
    QGridLayout, QFrame, QPushButton, QMainWindow, QStatusBar
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
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.text():
            # Extract just the number from the text
            text = self.text()
            number = ''.join(c for c in text if c.isdigit() or c in '.-,%')
            number = number.rstrip('%')  # Remove trailing % if present
            
            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(number)
            
            # Store original text and show feedback
            self.original_text = self.text()
            self.setText("Copied!")
            
            # Restore original text after 1 second
            QTimer.singleShot(1000, self.restore_text)
            
            self.setStyleSheet("color: #008000;")  # Green text for feedback
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
        self.setMinimumWidth(350)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Input section
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_layout = QGridLayout(input_frame)
        input_layout.setSpacing(8)

        font = self.font()
        font.setPointSize(10)
        
        self.value1_label = QLabel("First Value:")
        self.value2_label = QLabel("Second Value:")
        for label in (self.value1_label, self.value2_label):
            label.setFont(font)

        self.value1_spin = QDoubleSpinBox()
        self.value2_spin = QDoubleSpinBox()
        for spinbox in (self.value1_spin, self.value2_spin):
            spinbox.setRange(-1000000, 1000000)
            spinbox.setDecimals(4)
            spinbox.setValue(0)
            spinbox.setFixedHeight(28)
            spinbox.setFont(font)
            spinbox.setAlignment(Qt.AlignRight)
            spinbox.setMinimumWidth(120)

        input_layout.addWidget(self.value1_label, 0, 0)
        input_layout.addWidget(self.value1_spin, 0, 1)
        input_layout.addWidget(self.value2_label, 1, 0)
        input_layout.addWidget(self.value2_spin, 1, 1)

        # Results section with clickable labels
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_layout = QVBoxLayout(result_frame)
        result_layout.setSpacing(6)

        font.setBold(True)
        font.setPointSize(11)
        
        self.larger_label = ClickableLabel()
        self.smaller_label = ClickableLabel()
        self.delta_label = ClickableLabel()
        self.proportion_label = ClickableLabel()

        for label in (self.larger_label, self.smaller_label, self.delta_label, self.proportion_label):
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)

        result_layout.addWidget(self.larger_label)
        result_layout.addWidget(self.smaller_label)
        result_layout.addWidget(self.delta_label)
        result_layout.addWidget(self.proportion_label)

        # Clear button
        self.clear_button = QPushButton("Clear")
        font.setPointSize(10)
        self.clear_button.setFont(font)
        self.clear_button.setFixedHeight(28)
        self.clear_button.setCursor(Qt.PointingHandCursor)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Click any result to copy its value", 3000)

        # Layout assembly
        main_layout.addWidget(input_frame)
        main_layout.addWidget(result_frame)
        main_layout.addWidget(self.clear_button)
        main_layout.addStretch()

        # Connect signals
        self.value1_spin.valueChanged.connect(self.calculate_difference)
        self.value2_spin.valueChanged.connect(self.calculate_difference)
        self.clear_button.clicked.connect(self.clear_values)

        # Initial calculation
        self.clear_values()

    def clear_values(self):
        self.value1_spin.setValue(0)
        self.value2_spin.setValue(0)
        self.larger_label.setText("Enter values to calculate Δ%")
        self.smaller_label.setText("")
        self.delta_label.setText("")
        self.proportion_label.setText("")
        self.statusBar.showMessage("Values cleared", 2000)

    def calculate_difference(self):
        try:
            val1 = Decimal(str(self.value1_spin.value()))
            val2 = Decimal(str(self.value2_spin.value()))

            if val1 == 0 and val2 == 0:
                self.larger_label.setText("Both values are zero")
                self.smaller_label.setText("")
                self.delta_label.setText("")
                self.proportion_label.setText("")
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

        except (InvalidOperation, ValueError, ZeroDivisionError) as e:
            self.larger_label.setText("Invalid input")
            self.smaller_label.setText("")
            self.delta_label.setText("")
            self.proportion_label.setText("")
            self.statusBar.showMessage("Error in calculation", 2000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    calculator = PercentageDifferenceCalculator()
    calculator.show()
    sys.exit(app.exec_())
