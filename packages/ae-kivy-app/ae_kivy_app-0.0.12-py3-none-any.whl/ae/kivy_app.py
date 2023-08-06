"""
main application class for GUIApp-conform Kivy app
==================================================

This ae portion is providing two classes (:class:`FrameworkApp`
and :class:`KivyMainApp` and some useful constants.

The class :class:`KivyMainApp` is implementing a main app class,
based on the abstract base class :class:`~ae.gui_app.MainAppBase`
that is reducing the amount of code needed for to create a Python
application based on the :ref:`kivy <kivy.org>` framework.

The main app class :class:`KivyMainApp` is also encapsulating the
:class:`Kivy app class <kivy.app.App>` within the :class:`FrameworkApp`. The
instance of the Kivy app class can be directly accessed from the main app class
instance via the :attr:`~KivyMainApp.framework_app` attribute.


unit tests
----------

For to run the unit tests of this ae portion you need a system
with a graphic system supporting at least V 2.0 of OpenGL and the
kivy framework installed.

.. note::
    unit tests does have 100 % coverage but are currently not passing the gitlab CI
    tests because we failing in setup a proper running window system on the
    python image that all ae portions are using.

Any help for to fix the problems with the used gitlab CI image is highly appreciated.

"""
import os
from typing import Callable, Optional, Tuple, Type

# import jnius                                                                # type: ignore
import kivy                                                                 # type: ignore
from kivy.app import App                                                    # type: ignore
from kivy.core.window import Window                                         # type: ignore
from kivy.factory import Factory                                            # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import BooleanProperty, DictProperty, ListProperty     # type: ignore
from kivy.core.audio import SoundLoader                                     # type: ignore
from kivy.uix.widget import Widget                                          # type: ignore
from plyer import vibrator                                                  # type: ignore

from ae.files import FilesRegister, CachedFile                              # type: ignore
from ae.gui_app import (                                                    # type: ignore
    THEME_LIGHT_BACKGROUND_COLOR, THEME_LIGHT_FONT_COLOR, THEME_DARK_BACKGROUND_COLOR, THEME_DARK_FONT_COLOR,
    MainAppBase,
)                                                                           # type: ignore


__version__ = '0.0.12'


kivy.require('1.9.1')  # currently using 1.11.1 but at least 1.9.1 is needed for Window.softinput_mode 'below_target'
# Window.softinput_mode = 'below_target'  # ensure android keyboard is not covering Popup/text input

MAIN_KV_FILE_NAME = 'main.kv'       #: default file name of the main kv file

LOVE_VIBRATE_PATTERN = (0.0, 0.12, 0.12, 0.21, 0.03, 0.12, 0.12, 0.12)
""" short/~1.2s vibrate pattern for fun/love notification. """

ERROR_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.18, 0.18, 0.27, 0.18, 0.36, 0.27, 0.45)
""" long/~2s vibrate pattern for error notification. """

CRITICAL_VIBRATE_PATTERN = (0.00, 0.12, 0.12, 0.12, 0.12, 0.12,
                            0.12, 0.24, 0.12, 0.24, 0.12, 0.24,
                            0.12, 0.12, 0.12, 0.12, 0.12, 0.12)
""" very long/~2.4s vibrate pattern for critical error notification (sending SOS to the mobile world;). """


