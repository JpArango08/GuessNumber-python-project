from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.logic_guessnumber import GuessNumber, WrongLengthNumberUser, InputEmpty, StringInput

Window.size = (400, 600)
Window.clearcolor = get_color_from_hex("#0f0f1a")


class DigitBox(Widget):
    """Caja visual para cada dígito adivinado."""

    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.size_hint = (None, None)
        self.size = (70, 70)
        self._value = "?"
        self._guessed = False
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self._guessed:
                Color(*get_color_from_hex("#00e5ff"))
            else:
                Color(*get_color_from_hex("#1e1e3a"))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        # Label child
        if not hasattr(self, "_lbl"):
            self._lbl = Label(
                text=self._value,
                font_size=32,
                bold=True,
                color=get_color_from_hex("#ffffff"),
                size=self.size,
                pos=self.pos,
            )
            self.add_widget(self._lbl)
        else:
            self._lbl.text = self._value
            self._lbl.pos = self.pos
            self._lbl.size = self.size

    def update(self, value, guessed):
        self._value = str(value) if value is not None else "?"
        self._guessed = guessed
        self._draw()
        if guessed:
            anim = Animation(opacity=0.3, duration=0.15) + Animation(opacity=1, duration=0.15)
            anim.start(self)


class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=30, spacing=20, **kwargs)
        self.game = GuessNumber()
        self.attempts = 0
        self._build_ui()

    def _build_ui(self):
        # Título
        title = Label(
            text="Adivina el Número",
            font_size=26,
            bold=True,
            color=get_color_from_hex("#00e5ff"),
            size_hint_y=None,
            height=50,
        )
        self.add_widget(title)

        subtitle = Label(
            text="Número secreto de 4 dígitos",
            font_size=14,
            color=get_color_from_hex("#7a7aaa"),
            size_hint_y=None,
            height=25,
        )
        self.add_widget(subtitle)

        self.add_widget(Widget(size_hint_y=None, height=10))

        # Cajas de dígitos
        boxes_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=80,
            spacing=12,
        )
        boxes_row.add_widget(Widget())  # spacer
        self.digit_boxes = []
        for i in range(4):
            box = DigitBox(index=i)
            self.digit_boxes.append(box)
            boxes_row.add_widget(box)
        boxes_row.add_widget(Widget())  # spacer
        self.add_widget(boxes_row)

        self.add_widget(Widget(size_hint_y=None, height=10))

        # Input
        input_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            spacing=10,
        )
        self.text_input = TextInput(
            hint_text="Ingresa 4 dígitos...",
            multiline=False,
            font_size=20,
            foreground_color=get_color_from_hex("#ffffff"),
            hint_text_color=get_color_from_hex("#55557a"),
            background_color=get_color_from_hex("#1e1e3a"),
            cursor_color=get_color_from_hex("#00e5ff"),
        )
        self.text_input.bind(on_text_validate=self._on_guess)
        self.text_input.bind(text=self._limit_input)
        input_row.add_widget(self.text_input)

        guess_btn = Button(
            text="↵",
            font_size=22,
            bold=True,
            size_hint_x=None,
            width=55,
            background_color=get_color_from_hex("#00e5ff"),
            color=get_color_from_hex("#0f0f1a"),
            background_normal="",
        )
        guess_btn.bind(on_release=self._on_guess)
        input_row.add_widget(guess_btn)
        self.add_widget(input_row)

        # Intentos
        self.attempts_label = Label(
            text="Intentos: 0",
            font_size=14,
            color=get_color_from_hex("#7a7aaa"),
            size_hint_y=None,
            height=30,
        )
        self.add_widget(self.attempts_label)

        # Mensaje de feedback
        self.feedback_label = Label(
            text="",
            font_size=16,
            color=get_color_from_hex("#ffffff"),
            size_hint_y=None,
            height=50,
            halign="center",
            text_size=(340, None),
        )
        self.add_widget(self.feedback_label)

        self.add_widget(Widget())  # spacer flexible

        # Botón reiniciar
        reset_btn = Button(
            text="Nueva partida",
            font_size=15,
            bold=True,
            size_hint_y=None,
            height=45,
            background_color=get_color_from_hex("#1e1e3a"),
            color=get_color_from_hex("#00e5ff"),
            background_normal="",
        )
        reset_btn.bind(on_release=self._reset)
        self.add_widget(reset_btn)

    def _limit_input(self, instance, value):
        if len(value) > 4:
            instance.text = value[:4]

    def _on_guess(self, *args):
        raw = self.text_input.text.strip()

        try:
            if raw == "":
                numbers_user = None          # -> InputEmpty
            elif not raw.isdigit():
                numbers_user = raw           # -> StringInput
            else:
                numbers_user = int(raw)      # -> WrongLengthNumberUser si != 4 digitos
            result = self.game.check_number(numbers_user)
            self.attempts += 1
            self.attempts_label.text = f"Intentos: {self.attempts}"

            if isinstance(result, str) and "HECHO" in result:
                # Ganó
                for i, box in enumerate(self.digit_boxes):
                    box.update(self.game.guessed_numbers[i], True)
                self.feedback_label.color = get_color_from_hex("#00e5ff")
                self.feedback_label.text = f"🎉 ¡Correcto en {self.attempts} intento(s)!"
            else:
                # Actualizar cajas
                for i, box in enumerate(self.digit_boxes):
                    val = result[i]
                    box.update(val, val is not None)

                guessed_count = sum(1 for v in result if v is not None)
                if guessed_count == 0:
                    self.feedback_label.color = get_color_from_hex("#ff5555")
                    self.feedback_label.text = "Ningún dígito correcto todavía."
                else:
                    self.feedback_label.color = get_color_from_hex("#ffdd57")
                    self.feedback_label.text = f"¡{guessed_count} dígito(s) en posición correcta! 🔥"

        except InputEmpty:
            self.feedback_label.color = get_color_from_hex("#ff5555")
            self.feedback_label.text = "Por favor ingresa un número."
        except StringInput as e:
            self.feedback_label.color = get_color_from_hex("#ff5555")
            self.feedback_label.text = str(e)
        except WrongLengthNumberUser:
            self.feedback_label.color = get_color_from_hex("#ff5555")
            self.feedback_label.text = "El número debe tener exactamente 4 dígitos."

        self.text_input.text = ""

    def _reset(self, *args):
        self.game = GuessNumber()
        self.attempts = 0
        self.attempts_label.text = "Intentos: 0"
        self.feedback_label.text = ""
        self.text_input.text = ""
        for box in self.digit_boxes:
            box.update(None, False)


class GuessNumberApp(App):
    def build(self):
        self.title = "Adivina el Número"
        return GameScreen()


if __name__ == "__main__":
    GuessNumberApp().run()