from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

# download and save model locally
model_name = 'cardiffnlp/twitter-roberta-base-emotion'
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained('./models/tokenizer/')
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.save_pretrained('./models/predictor/')