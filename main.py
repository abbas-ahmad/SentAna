import nltk
from nltk.corpus import stopwords
import re
import pickle

pos = open('positive4.txt', 'r').read()
neg = open("negative4.txt", 'r').read()
######################################


def process_data(data):
    data = data.lower()
    data = re.sub('[\s]+', ' ', data)
    data = data.strip(' \'"?,. !')
    data = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', data)
    # Convert @username to AT_USER
    data = re.sub('@[^\s]+', 'AT_USER', data)
    data = re.sub(r'#([^\s]+)', r'\1', data)
    # print data
    return data


def replace_two_or_more(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def get_stopwords(stopwords_file):
    sw.append("AT_USER")
    sw.append("URL")
    fp = open(stopwords_file , 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        sw.append(word)
        line = fp.readline()
    return sw


def get_feature_vector(data):
    feature_vector = []
    words = data.split()
    for w in words:
        w = get_feature_vector(w)
        w = w.strip('\'"?,.!')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if w in sw or val is None:
            continue
        else:
            feature_vector.append(w.lower())
    return feature_vector


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in document_words)
    return features


########################################

documents = []
featureList = []
sw = stopwords.words('english')
sw = get_stopwords("stop_words.txt")

for review in pos.split('\n'):
    processedData = process_data(review)
    feature_vector = get_feature_vector(processedData)
    documents.append((feature_vector, 'positive'))

for review in neg.split('\n'):
    processedData = process_data(review)
    feature_vector = get_feature_vector(processedData)
    featureList.extend(feature_vector)
    documents.append((feature_vector, 'negative'))

save_document = open("pickled_algos3/documents.pickle", "wb")
pickle.dump(documents, save_document)
save_document.close()

featureList = list(set(featureList))
# fp = open("featureList.txt", 'w')
# fp.write(str(featureList))
# print featureList

save_featList = open("pickled_algos3/featurelist.pickle", "wb")
pickle.dump(featureList , save_featList )
save_featList.close()

#print "building feature set "
training_set = nltk.classify.apply_features(extract_features ,documents)

nbc = nltk.NaiveBayesClassifier.train(training_set)
nbc.show_most_informative_features(20)
save_nbc = open("pickled_algos3/nbc.pickle" , "wb")
pickle.dump(nbc , save_nbc)
save_nbc.close()




