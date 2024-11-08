from typing import Dict
from transformers import AutoTokenizer

class TextService:
    def __init__(self):
        # Initialize the tokenizer (using a basic BERT tokenizer)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            # Fallback to basic tokenization if transformer fails
            self.tokenizer = None

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

    def augment_text(self, text: str) -> str:
        return f"Augmented: {text}"