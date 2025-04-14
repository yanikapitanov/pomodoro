from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

class PomodoroApp(App):
    def build(self):
        self.work_duration = 25 * 60  # 25 minutes
        self.break_duration = 5 * 60  # 5 minutes
        self.is_work_session = True
        self.time = self.work_duration
        self.running = False

        self.start_sound = SoundLoader.load('start.mp3')
        self.end_sound = SoundLoader.load('stop.mp3')

        self.label = Label(text=self.format_time(self.time), font_size='40sp')
        self.button = Button(text='Start', size_hint=(1, 0.3))
        self.btn = Button(text='Reset', size_hint=(1, 0.3))
        self.button.bind(on_press=self.toggle_timer)
        self.btn.bind(on_press=self.reset)

        layout = BoxLayout(orientation='vertical')
        Window.clearcolor = (1, 0, 0, 1)
        layout.add_widget(self.label)
        layout.add_widget(self.button)
        layout.add_widget(self.btn)

        return layout

    def format_time(self, t):
        minutes = t // 60
        seconds = t % 60
        return f"{minutes:02}:{seconds:02}"

    def toggle_timer(self, instance):
        if not self.running:
            self.running = True
            self.button.text = 'Pause'
            Clock.schedule_interval(self.update_timer, 1)
            if self.start_sound:
                self.start_sound.play()
        else:
            self.running = False
            self.button.text = 'Start'
            Clock.unschedule(self.update_timer)

    def reset(self, idk):
        self.time = self.work_duration
        if not self.running:
            self.button.text = 'Start'
        self.start_sound.play()
        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.time > 0:
            self.time -= 1
            self.label.text = self.format_time(self.time)
        else:
            if self.end_sound:
                self.end_sound.play()
            Clock.unschedule(self.update_timer)
            self.running = False
            self.is_work_session = not self.is_work_session
            self.time = self.work_duration if self.is_work_session else self.break_duration
            self.label.text = self.format_time(self.time)
            self.button.text = 'Start'

if __name__ == '__main__':
    PomodoroApp().run()