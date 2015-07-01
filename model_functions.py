from gensim.models import Word2Vec # Gensim code to load Word2Vec model

path  = './data/ADD_MODEL_NAME_HERE'
model = Word2Vec.load_word2vec_format(path, binary=True)

# This works for testing:
# import random
#
# class dummy_model(object):
#     vocab = {'appel':1,'hond':2,'kat':3}
#     def similarity(self,x,y): return random.random()
#     def most_similar(self, positive=None,negative=None): return [('sheep',5),('dog',3)]
#     def doesnt_match(self, l): return 'beschuit'
#
# model = dummy_model()

vocab = set(model.vocab.keys())

def similarity(a,b):
    "Return the similarity between a and b unless either of them is not in the vocabulary."
    if a in vocab and b in vocab:
        return model.similarity(a,b)
    else:
        return None

def get_list_similarity(pairs):
    "Return similarity values for a list of pairs. If the list is empty, return None."
    if len(pairs) > 0:
        return {(a,b):model.similarity(a,b) for a,b in pairs}
    else:
        return None

def get_analogy(a,b,c):
    "Return answers to the analogy a:b::c:???"
    return model.most_similar(positive=[c,b], negative=[a])

def get_similar(l):
    "Return words that are similar to those in l."
    return model.most_similar(positive=l)

def get_outlier(l):
    "Return the word that is the least similar to the other words."
    return model.doesnt_match(l)
