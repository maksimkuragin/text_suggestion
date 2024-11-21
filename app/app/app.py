import reflex as rx

from rxconfig import config
from models import PrefixTreeNode, PrefixTree, WordCompletor, NGramLanguageModel, TextSuggestion
from utils import load_and_clean_data

# Global or class-level variables
print("Loading and cleaning data...")
corpus = load_and_clean_data()
print(f"Corpus loaded: {len(corpus)} documents")

# Reduce corpus size for easier processing
reduced_corpus_size = 20
corpus = corpus[:reduced_corpus_size]
print(f"Reduced corpus size: {len(corpus)} documents")

# Transform corpus into a flat list of words for WordCompletor
flat_corpus = [word for sublist in corpus for word in sublist]
print(f"Flat corpus generated: {len(flat_corpus)} words")

print("Initializing WordCompletor...")
word_completor = WordCompletor(flat_corpus)
print("WordCompletor initialized")

print("Initializing NGramLanguageModel...")
ngram_model = NGramLanguageModel(corpus, n=3)  # Using trigrams
print("NGramLanguageModel initialized")

print("Initializing TextSuggestion...")
text_suggester = TextSuggestion(word_completor, ngram_model)
print("TextSuggestion initialized")

class State(rx.State):
    user_input: str = ""
    suggestions: list = []
    predicted_text: str = ""
    display_text: str = ""

    @staticmethod
    def get_suggestions(prefix: str) -> list:
        # Use WordCompletor instance to fetch suggestions
        return word_completor.get_suggestions(prefix)

    def update_text(self, input_text):
        print(f"Updating text: {input_text}")
        self.user_input = input_text
        words = self.user_input.strip().split()
        print(f"Split words: {words}")
        if not words:
            print("No words entered. Resetting suggestions and predictions.")
            self.suggestions = []
            self.predicted_text = ''
            self.display_text = ''
            return

        # Complete the last word
        last_word = words[-1]
        print(f"Last word: {last_word}")
        completions, probs = word_completor.get_words_and_probs(last_word)
        print(f"Completions: {completions}, Probabilities: {probs}")
        if completions:
            max_prob_index = probs.index(max(probs))
            completed_word = completions[max_prob_index]
            print(f"Most probable completion: {completed_word}")
            # Update display_text with the completed word
            display_words = words[:-1] + [completed_word]
            self.display_text = ' '.join(display_words)
        else:
            print("No completions found.")
            self.display_text = self.user_input

        # Get predictions for the next words
        predicted = text_suggester.suggest_text(words, n_words=3, n_texts=1)
        print(f"Predicted text: {predicted}")
        if predicted:
            # Show the suggested next words
            self.predicted_text = ' '.join(predicted[0][len(words):])
        else:
            self.predicted_text = ''

    def select_suggestion(self, suggestion):
        print(f"Suggestion selected: {suggestion}")
        # Append the suggestion to the user_input
        self.user_input = self.user_input.strip() + ' ' + suggestion + ' '
        print(f"Updated user input: {self.user_input}")
        self.display_text = self.user_input
        # Reset suggestions
        self.suggestions = []
        self.predicted_text = ''

def index() -> rx.Component:
    # Main page
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Text Suggestion App", size="9"),
            rx.input(
                placeholder="Type something...",
                value=State.user_input,  # Bind to user_input
                on_change=State.update_text,  # Call update_text on change
            ),
            rx.text("Suggestions:"),
            rx.cond(
                State.predicted_text != '',
                rx.button(
                    State.predicted_text,
                    on_click=lambda: State.select_suggestion(State.predicted_text)
                ),
                rx.text("No suggestions")
            ),
            rx.text("Completed Text:"),
            rx.text(State.display_text),  # Display text with completion
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

app = rx.App()
app.add_page(index)
