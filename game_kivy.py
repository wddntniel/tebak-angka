import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
import random

class GameLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=30, spacing=15, **kwargs)
        self.angka_rahasia = random.randint(1, 100)
        self.kesempatan = 7
        self.selesai = False
        self.rekor = None

        with self.canvas.before:
            Color(0.12, 0.12, 0.18, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.judul = Label(
            text="TEBAK ANGKA",
            font_size=32, bold=True,
            color=(0.8, 0.65, 0.97, 1),
            size_hint_y=None, height=60
        )
        self.add_widget(self.judul)

        self.sub = Label(
            text="Tebak angka antara 1 dan 100",
            font_size=14, color=(0.42, 0.44, 0.52, 1),
            size_hint_y=None, height=30
        )
        self.add_widget(self.sub)

        self.hati = Label(
            text="♥ " * 7,
            font_size=22, color=(0.95, 0.55, 0.66, 1),
            size_hint_y=None, height=40
        )
        self.add_widget(self.hati)

        self.rekor_label = Label(
            text="Rekor: -",
            font_size=13, color=(0.42, 0.44, 0.52, 1),
            size_hint_y=None, height=25
        )
        self.add_widget(self.rekor_label)

        self.entry = TextInput(
            hint_text="Masukkan angka...",
            font_size=28, multiline=False,
            size_hint_y=None, height=60,
            halign='center', input_filter='int',
            background_color=(0.19, 0.20, 0.27, 1),
            foreground_color=(0.8, 0.84, 0.96, 1),
            cursor_color=(0.8, 0.84, 0.96, 1),
        )
        self.entry.bind(on_text_validate=self.tebak)
        self.add_widget(self.entry)

        self.tebak_btn = Button(
            text="Tebak",
            font_size=16, bold=True,
            size_hint_y=None, height=50,
            background_color=(0.8, 0.65, 0.97, 1),
            color=(0.12, 0.12, 0.18, 1)
        )
        self.tebak_btn.bind(on_press=self.tebak)
        self.add_widget(self.tebak_btn)

        self.hint = Label(
            text="Masukkan tebakan kamu!",
            font_size=14, color=(0.8, 0.84, 0.96, 1),
            size_hint_y=None, height=40,
            halign='center', text_size=(300, None)
        )
        self.add_widget(self.hint)

        self.riwayat = Label(
            text="", font_size=13,
            color=(0.54, 0.71, 0.98, 1),
            size_hint_y=None, height=30
        )
        self.add_widget(self.riwayat)

        self.reset_btn = Button(
            text="Main lagi",
            font_size=13,
            size_hint_y=None, height=40,
            background_color=(0.19, 0.20, 0.27, 1),
            color=(0.42, 0.44, 0.52, 1)
        )
        self.reset_btn.bind(on_press=self.reset)
        self.add_widget(self.reset_btn)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def tebak(self, *args):
        if self.selesai:
            return
        try:
            nilai = int(self.entry.text)
        except ValueError:
            self.hint.text = "Masukkan angka yang valid!"
            self.hint.color = (0.95, 0.55, 0.66, 1)
            return
        if nilai < 1 or nilai > 100:
            self.hint.text = "Angka harus antara 1 - 100!"
            self.hint.color = (0.95, 0.55, 0.66, 1)
            return

        self.kesempatan -= 1
        hati_str = "♥ " * self.kesempatan + "♡ " * (7 - self.kesempatan)
        self.hati.text = hati_str.strip()

        riwayat_lama = self.riwayat.text
        self.riwayat.text = (riwayat_lama + "  " + str(nilai)).strip()
        self.entry.text = ""

        if nilai < self.angka_rahasia:
            self.hint.text = f"{nilai} terlalu kecil — coba lebih tinggi!"
            self.hint.color = (0.54, 0.71, 0.98, 1)
        elif nilai > self.angka_rahasia:
            self.hint.text = f"{nilai} terlalu besar — coba lebih rendah!"
            self.hint.color = (0.98, 0.70, 0.53, 1)
        else:
            jumlah = 7 - self.kesempatan
            self.hint.text = f"Benar! Angkanya {self.angka_rahasia}! ({jumlah} tebakan)"
            self.hint.color = (0.65, 0.89, 0.63, 1)
            if self.rekor is None or jumlah < self.rekor:
                self.rekor = jumlah
                self.rekor_label.text = f"Rekor: {self.rekor}"
            self.selesai = True
            return

        if self.kesempatan == 0:
            self.hint.text = f"Game over! Angkanya adalah {self.angka_rahasia}"
            self.hint.color = (0.95, 0.55, 0.66, 1)
            self.selesai = True

    def reset(self, *args):
        self.angka_rahasia = random.randint(1, 100)
        self.kesempatan = 7
        self.selesai = False
        self.hati.text = "♥ " * 7
        self.hint.text = "Masukkan tebakan kamu!"
        self.hint.color = (0.8, 0.84, 0.96, 1)
        self.riwayat.text = ""
        self.entry.text = ""

class TebakAngkaApp(App):
    def build(self):
        return GameLayout()

if __name__ == "__main__":
    TebakAngkaApp().run()