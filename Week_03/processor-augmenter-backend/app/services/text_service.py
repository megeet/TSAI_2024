from typing import Dict
from transformers import AutoTokenizer
import nltk
from nltk.corpus import wordnet
import random
import os

class TextService:
    def __init__(self):
        try:
            # Create a directory for NLTK data
            nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
            os.makedirs(nltk_data_dir, exist_ok=True)
            nltk.data.path.append(nltk_data_dir)

            # Download only required English data
            required_packages = {
                'tokenizers/punkt/english.pickle': 'punkt',  # English sentence tokenizer
                'taggers/averaged_perceptron_tagger/english.pickle': 'averaged_perceptron_tagger',  # English POS tagger
                'corpora/wordnet': 'wordnet'  # English WordNet
            }

            for file_path, package in required_packages.items():
                try:
                    print(f"Downloading {package} for English...")
                    nltk.download(package, download_dir=nltk_data_dir, quiet=True)
                except Exception as e:
                    print(f"Error downloading {package}: {e}")

            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            self.insertions = {
                'adjectives': ['interesting', 'remarkable', 'notable', 'significant', 'important'],
                'adverbs': ['notably', 'interestingly', 'remarkably', 'significantly', 'particularly'],
                'phrases': [', in fact,', ', indeed,', ', specifically,', ', in particular,']
            }
            self.nltk_initialized = True
            print("NLTK initialization completed successfully")
        except Exception as e:
            print(f"Error during initialization: {e}")
            self.nltk_initialized = False
            self.tokenizer = None

    def get_synonyms(self, word: str) -> list:
        if not self.nltk_initialized:
            return []
        try:
            synonyms = []
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.name() != word and '_' not in lemma.name():
                        synonyms.append(lemma.name())
            return list(set(synonyms))
        except Exception as e:
            print(f"Error getting synonyms for {word}: {e}")
            return []

    def augment_text(self, text: str) -> str:
        if not self.nltk_initialized:
            return f"Error: Text augmentation is not available (NLTK initialization failed)"
        
        try:
            sentences = text.split('. ')
            if not sentences:
                return text

            augmented_sentences = []
            for sentence in sentences:
                if not sentence:
                    continue
                    
                try:
                    words = sentence.split()
                    pos_tags = nltk.pos_tag(words)
                    
                    augmented_words = []
                    for word, tag in pos_tags:
                        if random.random() < 0.3:
                            if tag.startswith(('NN', 'VB', 'JJ', 'RB')):
                                synonyms = self.get_synonyms(word)
                                if synonyms:
                                    if random.random() < 0.5:
                                        # Mark augmented words with <aug> tags
                                        augmented_words.append(f"<aug>{random.choice(synonyms)}</aug>")
                                        if random.random() < 0.2:
                                            insertion_type = random.choice(['adjectives', 'adverbs', 'phrases'])
                                            augmented_words.append(f"<aug>{random.choice(self.insertions[insertion_type])}</aug>")
                                        continue
                        augmented_words.append(word)

                    augmented_sentence = ' '.join(augmented_words)
                    augmented_sentence = augmented_sentence.replace(' ,', ',')
                    augmented_sentence = augmented_sentence.replace(' .', '.')
                    augmented_sentence = augmented_sentence.replace(' !', '!')
                    augmented_sentence = augmented_sentence.replace(' ?', '?')
                    augmented_sentences.append(augmented_sentence)
                except Exception as e:
                    print(f"Error processing sentence: {e}")
                    augmented_sentences.append(sentence)

            return '. '.join(augmented_sentences)
        except Exception as e:
            print(f"Error during augmentation: {e}")
            return f"Error during text augmentation: {str(e)}"

    def process_text(self, text: str) -> Dict[str, str]:
        # 1. Add newlines after periods
        text_with_newlines = text.replace('. ', '.\n')
        
        # 2. Convert to lowercase
        processed_text = text_with_newlines.lower()

        # 3. Tokenize the text and get token IDs
        try:
            if self.tokenizer:
                # Get both tokens and their IDs
                encoded = self.tokenizer.encode_plus(text, add_special_tokens=False)
                tokens = self.tokenizer.convert_ids_to_tokens(encoded['input_ids'])
                token_ids = encoded['input_ids']
                
                # Combine tokens with their IDs without space
                tokens_with_ids = [f"{token}[{token_id}]" for token, token_id in zip(tokens, token_ids)]
                tokens_str = ' '.join(tokens_with_ids)
            else:
                # Fallback to basic tokenization
                import re
                tokens = re.findall(r'\w+|[^\w\s]', text)
                tokens_str = ' '.join(f"{token}[N/A]" for token in tokens)
        except Exception as e:
            print(f"Error during tokenization: {e}")
            tokens_str = "Error during tokenization"

        return {
            "processed_text": processed_text,
            "tokens": tokens_str
        }