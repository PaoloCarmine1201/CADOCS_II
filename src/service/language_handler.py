from langdetect import detect
import re

# The structure and the __call__ method of this file was created following this site: https://refactoring.guru/design-patterns/singleton/python/example


# This class is the metaclass for LanguageHandler
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    

# This is the class that detects the language of the user's message.
# It is a Singleton because only one instance of _current_language
class LanguageHandler(metaclass=SingletonMeta):

    # This variable contains the current language used by the system to help the functions select the right message to show
    # Its default value is set to "en"
    _current_language = "en"
    
    def detect_language(self, message):
        message_replaced = self._replace_message(message)
        language = detect(message_replaced)
        if (language == "en") or (language == "it"):
            self._current_language = language
        return self.get_current_language()
    
    def get_current_language(self):
        return self._current_language
    
    # This method replaces the cadocs-specific words with "" to not bias the language detector module
    def _replace_message(self, message):
        regex_for_replacement = r"CADOCS|community|smells|smell|repository|repo"
        strings_to_replace = re.compile(regex_for_replacement, re.IGNORECASE)
        message_replaced = strings_to_replace.sub("", message)
        return message_replaced
    