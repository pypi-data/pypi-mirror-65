"""
base class for python applications with a graphical user interface
==================================================================

The abstract base class :class:`MainAppBase` provided by this ae namespace
portion can be used for to integrate any of the available Python GUI
frameworks into the ae namespace.

The plan is to integrate the following GUI frameworks until the begin of 2021:

* :mod:`Kivy <ae.kivy_app>` - see also :ref:`kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`
* :mod:`Enaml <ae.enaml_app>` - see also :ref:`enaml lisz demo app <https://gitlab.com/ae-group/enaml_lisz>`
* :mod:`Beeware <ae.beeware_app>`
* :mod:`pyglet <ae.pyglet_app>`
* :mod:`pygobject <ae.pygobject_app>`
* :mod:`Dabo <ae.dabo_app>`
* :mod:`QPython <ae.qpython_app>`
* :mod:`AppJar <ae.appjar_app>`

Currently available is the :mod:`Kivy <ae.kivy_app>` integration of
the :ref:`Kivy Framework <kivy.org>`.

.. note:
    In implementing the outstanding framework integrations this module will be
    extended and changed frequently.


extended console application environment
----------------------------------------

The abstract base class :class:`MainAppBase` inherits directly from the ae namespace
class :class:`ae console application environment class <ae.console.ConsoleApp>`.
The so inherited helper methods are useful for to configure and
control the run-time of your GUI app via command line arguments,
:ref:`config-options` and :ref:`config-files`.

.. hint::
    Please see the documentation of the :mod:`ae.console` namespace
    portion/module for more detailed information.

:class:`MainAppBase` adds on top of the :class:`~ae.console.ConsoleApp`
the concepts of :ref:`application status` and :ref:`application context`,
explained further down.


integrate new gui framework
---------------------------

For to integrate a new Python GUI framework you have to declare a
new class that inherits from :class:`MainAppBase` and implements at
least the abstract method :meth:`~MainAppBase.init_app`.

Most GUI frameworks are providing an application class that need to
be initialized. For to keep a reference to the framework app class
instance within your main app class you can use the
:attr:`~MainAppBase.framework_app` attribute of :class:`MainAppBase`.

If you want ot use the :attr:`~MainAppBase.root_win` and/or
:attr:`~MainAppBase.root_layout` attributes you can initialize them
also within :meth:`~MainAppBase.init_app`.

.. hint::
    The initialization of the attributes :attr:`~MainAppBase.framework_app`
    :attr:`~MainAppBase.root_win` and :attr:`~MainAppBase.root_layout` is optional.
    You could e.g. also add the framework application as mixin
    to the main app class.

A typical implementation of a framework-specific main app class
looks like::

    from new_gui_framework import NewFrameworkApp

    class NewFrameworkMainApp(MainAppBase):
        def init_app(self):
            self.framework_app = NewFrameworkApp()
            self.root_win = MainView()
            self.root_layout = self.root_win.main_layout

            return self.framework_app.start, self.framework_app.stop

:meth:`~MainAppBase.init_app` will be executed only once
at app startup for to initialize the GUI framework and
prepare it for the app startup.

For to finally startup the app the :meth:`~MainAppClass.run_app` method
has to be called from the main module of your app project.
:meth:`~MainAppBase.run_app` will then start the GUI event loop by
calling the first method that got returned by :meth:`~MainAppBase.init_app`.


key press event dispatching
___________________________

For to provide a on_key_press event to the applications that will use the new
GUI framework you have to catch the key press events of the framework,
convert/normalize them and then call the :meth:`~MainAppBase.key_press_from_framework`
with the normalized modifiers and key args.

The :paramref:`~MainAppBase.key_press_from_framework.modifiers` arg is a string
that can contain several of the following sub-strings, always in the alphabetic
order (like listed below):

* Alt
* Ctrl
* Meta
* Shift

The :paramref:`~MainAppBase.key_press_from_framework.key` arg is a string
that is specifying the last pressed key. If the key is not representing
not a single character but a command key, then `key` will be one of the
following strings:

* escape
* tab
* backspace
* enter
* del
* enter
* up
* down
* right
* left
* home
* end
* pgup
* pgdown


application status
------------------

Any application- and user-specific configurations like e.g. the last
window position/size, the app theme/font or the last selected context
within your app, could be included in the application status.

This namespace portion introduces the section `aeAppState` in the app
:ref:`config-files`, where any status values can be stored persistently
for to be recovered on the next startup of your application.

.. hint::
    The section name is declared by the :data:`APP_STATE_SECTION_NAME`
    constant. If you need to access this config section directly then
    please use this constant instead of the hardcoded section name.

.. _app-state-variables:

This module is providing/pre-defining the following application state variables:

    * :attr:`~MainAppBase.context_id`
    * :attr:`~MainAppBase.context_path`
    * :attr:`~MainAppBase.font_size`
    * :attr:`~MainAppBase.light_theme`
    * :attr:`~MainAppBase.sound_volume`
    * :attr:`~MainAppBase.win_rectangle`

Which app state variables are finally used by your app project is (fully data-driven)
depending on the app state :ref:`config-variables` detected in all the
:ref:`config-files` that are found/available at run-time of your app.
The names of the available application state variables can be
determined with the main app helper method :meth:`~MainAppBase.app_state_keys`.

If your application is e.g. supporting a user-defined font size, using the
provided/pre-defined app state variable :attr:`~MainAppBase.font_size`, then it has to call
the method :meth:`change_app_state` with the :paramref:`~MainAppBase.change_app_state.state_name`
set to `font_size` every time when the user has changed the font size of your app.

.. hint::
    The two built-in app state variables are :attr:`~MainAppBase.context_id` and
    :attr:`~MainAppBase.context_path` will be explained detailed in the next section.

The :meth:`~MainBaseApp.load_app_states` method is called on instantiation from
the implemented main app class for to load the values of all
app state variables from the :ref:`config-files`, and is then calling
:meth:~MainAppBase.setup_app_states` for pass them into their corresponding
instance attributes.

Use the main app instance attribute for to read/get the actual value of
a single app state variable. The actual values of
all app state variables as a dict is determining the method
:meth:`~MainBaseApp.retrieve_app_states` for you.

Changed app state value that need to be propagated also to the framework
app instance should never be set via the instance attribute, instead call
the method :meth:`~MainBaseApp.change_app_state` (which ensures (1) the
propagation to any duplicated (observable/bound) framework property and
(2) the event notification to related the main app instance method).

For to to save the app state to the :ref:`config-files` the implementing main app
instance has to call the method :meth:`~MainBaseApp.save_app_states` - this could be
done e.g. after the app state has changed or at least on quiting the application.

.. _app-state-constants:

This module is also providing some pre-defined constants that can be optionally
used in your application in relation to the app states data store and
for the app state config variables :attr:`~MainAppBase.font_size`
and :attr:`~MainAppBase.light_theme`:

    * :data:`APP_STATE_SECTION_NAME`
    * :data:`APP_STATE_VERSION_VAR_NAME`
    * :data:`APP_STATE_CURRENT_VERSION`
    * :data:`MIN_FONT_SIZE`
    * :data:`MAX_FONT_SIZE`
    * :data:`THEME_LIGHT_BACKGROUND_COLOR`
    * :data:`THEME_LIGHT_FONT_COLOR`
    * :data:`THEME_DARK_BACKGROUND_COLOR`
    * :data:`THEME_DARK_FONT_COLOR`


application context
-------------------

:class:`MainBaseApp` provides your application a integrated context manager,
which persists application contexts in the :ref:`config-files` as an app state.

A application context is represented by a string that defines e.g.
the action for to enter into the context, the data that gets currently displayed
and an index within the data.

The format of this context string/id can be freely defined by your application.
The app state variable :attr:`~MainAppBase.context_id` stores the current
context (or selection) when the app quits for to restore it
on the next app start.

The context id is initially an empty string. As soon as the user is
changing the current selection your application should call the
:meth:`~MainBaseApp.change_app_state` passing the string `context_id`
into the :paramref:`~MainAppBase.change_app_state.state_name` argument
for to change the app context.

For more complex applications you can specify a path of nested contexts.
This context path gets represented by the app state variable
:attr:`~MainAppBase.context_path`, which is a list of context strings/ids.
For to enter into a deeper/nested context you simply call the
:meth:`~MainBaseApp.context_enter` method instead of calling the
:meth:`~MainBaseApp.change_app_state` method for the `context_id`
and `context_path` app states.


application state events
------------------------

The helper method :meth:`~MainAppBase.call_event` can be used to support
optionally implemented event callback routines.

This method is used internally by this module for to fire notification events when one of
the app state variables gets changed - like e.g. the :ref:`application context` or if
the user changes the font size.

The method name of the notification event consists of the prefix ``on_`` followed
by the variable name of the app state. So on a change of the `font_size` the
notification event ``on_font_size`` will be called (if exists as a method
of the main app instance).
"""
from abc import ABC, abstractmethod
from configparser import NoSectionError
from typing import Any, Callable, Dict, Tuple, List, Optional

