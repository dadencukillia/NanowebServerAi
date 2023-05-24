import generator


generator.Application.set_application_name("NanoWebTemplate")
generator.Application.set_author_name("NanoWeb")
generator.Application.set_icon("./icon.png")

generator.Application.add_source("YouTube", "https://youtube.com")
generator.Application.add_source("TikTok", "https://tiktok.com")

generator.Application.register_widgets(
    generator.Widget(generator.WidgetType.TEXT_INPUT, "textinput_example", "Введіть текст", True),
    generator.Widget(generator.WidgetType.CHECKBOX, "checkbox_example", "Забирайте або ставте галочку", False),
    generator.Widget(generator.WidgetType.FILE_DROP, "file_example", "Завантажте файл", True)
)

generator.Application.register_requirements_modules(
    "numpy",
    "colorama",
    "pillow"
) # Потрібні для роботи бібліотеки

generator.CompilerConfig.add_invisibles(
    "./venv", "./config.py", "./generator", "./generate.py", "./out"
)

generator.CompilerConfig.set_compile_dir("./out")