import sublime
import sublime_plugin


SINGLE_QUOTE_PATTERN = "'"
UCASE_FALSE_PATTERN = ":\s?False"
UCASE_TRUE_PATTERN = ":\s?True"
NONE_PATTERN = ":\s?None"
ANY_PATTERN = "<ANY>"
ENUM_PATTERN = "<.{0,100}>"

SINGLE_QUOTE_REPLACEMENT = "\""
UCASE_FALSE_REPLACEMENT = ": false"
UCASE_TRUE_REPLACEMENT = ": true"
NONE_REPLACEMENT = ": null"
ANY_REPLACEMENT = "\"<ANY>\""
ENUM_REPLACEMENT = lambda x: x.split(" ")[1].replace(">", "")


class ConvertPythonDictCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self._replace_single_quotes(edit)
        self._replace_ucase_false_occurences(edit)
        self._replace_ucase_true_occurences(edit)
        self._replace_pydantic_any_occurences(edit)
        self._replace_pydantic_enum_occurences(edit)

    def _replace_single_quotes(self, edit):
        self._simple_replace(edit, pattern=SINGLE_QUOTE_PATTERN, replacement=SINGLE_QUOTE_REPLACEMENT)

    def _replace_ucase_false_occurences(self, edit):
        self._simple_replace(edit, pattern=UCASE_FALSE_PATTERN, replacement=UCASE_FALSE_REPLACEMENT)

    def _replace_ucase_true_occurences(self, edit):
        self._simple_replace(edit, pattern=UCASE_TRUE_PATTERN, replacement=UCASE_TRUE_REPLACEMENT)

    def _replace_pydantic_any_occurences(self, edit):
        self._simple_replace(edit, pattern=NONE_PATTERN, replacement=NONE_REPLACEMENT)

    def _replace_any_occurences(self, edit):
        self._simple_replace(edit, pattern=ANY_PATTERN, replacement=ANY_REPLACEMENT)

    def _replace_pydantic_enum_occurences(self, edit):
        self._transform_replace(edit, pattern=ENUM_PATTERN, transform=ENUM_REPLACEMENT)

    def _simple_replace(self, edit, pattern, replacement):
        occurences = self.view.find_all(pattern)
        for occurence in occurences[-1::-1]:
            self._replace_with(edit, occurence, replacement)

    def _transform_replace(self, edit, pattern, transform):
        occurences = self.view.find_all(pattern)
        for occurence in occurences[-1::-1]:
            token = transform(self.view.substr(occurence))
            self._replace_with(edit, occurence, token)

    def _replace_with(self, edit, region, text):
        self.view.replace(edit, region, text)

    # Add the following method to define the menu entry
    def description(self):
        return "Convert Python Dict to JSON"


# Add the following class to define the keybinding
class ConvertPythonDictKeyBinding(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        view.run_command("convert_python_dict")
