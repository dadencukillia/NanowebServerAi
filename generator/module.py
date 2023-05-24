from enum import Enum


class WidgetType(Enum):
    TEXT_INPUT = 0
    CHECKBOX = 1
    FILE_DROP = 2


class Widget:
    def __init__(self, widget_type: WidgetType, data_name: str, label_text: str, required: bool):
        self.widget_type = widget_type
        self.data_name = data_name
        self.label_text = label_text
        self.required = required


class App:
    def __init__(self):
        self.__widgets__ = []
        self.__requirements__ = []
        self.__application_name__ = "Nanoweb"
        self.__author_name__ = "Nanoweb"
        self.__sources__ = {}
        self.__icon_path__ = "./icon.png"

    def register_widget(self, widget: Widget):
        self.__widgets__.append(widget)

    def register_widgets(self, *widgets_list: Widget):
        self.__widgets__ = self.__widgets__ + [*widgets_list]

    def register_requirements_module(self, module_name):
        self.__requirements__.append(module_name)

    def register_requirements_modules(self, *modules_list):
        self.__requirements__ = self.__requirements__ + [*modules_list]

    def set_application_name(self, name: str):
        self.__application_name__ = name

    def set_author_name(self, name: str):
        self.__author_name__ = name

    def add_source(self, name: str, url: str):
        self.__sources__[name] = url

    def set_icon(self, path: str):
        self.__icon_path__ = path


class Compiler:
    def __init__(self):
        self.__invisible_path__ = []
        self.__compile_dir__ = "./out"

    def add_invisible(self, path):
        self.__invisible_path__.append(path)

    def add_invisibles(self, *path_list):
        self.__invisible_path__ = self.__invisible_path__ + [*path_list]

    def set_compile_dir(self, path):
        self.__compile_dir__ = path


Application = App()
CompilerConfig = Compiler()