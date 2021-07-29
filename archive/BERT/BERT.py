import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification


class BERT:
    def set_device(self):
        """
        Sets device as 'GPU' or 'CPU'
        """
        # if there's a GPU available...
        if torch.cuda.is_available():
            # tell PyTorch to use the GPU.
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')

        return device

    def load_model(self, path):
        """
        Loads model and tokenizer from binary file

        path: str
        """
        # load a trained model and vocabulary that you have fine-tuned
        model = BertForSequenceClassification.from_pretrained(path)
        tokenizer = BertTokenizer.from_pretrained(path)

        return model, tokenizer

    def predict(self, text, model_path):
        """
        Uses fine tuned BERTforSequenceClassification to make a 
        prediction
        
        text: str
        model_path: str
        """
        device = self.set_device()

        model, tokenizer = self.load_model(model_path)

        model.to(device)

        # prepare our text into tokenized sequence
        inputs = tokenizer(text, padding=True, truncation=True,
                           max_length=64, return_tensors='pt').to(device)
        
        # perform inference on our model
        outputs = model(**inputs)
        
        # get output probabilities through softmax
        probs = outputs[0].softmax(1)
        
        # executing argmax function to get label
        return np.argmax(probs.detach().cpu().numpy())
