from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
import qrcode
import os


class MainScreen(Screen):
    """Main Screen of the App."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set window size (optional)
        Window.size = (500, 700)

        # Main Layout
        layout = BoxLayout(orientation="vertical", spacing=20, padding=20)

        # Title Label
        title = MDLabel(
            text="QR Code Generator",
            halign="center",
            font_style="H4",
            size_hint=(1, 0.2),
        )
        layout.add_widget(title)

        # Text Input Field for User Data
        self.text_input = MDTextField(
            hint_text="Enter text to generate QR Code",
            size_hint=(1, 0.1),
            font_size=18,
            helper_text="QR Code cannot exceed data limits",
            helper_text_mode="on_focus",
        )
        layout.add_widget(self.text_input)

        # Generate Button
        generate_button = MDRaisedButton(
            text="Generate QR Code",
            pos_hint={"center_x": 0.5},
            size_hint=(0.6, 0.1),
            md_bg_color=(0, 0.5, 1, 1),  # Blue color
            font_size=16,
        )
        generate_button.bind(on_press=self.generate_qr)
        layout.add_widget(generate_button)

        # Exit Button
        exit_button = MDFlatButton(
            text="Exit",
            pos_hint={"center_x": 0.5},
            size_hint=(0.6, 0.1),
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),  # Red color for the text
            font_size=16,
        )
        exit_button.bind(on_press=self.exit_app)
        layout.add_widget(exit_button)

        # QR Code Display Area
        self.qr_image = Image(size_hint=(1, 0.6))
        layout.add_widget(self.qr_image)

        # Create a Status Label for Feedback
        self.status_label = MDLabel(
            text="",
            halign="center",
            font_size=14,
            theme_text_color="Hint",
            size_hint=(1, 0.1),
        )
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def generate_qr(self, instance):
        """Generate the QR Code based on Text Input."""
        user_input = self.text_input.text.strip()

        # Validate Input
        if not user_input:
            self.status_label.text = "Please enter some text to generate a QR Code!"
            return

        try:
            # Create a QR Code
            qr = qrcode.QRCode(
                version=None,  # Automatically pick the smallest version
                error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction
                box_size=10,
                border=4,  # Border size of 4 'boxes'
            )
            qr.add_data(user_input)
            qr.make(fit=True)

            # Save the generated QR code image temporarily
            qr_image_path = "modern_qr.png"
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save(qr_image_path)

            # Update the Image widget in the UI
            self.qr_image.source = qr_image_path
            self.qr_image.reload()

            self.status_label.text = "QR Code Generated Successfully!"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def exit_app(self, instance):
        """Exit the App."""
        MDDialog(
            title="Exit",
            text="Are you sure you want to exit?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dismiss_dialog()
                ),
                MDRaisedButton(
                    text="EXIT",
                    md_bg_color=(1, 0, 0, 1),  # Red exit button
                    on_release=lambda x: App.get_running_app().stop()
                ),
            ],
        ).open()

    def dismiss_dialog(self):
        """Close the dialog box."""
        # If you want to add other functionality like closing popups, this could be defined here
        pass


class QRCodeApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        return sm


# Run the app
if __name__ == "__main__":
    QRCodeApp().run()