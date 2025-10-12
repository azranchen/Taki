from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.metrics import dp, sp
from kivy.core.window import Window
from datetime import datetime
import os
import tempfile


class PlayerFrame(BoxLayout):
    def __init__(self, index, player_name, on_buy_callback, on_log_callback, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(3), size_hint_y=None, padding=dp(5), **kwargs)
        self.height = dp(60)

        self.total_buy = 0
        self.player_name = player_name
        self.on_buy_callback = on_buy_callback
        self.on_log_callback = on_log_callback

        # Display indexed and capitalized player name
        formatted_name = f"{index}. {player_name.capitalize()}"

        # Row 1: Name, Buy input, Buy button, Total, Debt, Chips
        row1 = BoxLayout(orientation='horizontal', spacing=dp(2), size_hint_y=None, height=dp(30))
        self.label_name = Label(text=formatted_name, font_size=sp(12), bold=True, size_hint_x=0.15, halign='left')
        self.label_name.bind(size=self.label_name.setter('text_size'))
        row1.add_widget(self.label_name)
        
        self.input_buy = TextInput(hint_text="0", input_filter="int", multiline=False, size_hint_x=0.12, font_size=sp(12))
        self.input_buy.bind(focus=self.on_focus_buy)
        row1.add_widget(self.input_buy)
        
        self.button_buy = Button(text="Buy", size_hint_x=0.12, font_size=sp(10))
        self.button_buy.bind(on_press=self.calculate_buy)
        row1.add_widget(self.button_buy)
        
        row1.add_widget(Label(text="T:", size_hint_x=0.08, font_size=sp(10)))
        self.label_total_buy = Label(text="0", size_hint_x=0.10, font_size=sp(12), bold=True)
        row1.add_widget(self.label_total_buy)
        
        row1.add_widget(Label(text="D:", size_hint_x=0.08, font_size=sp(10)))
        self.input_debt = TextInput(hint_text="0", input_filter="int", multiline=False, size_hint_x=0.12, font_size=sp(12))
        self.input_debt.bind(focus=self.on_focus_debt)
        row1.add_widget(self.input_debt)
        
        row1.add_widget(Label(text="C:", size_hint_x=0.08, font_size=sp(10)))
        self.input_chips = TextInput(hint_text="0", input_filter="int", multiline=False, size_hint_x=0.12, font_size=sp(12))
        self.input_chips.bind(focus=self.on_focus_chips)
        row1.add_widget(self.input_chips)
        self.add_widget(row1)

        # Row 2: Sum only
        row2 = BoxLayout(orientation='horizontal', spacing=dp(2), size_hint_y=None, height=dp(25))
        row2.add_widget(Label(text="Sum:", size_hint_x=0.2, font_size=sp(12), halign='left'))
        self.label_sum = Label(text="0", size_hint_x=0.8, font_size=sp(14), bold=True, halign='left')
        self.label_sum.bind(size=self.label_sum.setter('text_size'))
        row2.add_widget(self.label_sum)
        self.add_widget(row2)

    def on_focus_buy(self, instance, value):
        """Clear text when focused for easy input"""
        if value and instance.text == "":  # When focused and empty
            pass  # Do nothing, let user type
        elif value:  # When focused with text
            instance.select_all()
    
    def on_focus_debt(self, instance, value):
        """Select all text when focused for easy replacement"""
        if value:  # When focused
            instance.select_all()
    
    def on_focus_chips(self, instance, value):
        """Select all text when focused for easy replacement"""
        if value:  # When focused
            instance.select_all()

    def calculate_buy(self, instance):
        try:
            buy_value = int(self.input_buy.text) if self.input_buy.text else 0
        except ValueError:
            buy_value = 0
        
        if buy_value > 0:
            self.total_buy += buy_value
            self.label_total_buy.text = str(self.total_buy)
            # Log before resetting input
            if self.on_log_callback:
                self.on_log_callback(f"{self.player_name.capitalize()} bought in for {buy_value} (Total: {self.total_buy})")
            self.input_buy.text = ""  # Clear instead of setting to "0"
            if self.on_buy_callback:
                self.on_buy_callback()

    def calculate_sum(self, log_changes=False):
        try:
            chips = int(self.input_chips.text) if self.input_chips.text else 0
        except ValueError:
            chips = 0
        try:
            debt = int(self.input_debt.text) if self.input_debt.text else 0
        except ValueError:
            debt = 0
        total = chips - debt
        self.label_sum.text = str(total)
        
        if log_changes and self.on_log_callback:
            if chips > 0 or debt > 0:
                self.on_log_callback(f"{self.player_name.capitalize()} - Chips: {chips}, Debt: {debt}, Sum: {total}")
        
        return chips  # Return chips for total calculation

    def get_total_buy(self):
        return self.total_buy


