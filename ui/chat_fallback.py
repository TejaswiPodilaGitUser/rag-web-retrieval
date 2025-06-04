import string

SAMPLE_CONVERSATIONS = [
    {"user": "Hi", "bot": "Hello! How can I assist you today?"},
    {"user": "Hello", "bot": "Hi there! What can I do for you?"},
    {"user": "Hey", "bot": "Hey! How can I help you?"},
    {"user": "How are you?", "bot": "I'm doing great, thanks for asking!"},
    {"user": "What’s your name?", "bot": "I’m your friendly AI assistant."},
    {"user": "Thank you", "bot": "You’re welcome!"},
    {"user": "Thanks", "bot": "Anytime!"},
    {"user": "Can you help me?", "bot": "Of course! What do you need help with?"},
    {"user": "Tell me a joke", "bot": "Why did the scarecrow win an award? Because he was outstanding in his field!"},
    {"user": "What’s the weather like?", "bot": "I don’t have weather info, but I hope it’s nice where you are!"},
    {"user": "Goodbye", "bot": "Goodbye! Have a great day!"},
    {"user": "Bye", "bot": "See you later!"},
    {"user": "What do you do?", "bot": "I answer questions and help you find info."},
    {"user": "Are you human?", "bot": "I’m an AI, but I’m here to help you just like a friend!"},
    {"user": "How old are you?", "bot": "I don’t have an age like humans do, but I’m always learning!"},
    {"user": "Where are you from?", "bot": "I live in the cloud, everywhere and nowhere at the same time."},
    {"user": "What can you do?", "bot": "I can chat with you, answer questions, and help you find information."},
    {"user": "Help", "bot": "Sure! Please tell me what you need help with."},
    {"user": "Who created you?", "bot": "I was created by a team of developers using advanced AI technologies."},
    {"user": "What is AI?", "bot": "AI stands for Artificial Intelligence, which enables machines to think and learn like humans."},
    {"user": "Are you smart?", "bot": "I try my best to be helpful and smart!"},
    {"user": "Tell me something interesting", "bot": "Did you know that honey never spoils? Archaeologists have found edible honey thousands of years old!"},
    {"user": "What is the meaning of life?", "bot": "That’s a big question! Many say it’s to find happiness and help others."},
    {"user": "What languages do you speak?", "bot": "I understand and can respond in many languages, including English."},
    {"user": "Can you learn?", "bot": "I learn from the data and interactions I have, always trying to improve."},
]

GENERIC_FALLBACK = (
    "Sorry, I couldn’t find relevant content. Try asking about GenAI platforms, "
    "ColBERT, hallucinations, embedding search, vector, or related AI topics."
)

def normalize_text(text):
    # Lowercase and remove punctuation
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation)).strip()

def get_fallback_response(user_message):
    normalized_input = normalize_text(user_message)
    for conv in SAMPLE_CONVERSATIONS:
        normalized_question = normalize_text(conv["user"])
        if normalized_question == normalized_input:
            return conv["bot"]
    return GENERIC_FALLBACK
