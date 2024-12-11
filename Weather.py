import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather APP")
        vbox = QVBoxLayout()

        # Add widgets to layout
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        # Center alignments
        for widget in [self.city_label, self.city_input, self.temperature_label, self.emoji_label, self.description_label]:
            widget.setAlignment(Qt.AlignCenter)

        # Object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Apply styles
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 20px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label {
                font-size: 30px;
            }
        """)

        # Connect button click
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "6231c5e4b2f9be27e364fbd5ef9a4b5e"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error("City not found.")
        except requests.exceptions.RequestException as e:
            self.display_error(f"Error: {e}")

    def display_weather(self, data):
        # Convert temperature
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9 / 5) - 459.67

        # Update labels
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.description_label.setText(data["weather"][0]["description"].capitalize())

        # Show appropriate emoji
        weather_main = data["weather"][0]["main"].lower()
        emoji = self.get_weather_emoji(weather_main)
        self.emoji_label.setText(emoji)

    def get_weather_emoji(self, weather_main):
        """Returns an emoji based on the weather condition."""
        if "clear" in weather_main:
            return "☀️"
        elif "cloud" in weather_main:
            return "☁️"
        elif "rain" in weather_main or "drizzle" in weather_main:
            return "🌧️"
        elif "thunderstorm" in weather_main:
            return "⛈️"
        elif "snow" in weather_main:
            return "❄️"
        elif "mist" in weather_main or "fog" in weather_main:
            return "🌫️"
        else:
            return "🌍"

    def display_error(self, message):
        """Displays an error message."""
        self.temperature_label.setStyleSheet("font-size: 30px; color: red;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())