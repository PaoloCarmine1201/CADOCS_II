from .model_selector import ModelSelector
from .CADOCS import ItalianModel, EnglishModel
from langdetect import detect

# This is the class that supports language detection
class PredictionService:
    def predict(self, message):
        if self._is_italian(message):
            model = ModelSelector(ItalianModel())
        else:
            model = ModelSelector(EnglishModel())

        return model.run(message)

    def _is_italian(self, message):
        try:
            lang = detect(message)
            return lang == 'it'
        except:
            return False