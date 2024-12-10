# All my imports if it wasn't obvious
from PyQt6.QtWidgets import QStackedWidget, QMainWindow
from PyQt6.QtGui import QPalette
from PyQt6 import uic
from logic import *

"""
Coder fun fact: I started this after a burst of energy at fucking 12:00AM in the morning and worked until 3:00AM and
woke up at 9:00AM to continue working until 5:00PM. Attempting to condense this into an application so I can send to
friends that can use this.
"""

def is_valid_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

class GUI(QMainWindow):
    def __init__(self, ui_file_1, ui_file_2, ui_file_3):
        super().__init__()

        # To set the window size to prevent resizing. Please don't resize it, I worked really hard on the GUI
        self.setFixedSize(800, 650)

        # Setting up the screens
        uic.loadUi(ui_file_1, self)

        self.stacked_widgets = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widgets)

        self.screen_main = uic.loadUi(ui_file_1)
        self.screen_modes = uic.loadUi(ui_file_2)
        self.screen_copy = uic.loadUi(ui_file_3)

        # Adds the screens to stacked_widgets
        self.stacked_widgets.addWidget(self.screen_main)
        self.stacked_widgets.addWidget(self.screen_modes)
        self.stacked_widgets.addWidget(self.screen_copy)

        # Main menu screen change buttons
        self.screen_main.copy_menu_button.clicked.connect(self.change_to_copy)
        self.screen_main.screen_mode_button.clicked.connect(self.change_to_mode)

        # Return buttons
        self.screen_modes.screen_return_button.clicked.connect(self.change_to_main)
        self.screen_copy.copy_return_button.clicked.connect(self.change_to_main)

        # Screen Mode Buttons - Theme Color Buttons (*sobbing* why did I do this?)
        self.combine_theme_buttons()

        # Screen Mode Buttons = Text Color Buttons
        self.screen_modes.white_text_button.clicked.connect(lambda: self.text_color_change("white"))
        self.screen_modes.black_text_button.clicked.connect(lambda: self.text_color_change("black"))

        # Main Screen - Clear Button
        self.screen_main.clear_button.clicked.connect(self.clear_line_edits)

        # Main Screen - Sort Button
        self.screen_main.sort_button.clicked.connect(self.sort_and_display_data)

        # Sets default colors when program runs
        self.set_colors()

    def set_colors(self): # Sets the default colors of the program
        self.text_color = self.screen_main.main_menu_title.palette().color(QPalette.ColorRole.WindowText).name()
        self.background_color = self.screen_main.main_menu_title.palette().color(QPalette.ColorRole.Window).name()

    def change_to_main(self): #Swaps to the main menu screen
        self.stacked_widgets.setCurrentWidget(self.screen_main)

    def change_to_mode(self): #Swaps to the screen mode screen
        self.stacked_widgets.setCurrentWidget(self.screen_modes)

    def change_to_copy(self): # Swap to the copy log screen
        self.stacked_widgets.setCurrentWidget(self.screen_copy)

    def theme_color_change(self, theme): # Creates the themes to be used
        theme_colors = {
            "default": "rgb(204, 51, 51)",
            "artificer": "rgb(224, 141, 60)",
            "barbarian": "rgb(229, 91, 60)",
            "bard": "rgb(166, 111, 181)",
            "bloodhunter": "rgb(127, 43, 37)",
            "cleric": "rgb(145, 163, 176)",
            "druid": "rgb(114, 134, 57)",
            "fighter": "rgb(136, 83, 66)",
            "monk": "rgb(101, 158, 199)",
            "paladin": "rgb(183, 164, 88)",
            "ranger": "rgb(81, 124, 102)",
            "rogue": "rgb(85, 85, 85)",
            "sorcerer": "rgb(163, 30, 30)",
            "warlock": "rgb(115, 79, 150)",
            "wizard": "rgb(25, 89, 168)"
        }
        self.background_color = theme_colors.get(theme, self.background_color)
        self.update_styles()

    def combine_theme_buttons(self): # Adds functionality to the theme buttons
        theme_buttons = {"default": self.screen_modes.default_theme_button,
                         "artificer": self.screen_modes.artificer_theme_button,
                         "barbarian": self.screen_modes.barbarian_theme_button,
                         "bard": self.screen_modes.bard_theme_button,
                         "bloodhunter": self.screen_modes.bloodhunter_theme_button,
                         "cleric": self.screen_modes.cleric_theme_button,
                         "druid": self.screen_modes.druid_theme_button,
                         "fighter": self.screen_modes.fighter_theme_button,
                         "monk": self.screen_modes.monk_theme_button,
                         "paladin": self.screen_modes.paladin_theme_button,
                         "ranger": self.screen_modes.ranger_theme_button,
                         "rogue": self.screen_modes.rogue_theme_button,
                         "sorcerer": self.screen_modes.sorcerer_theme_button,
                         "warlock": self.screen_modes.warlock_theme_button,
                         "wizard": self.screen_modes.wizard_theme_button}
        for theme, button in theme_buttons.items():
            button.clicked.connect(lambda _, t=theme: self.theme_color_change(t))

    def text_color_change(self, color): # To change the title text color
        if color == "white":
            self.text_color = "white"
        elif color == "black":
            self.text_color = "black"
        else:
            return
        self.update_styles()

    def update_styles(self): # Applies any style changes made
        stylesheet = f"color: {self.text_color}; background-color: {self.background_color};"
        self.screen_main.main_menu_title.setStyleSheet(stylesheet)
        self.screen_modes.screen_menu_title.setStyleSheet(stylesheet)
        self.screen_copy.copy_menu_title.setStyleSheet(stylesheet)

    def clear_line_edits(self): # Clear line edits
        for i in range(1, 9):
            for prefix in ['character', 'dex', 'init']:
                getattr(self.screen_main, f'{prefix}_line_edit{i}').setText('')

    def gather_and_sort_data(self): # Retrieves the data from all line edits and sorts them with logic.py
        data = []
        character_data = [getattr(self.screen_main, f'character_line_edit{i}').text() for i in range(1, 9) if
                          getattr(self.screen_main, f'character_line_edit{i}').text().strip()]
        dex_data = [getattr(self.screen_main, f'dex_line_edit{i}').text() for i in range(1, 9) if
                    getattr(self.screen_main, f'dex_line_edit{i}').text().strip()]
        init_data = [getattr(self.screen_main, f'init_line_edit{i}').text() for i in range(1, 9) if
                     getattr(self.screen_main, f'init_line_edit{i}').text().strip()]

        for character, dex, init in zip(character_data, dex_data, init_data):
            data.append({'character': character, 'dex': dex, 'init': init})

        sorted_data = sort_data_by_init(data)

        return sorted_data

    def sort_and_display_data(self):
        errors = self.validate_inputs()
        if errors:
            self.screen_main.error_message.setText("\n".join(errors))
            return

        sorted_data = self.gather_and_sort_data()

        # Makes the text to send to the copy_log
        display_text = "\n".join([f"{entry['character']}: {entry['init']}" for entry in sorted_data])

        # Set the text to the text box on screen_copy
        self.screen_copy.copy_log_textbox.setPlainText(display_text)

        # Clear the error message if inputs are correct
        self.screen_main.error_message.setText("")

        # Switch to screen_copy
        self.change_to_copy()

    def validate_inputs(self): # To check for errors
        character_names = set()
        errors = []

        # Detects if any lines are left empty
        any_fields_filled = False

        for i in range(1, 9):
            character_name = getattr(self.screen_main, f'character_line_edit{i}').text().strip()
            dex = getattr(self.screen_main, f'dex_line_edit{i}').text().strip()
            init = getattr(self.screen_main, f'init_line_edit{i}').text().strip()

            # Detects if any lines are filled
            if character_name or dex or init:
                any_fields_filled = True

            # Detects if a line has data but is incomplete
            if (character_name and (not dex or not init)) or (dex and (not character_name or not init)) or (
                    init and (not character_name or not dex)):
                errors.append(f"Error: Entry {i} is incomplete.")
            # Detects if dex or init contains non-integers
            elif character_name and ((dex and not is_valid_integer(dex)) or (init and not is_valid_integer(init))):
                errors.append(f"Error: Entry {i} contains non-integers in the dex modifier and/or initiative score.")
            # Detects if characters are sharing names
            elif character_name in character_names:
                errors.append(f"Error: Entry {i} has a duplicate character name '{character_name}'.")
            elif character_name:
                character_names.add(character_name)

        # Detects if all lines are empty
        if not any_fields_filled:
            errors.append("Error: Nothing has been entered.")

        return errors

    def show_ui(self):
        self.show()