class MainApp(App):
    def build(self):
        # Set window size to simulate mobile screen (comment out for desktop use)
        #Window.size = (360, 640)  # Typical mobile screen in portrait
        
        self.players = []
        self.log_file_path = os.path.join(tempfile.gettempdir(), 'taki_game_log.txt')
        self.init_log_file()

        self.total_buy_label = Label(text="0", font_size=sp(18), bold=True)
        self.total_chips_label = Label(text="0", font_size=sp(18), bold=True)

        # Create tabbed panel
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_height=dp(50))
        
        # Game tab
        game_tab = TabbedPanelItem(text='Game')
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Date layout aligned to left
        date_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_label = Label(text="Date:", size_hint_x=0.2, font_size=sp(16), halign='left', valign='middle')
        self.date_display = Label(text=current_date, size_hint_x=0.8, font_size=sp(16), halign='left', valign='middle')
        for widget in [date_label, self.date_display]:
            widget.bind(size=widget.setter('text_size'))
        date_layout.add_widget(date_label)
        date_layout.add_widget(self.date_display)
        main_layout.add_widget(date_layout)

        # Players input row
        player_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        self.player_name_input = TextInput(hint_text="Player name", multiline=False, font_size=sp(14), size_hint_x=0.5)
        self.add_player_button = Button(text="Add", font_size=sp(14), size_hint_x=0.3)
        self.add_player_button.bind(on_press=self.add_player)
        player_input_layout.add_widget(self.player_name_input)
        player_input_layout.add_widget(self.add_player_button)
        main_layout.add_widget(player_input_layout)

        # Scrollable area for players
        self.scroll = ScrollView(size_hint=(1, 1))
        self.players_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None, padding=dp(3))
        self.players_layout.bind(minimum_height=self.players_layout.setter('height'))
        self.scroll.add_widget(self.players_layout)
        main_layout.add_widget(self.scroll)

        # Total Buy-Ins and Chips Summary
        summary_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=dp(5), padding=dp(10))
        
        buy_summary = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        buy_summary.add_widget(Label(text="Total Buy-Ins:", font_size=sp(16), halign='left'))
        buy_summary.add_widget(self.total_buy_label)
        summary_layout.add_widget(buy_summary)
        
        chips_summary = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        chips_summary.add_widget(Label(text="Total Chips:", font_size=sp(16), halign='left'))
        chips_summary.add_widget(self.total_chips_label)
        summary_layout.add_widget(chips_summary)
        
        main_layout.add_widget(summary_layout)

        # Calculate button
        self.calculate_button = Button(text="Calculate", size_hint_y=None, height=dp(60), font_size=sp(18))
        self.calculate_button.bind(on_press=self.calculate_all)
        main_layout.add_widget(self.calculate_button)
        
        game_tab.add_widget(main_layout)
        tabbed_panel.add_widget(game_tab)
        
        # Log tab
        self.log_tab = TabbedPanelItem(text='Log')
        log_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Show log file path
        log_path_label = Label(text=f"Log: {self.log_file_path}", size_hint_y=None, height=dp(40), font_size=sp(12))
        log_layout.add_widget(log_path_label)
        
        # Refresh button for log
        refresh_button = Button(text="Refresh Log", size_hint_y=None, height=dp(60), font_size=sp(16))
        refresh_button.bind(on_press=self.refresh_log)
        log_layout.add_widget(refresh_button)
        
        # Log display area - using TextInput for better display
        self.log_display = TextInput(
            text="Game log will appear here...",
            readonly=True,
            multiline=True,
            size_hint=(1, 1),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            font_size=sp(14)
        )
        log_layout.add_widget(self.log_display)
        
        self.log_tab.add_widget(log_layout)
        tabbed_panel.add_widget(self.log_tab)
        
        # Bind tab switch event to refresh log
        self.log_tab.bind(on_press=self.on_log_tab_press)
        tabbed_panel.bind(current_tab=self.on_tab_switch)
        
        return tabbed_panel

    def init_log_file(self):
        """Initialize the log file with a header"""
        try:
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"=== Taki Game Log ===\n")
                f.write(f"Game started: {current_time}\n")
                f.write(f"{'='*50}\n\n")
                f.flush()
        except Exception as e:
            print(f"Error initializing log file: {e}")
    
    def log_event(self, message):
        """Log an event to the file with timestamp"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                f.flush()  # Ensure it's written immediately
        except Exception as e:
            print(f"Error logging event: {e}")
    
    def refresh_log(self, instance=None):
        """Refresh the log display from the file"""
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                f.seek(0)  # Go to start of file
                log_content = f.read()
                if log_content:
                    self.log_display.text = log_content
                    # Scroll to bottom to show latest entries
                    self.log_display.cursor = (0, len(self.log_display.text))
                else:
                    self.log_display.text = "No log entries yet."
        except FileNotFoundError:
            self.log_display.text = f"Log file not found at: {self.log_file_path}"
        except Exception as e:
            self.log_display.text = f"Error reading log: {e}"
    
    def on_log_tab_press(self, instance):
        """Called when log tab is pressed"""
        self.refresh_log()
    
    def on_tab_switch(self, instance, value):
        """Called when switching tabs"""
        if hasattr(value, 'text') and value.text == 'Log':
            self.refresh_log()
    
    def add_player(self, instance):
        name = self.player_name_input.text.strip()
        if name:
            index = len(self.players) + 1
            frame = PlayerFrame(index, name, on_buy_callback=self.update_total_buy, on_log_callback=self.log_event)
            self.players_layout.add_widget(frame)
            self.players.append(frame)
            self.player_name_input.text = ""
            self.log_event(f"Player added: {name.capitalize()}")
            self.update_total_buy()

    def update_total_buy(self):
        total = sum(player.get_total_buy() for player in self.players)
        self.total_buy_label.text = str(total)

    def calculate_all(self, instance):
        self.log_event("--- Calculate All ---")
        total_chips = sum(player.calculate_sum(log_changes=True) for player in self.players)
        self.total_chips_label.text = str(total_chips)
        self.log_event(f"Total Chips: {total_chips}")
        self.log_event(f"Total Buy-Ins: {self.total_buy_label.text}")


if __name__ == '__main__':
    MainApp().run()
