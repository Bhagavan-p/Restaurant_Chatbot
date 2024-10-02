from collections import Counter
import re
from collections import Counter
import spacy
word2vec = spacy.load('en')
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
import spacy

word2vec = spacy.load('en')
exit_commands = ("quit", "goodbye", "exit", "no")
response_a = "The {} has a gluten-free option, but it is not vegan"
response_b = "We have a selection of sides to go along with the {}, including mashed potatoes and steamed vegatables."
response_c = "{} includes habanero, so it is a bit spicy!"
blank_spot = "food"
responses = [response_a, response_b, response_c]

def preprocess(input_sentence):
    input_sentence = input_sentence.lower()
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    tokens = word_tokenize(input_sentence)
    input_sentence = [i for i in tokens if not i in stop_words]
    return(input_sentence)

def compare_overlap(user_message, possible_response):
    similar_words = 0
    for token in user_message:
        if token in possible_response:
              similar_words += 1
    return similar_words
  
def extract_nouns(tagged_message):
    message_nouns = list()
    for token in tagged_message:
        if token[1].startswith("N"):
            message_nouns.append(token[0])
    return message_nouns

def compute_similarity(tokens, category):
    output_list = list()
    for token in tokens:
        output_list.append([token.text, category.text, token.similarity(category)])
    return output_list

class ChatBot:
  
  #define .make_exit() below:
  def make_exit(self, user_message):
    for exit_command in exit_commands:
      if exit_command in user_message:
        print("Ok, bye!")
        return True
  #define .chat() below:
  def chat(self):
    user_message = input("Hey! What would you like to know about our menu today? ")
    while not self.make_exit(user_message):
      user_message = self.respond(user_message)
  #define .find_intent_match() below:
  def find_intent_match(self, responses, user_message):
    bow_user_message = Counter(preprocess(user_message))
    processed_responses = [Counter(preprocess(response)) for response in responses]
    similarity_list = [compare_overlap(doc, bow_user_message) for doc in processed_responses]
    response_index = similarity_list.index(max(similarity_list))
    return responses[response_index]
  #define .find_entities() below:
  def find_entities(self, user_message):
    tagged_user_message = pos_tag(preprocess(user_message))
    message_nouns = extract_nouns(tagged_user_message)
    tokens = word2vec(" ".join(message_nouns))
    category = word2vec(blank_spot)
    word2vec_result = compute_similarity(tokens, category)
    word2vec_result.sort(key=lambda x: x[2])
    if len(word2vec_result) < 1:
      return blank_spot
    else:
      return word2vec_result[-1][0]
  #define .respond() below:
  def respond(self, user_message):
    best_response = self.find_intent_match(responses, user_message)
    entity = self.find_entities(user_message)
    print(best_response.format(entity))
    input_message = input("Do you have any other questions? ")           
    return input_message

#initialize ChatBot instance below:
chatbot = ChatBot()
#call .chat() method below:
chatbot.chat()