from ae.updater import check_all                    # type: ignore
from ae.console import ConsoleApp                   # type: ignore

from ae.files import FilesRegister, RegisteredFile  # type: ignore


__version__ = '0.0.14'


AppStateType = Dict[str, Any]                   #: app state config variable type

APP_STATE_SECTION_NAME = 'aeAppState'           #: config section name for to store app state

#: config variable name for to store the current application state version
APP_STATE_VERSION_VAR_NAME = 'app_state_version'
APP_STATE_CURRENT_VERSION = 2                   #: current application state version

MIN_FONT_SIZE = 15.0                            #: minimum font size in pixels
MAX_FONT_SIZE = 99.0                            #: maximum font size in pixels

COLOR_BLACK = (0.009, 0.006, 0.003, 1.0)        # for to differentiate from framework pure black/white colors
COLOR_WHITE = (0.999, 0.996, 0.993, 1.0)
THEME_DARK_BACKGROUND_COLOR = COLOR_BLACK       #: dark theme background color in rgba(0.0 ... 1.0)
THEME_DARK_FONT_COLOR = COLOR_WHITE             #: dark theme font color in rgba(0.0 ... 1.0)
THEME_LIGHT_BACKGROUND_COLOR = COLOR_WHITE      #: light theme background color in rgba(0.0 ... 1.0)
THEME_LIGHT_FONT_COLOR = COLOR_BLACK            #: light theme font color in rgba(0.0 ... 1.0)


