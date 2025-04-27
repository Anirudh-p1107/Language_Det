import random
import os
from indicnlp.tokenize import indic_tokenize
from indicnlp.normalize import indic_normalize

# Define character sets for each language's script (no hardcoded words)
# Edit this section to add or modify languages
char_sets = {
    "en": {  # Latin script for English
        "consonants": ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "y"],
        "vowels": ["a", "e", "i", "o", "u"]
    },
    "kn": {  # Kannada script
        "consonants": ["ಕ", "ಖ", "ಗ", "ಘ", "ಚ", "ಛ", "ಜ", "ಝ", "ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "ಧ", "ನ", "ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ", "ರ", "ಲ", "ವ", "ಶ", "ಷ", "ಸ", "ಹ"],
        "vowels": ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ", "ಂ", "ಃ"],
        "independent_vowels": ["ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ"]
    },
    "ml": {  # Malayalam script
        "consonants": ["ക", "ഖ", "ഗ", "ഘ", "ച", "ഛ", "ജ", "ഝ", "ട", "ഠ", "ഡ", "ഢ", "ണ", "ത", "ഥ", "ദ", "ധ", "ന", "പ", "ഫ", "ബ", "ഭ", "മ", "യ", "ര", "ല", "വ", "ശ", "ഷ", "സ", "ഹ"],
        "vowels": ["ാ", "ി", "ീ", "ു", "ൂ", "െ", "േ", "ൈ", "ൊ", "ോ", "ൌ", "ം", "ഃ"],
        "independent_vowels": ["അ", "ആ", "ഇ", "ഈ", "ഉ", "ഊ", "എ", "ഏ", "ഐ", "ഒ", "ഓ", "ഔ"]
    },
    "or": {  # Odia script
        "consonants": ["କ", "ଖ", "ଗ", "ଘ", "ଚ", "ଛ", "ଜ", "ଝ", "ଟ", "ଠ", "ଡ", "ଢ", "ଣ", "ତ", "ଥ", "ଦ", "ଧ", "ନ", "ପ", "ଫ", "ବ", "ଭ", "ମ", "ଯ", "ର", "ଲ", "ଵ", "ଶ", "ଷ", "ସ", "ହ"],
        "vowels": ["ା", "ି", "ୀ", "ୁ", "ୂ", "େ", "ୈ", "ୋ", "ୌ", "ଂ", "ଃ"],
        "independent_vowels": ["ଅ", "ଆ", "ଇ", "ଈ", "ଉ", "ଊ", "ଏ", "ଐ", "ଓ", "ଔ"]
    },
    "ur": {  # Perso-Arabic script for Urdu
        "consonants": ["ب", "پ", "ت", "ٹ", "ث", "ج", "چ", "ح", "خ", "د", "ڈ", "ذ", "ر", "ڑ", "ز", "ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "گ", "ل", "م", "ن", "و", "ہ", "ی"],
        "vowels": ["َ", "ِ", "ُ", "ْ", "ّ", "ٰ", "ً", "ٍ", "ٌ"],
        "independent_vowels": ["ا", "آ", "ی", "و"]
    }
}

# Sentence templates (language-specific, filled with pseudo-words)
template_adjustments = {
    "en": {
        "templates": [
            "{noun} is {adjective}.",
            "{noun} likes to {verb}.",
            "I {verb} in {place}.",
            "{adjective} {noun} is in {place}.",
            "{noun} and {noun} {verb}."
        ]
    },
    "kn": {
        "templates": [
            "{noun} {adjective} ಆಗಿದೆ।",
            "{noun} {verb} ಮಾಡಲು ಇಷ್ಟಪಡುತ್ತದೆ।",
            "ನಾನು {place} ನಲ್ಲಿ {verb} ಮಾಡುತ್ತೇನೆ।",
            "{adjective} {noun} {place} ನಲ್ಲಿದೆ।",
            "{noun} ಮತ್ತು {noun} {verb} ಮಾಡುತ್ತಾರೆ।"
        ]
    },
    "ml": {
        "templates": [
            "{noun} {adjective} ആണ്।",
            "{noun} {verb} ചെയ്യാൻ ഇഷ്ടപ്പെടുന്നു।",
            "ഞാൻ {place} ൽ {verb} ചെയ്യുന്നു।",
            "{adjective} {noun} {place} ൽ ഉണ്ട്।",
            "{noun} ഒപ്പം {noun} {verb} ചെയ്യുന്നു।"
        ]
    },
    "or": {
        "templates": [
            "{noun} {adjective} ଅଟେ।",
            "{noun} {verb} କରିବାକୁ ପସନ୍ଦ କରେ।",
            "ମୁଁ {place} ରେ {verb} କରୁଛି।",
            "{adjective} {noun} {place} ରେ ଅଛି।",
            "{noun} ଏବଂ {noun} {verb} କରନ୍ତି।"
        ]
    },
    "ur": {
        "templates": [
            "{noun} {adjective} ہے۔",
            "{noun} کو {verb} کرنا پسند ہے۔",
            "میں {place} میں {verb} کرتا ہوں۔",
            "{adjective} {noun} {place} میں ہے۔",
            "{noun} اور {noun} {verb} کرتے ہیں۔"
        ]
    }
}

# Function to generate a pseudo-word for a given language
def generate_pseudo_word(lang, min_length=2, max_length=6):
    chars = char_sets[lang]
    word_length = random.randint(min_length, max_length)
    word = []
    
    if lang == "en":
        # English: Generate syllable-based pseudo-words (e.g., "salu")
        for _ in range(word_length // 2):
            if random.random() < 0.8:  # 80% chance for consonant-vowel
                word.append(random.choice(chars["consonants"]))
                word.append(random.choice(chars["vowels"]))
            else:  # Standalone consonant
                word.append(random.choice(chars["consonants"]))
        if random.random() < 0.5:  # 50% chance to end with vowel
            word.append(random.choice(chars["vowels"]))
    else:
        # Indic/Urdu: Generate script-based pseudo-words
        # Start with an independent vowel or consonant
        if random.random() < 0.3:  # 30% chance to start with independent vowel
            word.append(random.choice(chars["independent_vowels"]))
        else:
            word.append(random.choice(chars["consonants"]))
        
        # Add consonant-vowel pairs or standalone consonants
        for _ in range(word_length - 1):
            if random.random() < 0.7:  # 70% chance to add consonant-vowel
                word.append(random.choice(chars["consonants"]))
                word.append(random.choice(chars["vowels"]))
            else:  # Add standalone consonant
                word.append(random.choice(chars["consonants"]))
    
    return "".join(word)

# Function to generate a sentence for a given language
def generate_sentence(lang):
    templates = template_adjustments[lang]["templates"]
    template = random.choice(templates)
    sentence = template.format(
        noun=generate_pseudo_word(lang),
        verb=generate_pseudo_word(lang),
        adjective=generate_pseudo_word(lang),
        place=generate_pseudo_word(lang)
    )
    return sentence

# Function to clean and normalize text
def clean_text(text, lang):
    # Remove any symbols or numbers
    text = ''.join(c for c in text if c.isalpha() or c.isspace() or c in "।")
    if lang == "en":
        # English: Simple cleaning, no normalization needed
        return ' '.join(text.split()).strip()
    else:
        # Indic/Urdu: Normalize and tokenize
        normalizer = indic_normalize.IndicNormalizerFactory().get_normalizer(lang)
        text = normalizer.normalize(text)
        tokens = indic_tokenize.trivial_tokenize(text, lang)
        return ' '.join(tokens).strip()

# Generate dataset for each language (10,000 sentences)
def generate_dataset(lang, num_sentences=10000, output_dir="indic_datasets"):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{lang}.txt")
    sentences = []
    
    for _ in range(num_sentences):
        sentence = generate_sentence(lang)
        sentence = clean_text(sentence, lang)
        if sentence:  # Ensure non-empty sentences
            sentences.append(sentence)
    
    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.write(sentence + "\n")
    
    print(f"Generated dataset for {lang}: {output_file}")

# Generate datasets for all languages 
# It will create a folder named 'indic_datasets' and save the .txt files in it
languages = ["en", "kn", "ml", "or", "ur"]
for lang in languages:
    generate_dataset(lang)