class FrameworkApp(App):
    """ kivy framework app class proxy redirecting events and callbacks to the main app class instance. """

    landscape = BooleanProperty()                           #: True if app win width is bigger than the app win height
    font_color = ListProperty(THEME_DARK_FONT_COLOR)        #: rgba color of the font used for labels/buttons/...
    ae_states = DictProperty()                              #: duplicate of MainAppBase app state for events/binds

    def __init__(self, main_app: 'KivyMainApp', **kwargs):
        """ init kivy app """
        self.main_app = main_app                            #: set reference to KivyMainApp instance
        self.title = main_app.app_title                     #: set kivy.app.App.title
        self.icon = os.path.join("img", "app_icon.png")     #: set kivy.app.App.icon

        super().__init__(**kwargs)

        # redirecting class name, app name and directory to the main app class for kv/ini file names is
        # .. no longer needed because main.kv get set in :meth:`KivyMainApp.init_app` and app states
        # .. get stored in the :ref:`ae config files <config-files>`.
        # self.__class__.__name__ = main_app.__class__.__name__
        # self._app_name = main_app.app_name
        # self._app_directory = '.'

    def build(self) -> Widget:
        """ kivy build app callback """
        self.main_app.po('App.build(), user_data_dir', self.user_data_dir,
                         "config files", getattr(self.main_app, '_cfg_files'))

        Window.bind(on_resize=self.win_pos_size_changed,
                    left=self.win_pos_size_changed,
                    top=self.win_pos_size_changed,
                    on_key_down=self.key_press_from_kivy,
                    on_key_up=self.key_release_from_kivy)

        return Factory.Main()

    def key_press_from_kivy(self, keyboard, key_code, _scan_code, key_text, modifiers) -> bool:
        """ convert and redistribute key down/press events coming from Window.on_key_down.

        :param keyboard:        used keyboard.
        :param key_code:        key code of pressed key.
        :param _scan_code:      key scan code of pressed key.
        :param key_text:        key text of pressed key.
        :param modifiers:       list of modifier keys (including e.g. 'capslock', 'numlock', ...)
        :return:                True if key event got processed used by the app, else False.
        """
        return self.main_app.key_press_from_framework(
            "".join(_.capitalize() for _ in sorted(modifiers) if _ in ('alt', 'ctrl', 'meta', 'shift')),
            key_text or keyboard.command_keys.get(key_code, str(key_code)),
            )

    def key_release_from_kivy(self, keyboard, key_code, _scan_code) -> bool:
        """ key release/up event. """
        return self.main_app.call_event('on_key_release', keyboard.command_keys.get(key_code, str(key_code)))

    def on_start(self):
        """ app start event """
        self.win_pos_size_changed()  # init. app./self.landscape (on app startup and after build)
        self.main_app.root_layout = self.root
        self.main_app.root_win = self.root.parent
        self.main_app.call_event('on_app_start')

    def on_pause(self) -> bool:
        """ app pause event """
        self.main_app.save_app_states()
        self.main_app.call_event('on_app_pause')
        return True

    def on_resume(self) -> bool:
        """ app resume event """
        self.main_app.load_app_states()
        self.main_app.call_event('on_app_resume')
        return True

    def on_stop(self):
        """ quit app event """
        self.main_app.save_app_states()
        self.main_app.call_event('on_app_stop')

    def win_pos_size_changed(self, *_):
        """ screen resize handler """
        win_pos_size = (Window.left, Window.top, Window.width, Window.height)
        # self.landscape = self.root.width >= self.root.height
        self.landscape = Window.width >= Window.height
        self.main_app.po('win_pos_size_changed', self.landscape, *win_pos_size)
        self.main_app.change_app_state('win_rectangle', win_pos_size)
        self.main_app.call_event('on_win_pos_size')


class KivyMainApp(MainAppBase):
    """ Kivy application """
    def init_app(self, framework_app_class: Type[FrameworkApp] = FrameworkApp) -> Tuple[Callable, Callable]:
        # pylint: disable=arguments-differ
        """ initialize framework app instance """
        win_rect = self.win_rectangle
        if win_rect:
            Window.left, Window.top = win_rect[:2]
            Window.size = win_rect[2:]

        self.framework_app = framework_app_class(self)
        if os.path.exists(MAIN_KV_FILE_NAME):
            self.framework_app.kv_file = MAIN_KV_FILE_NAME
        self._update_observable_app_states(self.retrieve_app_states())  # copy app states to duplicate DictProperty

        self.switch_theme(self.light_theme)

        return self.framework_app.run, self.framework_app.stop

    def load_sounds(self):
        """ override for to pre-load audio sounds from app folder snd into sound file cache. """
        self.sound_files = FilesRegister('snd', file_class=CachedFile,
                                         object_loader=lambda f: SoundLoader.load(f.path))

    def play_beep(self):
        """ make a short beep sound. """
        self.play_sound('error')

    def play_sound(self, sound_name: str):
        """ play audio/sound file. """
        self.dpo(f"KivyMainApp.play_sound {sound_name}")
        file: Optional[CachedFile] = self.find_sound(sound_name)
        if file:
            try:
                sound_obj = file.loaded_object
                sound_obj.pitch = file.properties.get('pitch', 1.0)
                sound_obj.volume = (
                    file.properties.get('volume', 1.0) * self.framework_app.ae_states.get('sound_volume', 1.))
                sound_obj.play()
            except Exception as ex:
                self.po(f"KivyMainApp.play_sound exception {ex}")
        else:
            self.dpo(f"KivyMainApp.play_sound({sound_name}) not found")

    def play_vibrate(self, pattern: Tuple = (0.03, 0.3)):
        """ play vibrate pattern. """
        self.dpo(f"KivyMainApp.play_vibrate {pattern}")
        try:        # added because is crashing with current plyer version (master should work)
            vibrator.pattern(pattern)
        # except jnius.jnius.JavaException as ex:
        #    self.po(f"KivyMainApp.play_vibrate JavaException {ex}, update plyer to git/master")
        except Exception as ex:
            self.po(f"KivyMainApp.play_vibrate exception {ex}")

    def switch_theme(self, light_theme: bool):
        """ switch app theme between light (True) and dark (False).

        :param light_theme:     True == light theme, False == dark theme
        """
        Window.clearcolor = THEME_LIGHT_BACKGROUND_COLOR if light_theme else THEME_DARK_BACKGROUND_COLOR
        self.framework_app.font_color = THEME_LIGHT_FONT_COLOR if light_theme else THEME_DARK_FONT_COLOR
        self.change_app_state('light_theme', light_theme)
