import numpy as np
import torch
from transformers import BertForSequenceClassification, BertTokenizer


class FrankenBert:
    """
    Implements BertForSequenceClassification and BertTokenizer
    for binary classification from a saved model
    """

    def __init__(self, saved_model: str):
        """ Loads model and tokenizer from saved_model directory,
            activates CUDA if available """
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        self.model = BertForSequenceClassification.from_pretrained(saved_model)
        self.tokenizer = BertTokenizer.from_pretrained(saved_model)
        self.model.to(self.device)

    def predict(self, text: str):
        """ Makes a classification prediction of arbitrary text """
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=280,
            return_tensors='pt',
        ).to(self.device)
        output = self.model(**inputs)
        prediction = output[0].softmax(1)
        tensors = prediction.detach().cpu().numpy()
        rank = np.argmax(tensors)
        confidence = tensors[0][rank]
        return rank, confidence