check_all()     # let ae_updater module check/install any outstanding updates or new app versions


class MainAppBase(ConsoleApp, ABC):
    """ abstract base class for to implement a GUIApp-conform app class """
    # app states
    context_id: str = ""                                    #: id of the current app context (entered by the app user)
    context_path: List[str]                                 #: list of context ids, reflecting recent user actions
    font_size: float = 30.0                                 #: font size used for toolbar and context screens
    light_theme: bool = False                               #: True=light theme/background, False=dark theme
    sound_volume: float = 0.12                              #: sound volume of current app (0.0=mute, 1.0=max)
    win_rectangle: tuple = (0, 0, 800, 600)                 #: window coordinates (x, y, width, height)

    # generic run-time shortcut references provided by the main app
    framework_app: Any = None                               #: app class instance of the used GUI framework
    root_win: Any = None                                    #: app window
    root_layout: Any = None                                 #: app root layout

    image_files: Optional[FilesRegister] = None             #: image/icon files
    sound_files: Optional[FilesRegister] = None             #: sound/audio files

    def __init__(self, **console_app_kwargs):
        """ create instance of app class.

        :param console_app_kwargs:  kwargs to be passed to the __init__ method of :class:`~ae.console_app.ConsoleApp`.
        """
        self._exit_code: int = 0            #: init by stop_app() and passed onto OS by run_app()
        self._start_event_loop: Callable    #: callable to start event loop of GUI framework
        self._stop_event_loop: Callable     #: callable to start event loop of GUI framework

        self.context_path = list()  # init for Literal type recognition - will be overwritten by setup_app_states()
        super().__init__(**console_app_kwargs)
        self.load_app_states()
        self.load_images()
        self.load_sounds()

        self._start_event_loop, self._stop_event_loop = self.init_app()
        assert callable(self._start_event_loop) and callable(self._stop_event_loop), \
            f"MainAppBase.__init__: start/stop event handler methods have to be callable"

    # abstract methods

    @abstractmethod
    def init_app(self) -> Tuple[Callable, Callable]:
        """ initialize framework app instance and root window/layout, return GUI event loop start/stop methods.

        :return:        tuple of two callable, the 1st for to start and the 2nd for to stop/exit the GUI event loop.
        """

    # base implementation helper methods (can be overwritten by framework portion or by user main app)

    def app_state_keys(self) -> Tuple:
        """ determine current config variable names/keys of the app state section :data:`APP_STATE_SECTION_NAME`.

        :return:                tuple of all app state item keys (config variable names).
        """
        try:  # quicker than asking before with: if cfg_parser.has_section(APP_STATE_SECTION_NAME):
            return tuple(self._cfg_parser.options(APP_STATE_SECTION_NAME))
        except NoSectionError:
            self.dpo(f"MainAppBase.app_state_keys: ignoring missing config file section {APP_STATE_SECTION_NAME}")
            return tuple()

    def call_event(self, method: str, *args, **kwargs) -> Any:
        """ dispatch event to inheriting instances.

        :param method:      name of the main app method to call.
        :param args:        args passed to the main app method to be called.
        :param kwargs:      kwargs passed to the main app method to be called.
        :return:            return value of the called method or None if method does not exist.
        """
        event_callback = getattr(self, method, None)
        if event_callback:
            assert callable(event_callback), f"MainAppBase.call_event: {method!r} is not callable ({args}, {kwargs})"
            return event_callback(*args, **kwargs)
        return None

    def change_app_state(self, state_name: str, new_value: Any, send_event: bool = True):
        """ change single app state item to value in self.attribute and app_state dict item.

        :param state_name:  name of the app state to change.
        :param new_value:   new value of the app state to change.
        :param send_event:  pass False to prevent to send/call the on_<state_name> event to the main app instance.
        """
        setattr(self, state_name, new_value)
        self._change_observable(state_name, new_value)
        if send_event:
            self.call_event('on_' + state_name)

    def _change_observable(self, name: str, value: Any):
        """ change observable attribute/member/property in framework_app instance.

        :param name:    name of the observable attribute/member or key of an observable dict property.
        :param value:   new value of the observable.
        """
        if self.framework_app:
            if hasattr(self.framework_app, 'ae_states'):            # has observable DictProperty duplicates
                # noinspection PyUnresolvedReferences
                self.framework_app.ae_states[name] = value
            if hasattr(self.framework_app, 'ae_state_' + name):     # has observable attribute duplicate
                setattr(self.framework_app, 'ae_state_' + name, value)

    def context_enter(self, context_id: str, next_context_id: str = ''):
        """ user extending/entering/adding new context_id (e.g. navigates down in the app context path/tree).

        :param context_id:      context id/name to enter into.
        :param next_context_id: context id within the entering/new child context.
        """
        self.context_path.append(context_id)
        self.change_app_state('context_path', self.context_path)
        self.change_app_state('context_id', next_context_id)

    def context_leave(self, next_context_id: str = ''):
        """ user navigates up in the data tree.

        :param next_context_id: context id to set in the parent context.
        """
        list_name = self.context_path.pop()
        self.change_app_state('context_path', self.context_path)
        self.change_app_state('context_id', next_context_id or list_name)

    def find_image(self, image_name: str, height: float = 32.0, light_theme: bool = True) -> Optional[RegisteredFile]:
        """ find best fitting image in img app folder.

        :param image_name:      name of the image (file name without extension).
        :param height:          preferred height of the image/icon.
        :param light_theme:     preferred theme (dark/light) of the image.
        :return:                image file object (RegisteredFile/CachedFile) if found else None.
        """
        def property_matcher(file):
            """ find images with matching theme. """
            return bool(file.properties.get('dark', 0)) != light_theme

        def file_sorter(file):
            """ sort images files by height delta. """
            return abs(file.properties.get('height', 0.0) - height)

        if self.image_files:
            return self.image_files(image_name, property_matcher=property_matcher, file_sorter=file_sorter)
        return None

    def find_sound(self, sound_name: str) -> Optional[RegisteredFile]:
        """ find sound by name.

        :param sound_name:      name of the sound to search for.
        :return:                cached sound file object (RegisteredFile/CachedFile) if sound name was found else None.
        """
        if self.sound_files:    # prevent error on app startup (setup_app_states() called before load_images()
            return self.sound_files(sound_name)
        return None

    def key_press_from_framework(self, modifiers: str, key: str) -> bool:
        """ dispatch key press event, coming normalized from the UI framework. """
        event_name = f'on_key_press_of_{modifiers}_{key}'
        en_lower = event_name.lower()
        if not self.call_event(event_name):
            if event_name == en_lower or not self.call_event(en_lower):
                return self.call_event('on_key_press', modifiers, key)
        return True

    def load_app_states(self):
        """ load application state for to prepare app.run_app """
        app_state = dict()
        for key in self.app_state_keys():
            app_state[key] = self.get_var(key, section=APP_STATE_SECTION_NAME)

        self.setup_app_states(app_state)

    def load_images(self):
        """ load images from app folder img. """
        self.image_files = FilesRegister('img')

    def load_sounds(self):
        """ load audio sounds from app folder snd. """
        self.sound_files = FilesRegister('snd')

    def play_beep(self):
        """ make a short beep sound, should be overwritten by GUI framework. """
        self.po(chr(7), "BEEP")

    def play_sound(self, sound_name: str):
        """ play audio/sound file, should be overwritten by GUI framework.

        :param sound_name:  name of the sound to play.
        """
        self.po(f"play_sound {sound_name}")

    def play_vibrate(self, pattern: Tuple = (0.0, 0.3)):
        """ play vibrate pattern, should be overwritten by GUI framework.

        :param pattern:     tuple of pause and vibrate time sequence.
        """
        self.po(f"play_vibrate {pattern}")

    def retrieve_app_states(self) -> AppStateType:
        """ determine the state of a running app from the config files and return it as dict.

        :return:    dict with all app states available in the config files.
        """
        app_state = dict()
        for key in self.app_state_keys():
            app_state[key] = getattr(self, key)

        return app_state

    def run_app(self):
        """ startup main and framework applications. """
        self.dpo(f"MainAppBase.run_app")

        if not self._parsed_args:
            self._parse_args()

        try:
            self._start_event_loop()
        finally:
            self.shutdown(self._exit_code or None)  # don't call sys.exit() for zero exit code

    def save_app_states(self) -> str:
        """ save app state in config file.

        :return:    empty string if app status could be saved into config files else error message.
        """
        err_msg = ""

        app_state = self.retrieve_app_states()
        for key, state in app_state.items():
            err_msg = self.set_var(key, state, section=APP_STATE_SECTION_NAME)
            self.dpo(f"save_app_state {key}={state} {err_msg or 'OK'}")
            if err_msg:
                break
        self.load_cfg_files()
        return err_msg

    def setup_app_states(self, app_state: AppStateType):
        """ put app state variables into main app instance for to prepare framework app.run_app.

        :param app_state:   dict of app states.
        """
        for key, val in app_state.items():
            self.change_app_state(key, val, send_event=False)

        config_file_version = app_state.get(APP_STATE_VERSION_VAR_NAME, 0)
        for version in range(config_file_version, APP_STATE_CURRENT_VERSION):
            key, val = '', None
            if version == 0:
                key, val = 'light_theme', False
            elif version == 1:
                key, val = 'sound_volume', 1.0
            if key:
                self.change_app_state(key, val, send_event=False)
                self.set_var(key, val, section=APP_STATE_SECTION_NAME)
        if config_file_version < APP_STATE_CURRENT_VERSION:
            key, val = APP_STATE_VERSION_VAR_NAME, APP_STATE_CURRENT_VERSION
            self.change_app_state(key, val, send_event=False)
            self.set_var(key, val, section=APP_STATE_SECTION_NAME)

    def stop_app(self, exit_code: int = 0):
        """ quit this application.

        :param exit_code:   optional exit code.
        """
        self.dpo(f"MainAppBase.stop_app {exit_code}")
        self._exit_code = exit_code

        if self.root_win:
            # neither self.framework_app.stop() nor self.framework_app._qapp.exit(exit_code) trigger window closed event
            self.root_win.close()   # close window to save app state data

        self._stop_event_loop()     # will exit the self._start_event_loop() method called by self.run_app()

    def _update_observable_app_states(self, app_state: AppStateType):
        """ update all the observable app states.

        :param app_state:   dict of app states.
        """
        if self.framework_app:
            for key, val in app_state.items():
                self._change_observable(key, val)
