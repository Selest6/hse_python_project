from transformers import pipeline

# Загружаем модели

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
classifier1 = pipeline(task='text-classification', model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def emotion(sentence):
    model_outputs = classifier(sentence)
    a = ''
    results = classifier1(sentence)
    a += f"General sentiment: {results[0]['label']}\nProbability: {round(results[0]['score']*100)}%\n\nThe message contains the following emotions:\n"
    for i in model_outputs[0]:
        if i['score'] > 0.09:
            a += f"\nEmotion: {i['label']}\nProbability: {round(i['score']*100)}%\n"
    return a