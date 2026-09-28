# -*- coding: utf-8 -*-
"""
KHMEAS STREAM PLAYER v2.0
تطبيق بث مباشر احترافي
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    WebView = None

BG_COLOR = (0.02, 0.02, 0.02, 1)
GREEN = (0, 1, 0.25, 1)
CYAN = (0, 1, 1, 1)
RED = (1, 0, 0.2, 1)
YELLOW = (1, 0.8, 0, 1)
PURPLE = (0.7, 0.15, 1, 1)
WHITE = (1, 1, 1, 1)

PASSWORD = "008800"

PLATFORMS = {
    "YouTube": [
        ("Al Jazeera English", "https://www.youtube.com/watch?v=gCNeDWCI0vo"),
        ("France 24 English", "https://www.youtube.com/watch?v=h3MuIUNCCzI"),
        ("DW News", "https://www.youtube.com/watch?v=GE_SfNVNyqk"),
        ("Sky News", "https://www.youtube.com/watch?v=9Auq9mYxFEE"),
        ("NASA Live", "https://www.youtube.com/watch?v=21X5lGlDOfg"),
        ("Lofi Girl", "https://www.youtube.com/watch?v=jfKfPfyJRdk"),
    ],
    "Twitch": [
        ("Twitch Gaming", "https://www.twitch.tv/directory/game/Just%20Chatting"),
        ("Twitch Music", "https://www.twitch.tv/directory/game/Music"),
    ],
    "Telegram": [
        ("قناة مخصصة", "https://t.me/"),
    ],
    "منصات أخرى": [
        ("Facebook Live", "https://www.facebook.com/live"),
        ("Instagram Live", "https://www.instagram.com/"),
        ("TikTok Live", "https://www.tiktok.com/live"),
        ("Twitter / X Live", "https://twitter.com/"),
    ],
}

class ColoredBox(BoxLayout):
    def __init__(self, bg_color=(0, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class LoginScreen(ColoredBox):
    def __init__(self, app, **kwargs):
        super().__init__(bg_color=BG_COLOR, orientation='vertical', padding=40, spacing=20, **kwargs)
        self.app = app
        title = Label(
            text="[b][color=00ff41]KHMEAS[/color][/b]\n[size=40][b]STREAM PLAYER[/b][/size]\n\n[size=18][color=ff0033]SYSTEM LOCKED[/color][/size]",
            markup=True, font_size=60, halign='center', valign='middle', size_hint_y=0.5)
        self.add_widget(title)
        self.password_input = TextInput(hint_text="أدخل كلمة المرور", password=True, multiline=False,
            font_size=20, halign='center', background_color=(0, 0, 0, 1),
            foreground_color=GREEN, cursor_color=GREEN, size_hint_y=None, height=60)
        self.add_widget(self.password_input)
        btn = Button(text="[b]دخول[/b]", markup=True, font_size=24,
            background_color=(0, 1, 0.25, 1), background_normal='', size_hint_y=None, height=70)
        btn.bind(on_press=self.check_password)
        self.add_widget(btn)
        self.error_label = Label(text="", color=RED, font_size=18, size_hint_y=None, height=40)
        self.add_widget(self.error_label)
    def check_password(self, instance):
        if self.password_input.text == PASSWORD:
            self.app.show_main_menu()
        else:
            self.error_label.text = "كلمة المرور خاطئة!"
            self.password_input.text = ""

class MainMenu(ColoredBox):
    def __init__(self, app, **kwargs):
        super().__init__(bg_color=BG_COLOR, orientation='vertical', padding=20, spacing=15, **kwargs)
        self.app = app
        header = Label(
            text="[b][color=00ff41]KHMEAS[/color] [color=00ffff]STREAM[/color] [color=b026ff]PLAYER[/color][/b]\n[size=16][color=ff0033]v2.0 // LIVE STREAMS[/color][/size]",
            markup=True, font_size=38, halign='center', size_hint_y=None, height=120)
        self.add_widget(header)
        platforms = [
            ("YouTube", (1, 0, 0.2, 1), "YouTube"),
            ("Twitch", (0.7, 0.15, 1, 1), "Twitch"),
            ("Telegram", (0, 0.5, 1, 1), "Telegram"),
            ("منصات أخرى", (1, 0.8, 0, 1), "منصات أخرى"),
        ]
        for text, color, key in platforms:
            btn = Button(text=f"[b]{text}[/b]", markup=True, font_size=24,
                background_color=color, background_normal='', size_hint_y=None, height=80)
            btn.bind(on_press=lambda x, k=key: self.app.show_platform(k))
            self.add_widget(btn)
        exit_btn = Button(text="[b]خروج[/b]", markup=True, font_size=22,
            background_color=(1, 0, 0.2, 1), background_normal='', size_hint_y=None, height=70)
        exit_btn.bind(on_press=lambda x: self.app.stop())
        self.add_widget(exit_btn)

class PlatformScreen(ColoredBox):
    def __init__(self, app, platform_name, **kwargs):
        super().__init__(bg_color=BG_COLOR, orientation='vertical', padding=20, spacing=10, **kwargs)
        self.app = app
        title = Label(text=f"[b][color=00ff41]{platform_name}[/color][/b]",
            markup=True, font_size=32, size_hint_y=None, height=70)
        self.add_widget(title)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=10)
        content.bind(minimum_height=content.setter('height'))
        streams = PLATFORMS.get(platform_name, [])
        for name, url in streams:
            btn = Button(text=f"[b]{name}[/b]", markup=True, font_size=20,
                background_color=(0, 0.5, 0.3, 1), background_normal='', size_hint_y=None, height=70)
            btn.bind(on_press=lambda x, u=url, n=name: self.app.play_stream(n, u))
            content.add_widget(btn)
        custom_btn = Button(text="[b]رابط مخصص[/b]", markup=True, font_size=20,
            background_color=(0, 0.7, 0.7, 1), background_normal='', size_hint_y=None, height=70)
        custom_btn.bind(on_press=self.show_custom_url)
        content.add_widget(custom_btn)
        scroll.add_widget(content)
        self.add_widget(scroll)
        back_btn = Button(text="[b]رجوع[/b]", markup=True, font_size=22,
            background_color=(0.5, 0, 0.5, 1), background_normal='', size_hint_y=None, height=70)
        back_btn.bind(on_press=lambda x: self.app.show_main_menu())
        self.add_widget(back_btn)
    def show_custom_url(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        url_input = TextInput(hint_text="الصق الرابط هنا", multiline=False,
            font_size=18, background_color=(0, 0, 0, 1), foreground_color=GREEN)
        content.add_widget(url_input)
        buttons = BoxLayout(spacing=10, size_hint_y=None, height=60)
        play_btn = Button(text="[b]تشغيل[/b]", markup=True, background_color=GREEN, background_normal='')
        cancel_btn = Button(text="[b]إلغاء[/b]", markup=True, background_color=RED, background_normal='')
        buttons.add_widget(play_btn)
        buttons.add_widget(cancel_btn)
        content.add_widget(buttons)
        popup = Popup(title="رابط مخصص", content=content, size_hint=(0.9, 0.4))
        play_btn.bind(on_press=lambda x: (popup.dismiss(), self.app.play_stream("رابط مخصص", url_input.text)))
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

class PlayerScreen(ColoredBox):
    def __init__(self, app, stream_name, url, **kwargs):
        super().__init__(bg_color=BG_COLOR, orientation='vertical', padding=10, spacing=10, **kwargs)
        self.app = app
        self.url = url
        title = Label(text=f"[b][color=00ff41]{stream_name}[/color][/b]",
            markup=True, font_size=22, size_hint_y=None, height=50)
        self.add_widget(title)
        info = Label(text="[color=00ffff]جاري فتح البث...[/color]", markup=True, font_size=18)
        self.add_widget(info)
        back_btn = Button(text="[b]رجوع للقائمة[/b]", markup=True, font_size=22,
            background_color=PURPLE, background_normal='', size_hint_y=None, height=70)
        back_btn.bind(on_press=lambda x: self.app.show_main_menu())
        self.add_widget(back_btn)
        Clock.schedule_once(lambda dt: self.open_webview(), 0.5)
    def open_webview(self):
        if platform == 'android' and WebView:
            try:
                @run_on_ui_thread
                def show_webview():
                    webview = WebView(Activity)
                    webview.getSettings().setJavaScriptEnabled(True)
                    webview.getSettings().setDomStorageEnabled(True)
                    webview.setWebViewClient(WebViewClient())
                    webview.loadUrl(self.url)
                    Activity.setContentView(webview)
                show_webview()
            except Exception as e:
                print(f"WebView Error: {e}")

class KhmeasApp(App):
    def build(self):
        self.title = "KHMEAS STREAM PLAYER"
        Window.clearcolor = BG_COLOR
        self.root_box = ColoredBox(bg_color=BG_COLOR)
        Clock.schedule_once(lambda dt: self.show_login(), 0.1)
        return self.root_box
    def set_screen(self, widget):
        self.root_box.clear_widgets()
        self.root_box.add_widget(widget)
    def show_login(self):
        self.set_screen(LoginScreen(self))
    def show_main_menu(self):
        self.set_screen(MainMenu(self))
    def show_platform(self, platform_name):
        self.set_screen(PlatformScreen(self, platform_name))
    def play_stream(self, name, url):
        if not url:
            popup = Popup(title="تنبيه", content=Label(text="الرابط فارغ!", color=RED, font_size=20), size_hint=(0.8, 0.3))
            popup.open()
            return
        self.set_screen(PlayerScreen(self, name, url))

if __name__ == "__main__":
    KhmeasApp().run()
