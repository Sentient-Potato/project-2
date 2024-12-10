# All my imports if it wasn't obvious
import sys
from PyQt6.QtWidgets import QApplication
from gui import GUI

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ui files here, remember to put them in the same folder
    ui_file_1 = "dnd_tracker_main_menu.ui"
    ui_file_2 = "dnd_tracker_screen_menu.ui"
    ui_file_3 = "dnd_tracker_copy_menu.ui"

    window = GUI(ui_file_1, ui_file_2, ui_file_3)

    window.show_ui()

    # Start application here
    sys.exit(app.exec())