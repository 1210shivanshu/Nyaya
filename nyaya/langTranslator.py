# langTranslator.py  — USE THIS NEW VERSION

from deep_translator import GoogleTranslator

class MinimalIndianTranslator:
    def __init__(self):
        self.chunk_size = 300

    def set_chunk_size(self, size):
        self.chunk_size = size

    def translate(self, text, source_lang, target_lang):
        """
        Translate text using free Google Translate (deep_translator)
        """
        try:
            if source_lang == target_lang:
                return text

            if not text or not text.strip():
                return text

            # Auto chunking for long text
            if len(text) > self.chunk_size:
                chunks = [text[i:i+self.chunk_size] for i in range(0, len(text), self.chunk_size)]
                translated_chunks = [
                    GoogleTranslator(source=source_lang, target=target_lang).translate(chunk)
                    for chunk in chunks
                ]
                return " ".join(translated_chunks)

            return GoogleTranslator(source=source_lang, target=target_lang).translate(text)

        except Exception as e:
            print("Translation Error:", e)
            return text  # fallback to original text
