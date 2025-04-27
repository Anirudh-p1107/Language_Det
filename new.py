import tkinter as tk
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import os

# Suppress TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load model, tokenizer, label map
model = load_model("best_language_model.keras", compile=False)
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("label_map.pkl", "rb") as f:
    label_map = pickle.load(f)
reverse_label_map = {v: k for k, v in label_map.items()}

# Full language names
full_names = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "or": "Odia",
    "ur": "Urdu",
    "ar": "Arabic",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali"
}

# Prediction function
def predict_language():
    sentence = entry.get().strip()
    if not sentence:
        result_label.config(text="Please enter a sentence", fg="red")
        return

    seq = tokenizer.texts_to_sequences([sentence])
    padded = pad_sequences(seq, maxlen=100, padding="post", truncating="post")
    pred = model.predict(padded, verbose=0)
    pred_class = np.argmax(pred, axis=1)[0]
    lang_code = reverse_label_map[pred_class]
    lang_name = full_names.get(lang_code, lang_code)
    result_label.config(text=f"Predicted Language: {lang_name}", fg="#1a75ff")

# GUI Setup
root = tk.Tk()
root.title("Language Identifier")
root.geometry("600x400")
root.configure(bg="#f2f2f2")  # Light gray background
root.resizable(False, False)


# Heading
tk.Label(root, text="Language Identifier", font=("Helvetica", 24, "bold"), bg="#f2f2f2", fg="#003366").pack(pady=30)

# Entry
entry = tk.Entry(root, font=("Arial", 16), width=40, bd=3, relief="groove")
entry.pack(pady=10)

# Button
tk.Button(root, text="Predict Language", command=predict_language,
          font=("Verdana", 14), bg="#0066cc", fg="white", padx=10, pady=5).pack(pady=15)

# Result
result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f2f2f2")
result_label.pack(pady=10)

root.mainloop()
