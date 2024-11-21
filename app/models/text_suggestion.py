from typing import List, Union

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text: Union[str, List[str]], n_words=3, n_texts=1) -> List[List[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """
        print("Starting text suggestion...")
        suggestions = []

        # Преобразуем входной текст в список слов
        if isinstance(text, str):
            words = text.strip().split()
        else:
            words = text[:]
        
        print(f"Input words: {words}")
        
        if not words:
            print("No words provided, returning empty suggestions.")
            return []
        
        # Завершаем последнее слово
        last_word = words[-1]
        print(f"Last word to complete: {last_word}")
        completions, probs = self.word_completor.get_words_and_probs(last_word)
        print(f"Word completions: {completions}")
        print(f"Completion probabilities: {probs}")
        
        if completions:
            max_prob_index = probs.index(max(probs))
            completed_word = completions[max_prob_index]
            print(f"Selected completed word: {completed_word}")
        else:
            print("No completions found. Using the last word as is.")
            completed_word = last_word

        # Создаем список слов, включая дополненное
        full_words = words[:-1] + [completed_word]
        print(f"Full words after completion: {full_words}")
        
        suggestion = [completed_word]
        n = self.n_gram_model.n
        
        # Определяем контекст для n-граммной модели
        if n > 1:
            context = full_words[-(n - 1):]
        else:
            context = []
        print(f"Initial context for n-gram model: {context}")

        # Генерация следующих слов
        for _ in range(n_words):
            next_words, next_probs = self.n_gram_model.get_next_words_and_probs(context)
            print(f"Next words: {next_words}")
            print(f"Next probabilities: {next_probs}")

            if not next_words:
                print("No more words to predict. Breaking loop.")
                break
            
            max_prob_index = next_probs.index(max(next_probs))
            next_word = next_words[max_prob_index]
            print(f"Selected next word: {next_word}")
            
            suggestion.append(next_word)

            # Обновляем контекст
            if n > 1:
                context = context[1:] + [next_word]
            else:
                context = [next_word]
            print(f"Updated context: {context}")
        
        # Добавляем предложение в список результатов
        suggestions.append(suggestion)
        print(f"Final suggestion: {suggestion}")
        return suggestions
