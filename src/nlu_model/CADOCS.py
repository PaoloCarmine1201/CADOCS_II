import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TFAutoModelForSequenceClassification
from abc import ABC, abstractmethod

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

tokenizer = RobertaTokenizer.from_pretrained(
    'roberta-base', do_lower_case=True)

model_ita = RobertaForSequenceClassification.from_pretrained(
    'alfcan/CADOCS_NLU_ita')
model_eng = RobertaForSequenceClassification.from_pretrained(
    'alfcan/CADOCS_NLU_eng')


def get_prediction(model, request):
    # Encode the request using the tokenizer
    request_ids = tokenizer.encode_plus(
        request,
        add_special_tokens=True,
        max_length=32,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt'
    )

    input_ids = torch.clone(request_ids['input_ids'])

    # Make the prediction using the model
    with torch.no_grad():
        output = model(input_ids)

    predictions = torch.softmax(output.logits, dim=1)

    # Get the top-k predicted classes and confidences
    confidence, predicted_class = torch.topk(predictions, k=4)

    confidence = confidence.detach().cpu().numpy().flatten()
    predicted_class = predicted_class.detach().cpu().numpy().flatten()

    # Map class indices to class labels
    class_mapping = {0: 'get_smells',
                     1: 'get_smells_date', 2: 'report', 3: 'info'}

    # Create a dictionary mapping class indices to class labels and confidences
    class_confidence = {class_mapping[class_idx]: conf for class_idx, conf in zip(
        predicted_class, confidence)}

    # Format of the response
    output_dict = {
        "intent": {
            "name": class_mapping[predicted_class[0]],
            "confidence": confidence[0].item()
        },
        "entities": [],
        "intent_ranking":
        [{"name": class_label, "confidence": class_confidence.item()}
            for class_label, class_confidence in class_confidence.items()]
    }

    return output_dict


# Defining the abstract class of the strategy pattern
class LanguageModel(ABC):
    @abstractmethod
    def give_prediction(self, message):
        pass


# Implementation of the strategy pattern for the Italian model
class ItalianModel(LanguageModel):
    def give_prediction(self, message):
        pred = get_prediction(model_ita, message)
        print('IT')

        return pred


# Implementation of the strategy pattern for the English model
class EnglishModel(LanguageModel):
    def give_prediction(self, message):
        pred = get_prediction(model_eng, message)
        print('EN')

        return pred
