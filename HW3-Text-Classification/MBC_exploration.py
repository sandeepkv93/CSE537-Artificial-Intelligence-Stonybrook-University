import sys
import sklearn, sklearn.datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
import os, os.path
import shutil
import codecs
import copy
from nltk.stem import *


def apply_stemming(data):
    stemmer = PorterStemmer()
    stemmed = copy.deepcopy(data)

    for i in range(len(stemmed.data)):
        stemmed_words = []
        for word in stemmed.data[i].split():
            stemmed_words.append(stemmer.stem(word))
        stemmed.data[i] = ' '.join(stemmed_words)
    return stemmed
    ''' 
    Stopwords generated by executing this command
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stopwords.words('english')
    '''


def removeStopwords(input_data):
    stopword_free_data = copy.deepcopy(input_data)
    stopwords = [
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
        'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
        'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
        'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who',
        'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
        'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
        'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
        'about', 'against', 'between', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
        'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
        'can', 'will', 'just', 'don', 'should', 'now'
    ]

    for i in range(len(stopword_free_data.data)):
        removed_stopwords = []
        for word in stopword_free_data.data[i].split():
            if not word.lower() in stopwords:
                removed_stopwords.append(word)
        stopword_free_data.data[i] = ' '.join(removed_stopwords)
    return stopword_free_data


def preprocess_data(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    preprocessed_path = dir_path + '/preprocessed' + path
    if not os.path.exists(preprocessed_path):
        shutil.copytree(dir_path + path, preprocessed_path)
    else:
        return
    for dirpath, dirnames, files in os.walk(preprocessed_path):
        for name in files:
            f = codecs.open(os.path.join(dirpath, name), 'r+', 'utf8', 'ignore')
            _, _, text = f.read().partition('\n\n')
            f.seek(0)
            f.write(text)
            f.truncate()
            f.close()


def runconfiguration1(train, test):
    stopword_free_data_train = removeStopwords(train)
    stopword_free_data_test = removeStopwords(test)
    classifier = Pipeline([('vect', CountVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(stopword_free_data_train.data,
                                    stopword_free_data_train.target).predict(
                                        stopword_free_data_test.data)
    global output
    output += 'SVM, RemovedStoppedWords+CountVectorizer, ' + str(
        round(
            metrics.precision_score(
                stopword_free_data_test.target, classification,
                average='macro'), 2)) + ', ' + str(
                    round(
                        metrics.recall_score(
                            stopword_free_data_test.target,
                            classification,
                            average='macro'), 2)) + ', ' + str(
                                round(
                                    metrics.f1_score(
                                        stopword_free_data_test.target,
                                        classification,
                                        average='macro'), 2)) + '\n'


def runconfiguration2(train, test):
    stopword_free_data_train = removeStopwords(train)
    stopword_free_data_test = removeStopwords(test)
    classifier = Pipeline([('vect', TfidfVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(stopword_free_data_train.data,
                                    stopword_free_data_train.target).predict(
                                        stopword_free_data_test.data)
    global output
    output += 'SVM, RemovedStoppedWords+TfidfVectorizer, ' + str(
        round(
            metrics.precision_score(
                stopword_free_data_test.target, classification,
                average='macro'), 2)) + ', ' + str(
                    round(
                        metrics.recall_score(
                            stopword_free_data_test.target,
                            classification,
                            average='macro'), 2)) + ', ' + str(
                                round(
                                    metrics.f1_score(
                                        stopword_free_data_test.target,
                                        classification,
                                        average='macro'), 2)) + '\n'


def runconfiguration3(train, test):
    stopword_free_data_and_stemmed_train = apply_stemming(
        removeStopwords(train))
    stopword_free_data_and_stemmed_test = apply_stemming(removeStopwords(test))
    classifier = Pipeline([('vect', CountVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(
        stopword_free_data_and_stemmed_train.data,
        stopword_free_data_and_stemmed_train.target).predict(
            stopword_free_data_and_stemmed_test.data)
    global output
    output += 'SVM, RemovedStoppedWords+Stemmed+CountVectorizer, ' + str(
        round(
            metrics.precision_score(
                stopword_free_data_and_stemmed_test.target,
                classification,
                average='macro'), 2)) + ', ' + str(
                    round(
                        metrics.recall_score(
                            stopword_free_data_and_stemmed_test.target,
                            classification,
                            average='macro'),
                        2)) + ', ' + str(
                            round(
                                metrics.f1_score(
                                    stopword_free_data_and_stemmed_test.target,
                                    classification,
                                    average='macro'), 2)) + '\n'


def runconfiguration4(train, test):
    stopword_free_data_and_stemmed_train = apply_stemming(
        removeStopwords(train))
    stopword_free_data_and_stemmed_test = apply_stemming(removeStopwords(test))
    classifier = Pipeline([('vect', TfidfVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(
        stopword_free_data_and_stemmed_train.data,
        stopword_free_data_and_stemmed_train.target).predict(
            stopword_free_data_and_stemmed_test.data)
    global output
    output += 'SVM, RemovedStoppedWords+Stemmed+TfidfVectorizer, ' + str(
        round(
            metrics.precision_score(
                stopword_free_data_and_stemmed_test.target,
                classification,
                average='macro'), 2)) + ', ' + str(
                    round(
                        metrics.recall_score(
                            stopword_free_data_and_stemmed_test.target,
                            classification,
                            average='macro'),
                        2)) + ', ' + str(
                            round(
                                metrics.f1_score(
                                    stopword_free_data_and_stemmed_test.target,
                                    classification,
                                    average='macro'), 2)) + '\n'


def runconfiguration5(train, test):
    stopword_free_data_and_stemmed_train = apply_stemming(
        removeStopwords(train))
    stopword_free_data_and_stemmed_test = apply_stemming(removeStopwords(test))
    classifier = Pipeline([('vect', CountVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('selector', SelectFromModel(
                               LinearSVC(penalty="l2"))),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(
        stopword_free_data_and_stemmed_train.data,
        stopword_free_data_and_stemmed_train.target).predict(
            stopword_free_data_and_stemmed_test.data)
    global output
    output += 'SVM, RemovedStoppedWords+Stemmed+CountVectorizer+L2, ' + str(
        round(
            metrics.precision_score(
                stopword_free_data_and_stemmed_test.target,
                classification,
                average='macro'), 2)) + ', ' + str(
                    round(
                        metrics.recall_score(
                            stopword_free_data_and_stemmed_test.target,
                            classification,
                            average='macro'),
                        2)) + ', ' + str(
                            round(
                                metrics.f1_score(
                                    stopword_free_data_and_stemmed_test.target,
                                    classification,
                                    average='macro'), 2)) + '\n'


def runconfiguration6(train, test):
    stopword_free_data_and_stemmed_train = apply_stemming(
        removeStopwords(train))
    stopword_free_data_and_stemmed_test = apply_stemming(removeStopwords(test))
    classifier = Pipeline([('vect', TfidfVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('selector', SelectFromModel(
                               LinearSVC(penalty="l2"))),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(
        stopword_free_data_and_stemmed_train.data,
        stopword_free_data_and_stemmed_train.target).predict(
            stopword_free_data_and_stemmed_test.data)
    global output
    output += 'SVM, RemovedStoppedWords+Stemmed+TfidfVectorizer+L2, ' + str(
        round(
            metrics.precision_score(
                stopword_free_data_and_stemmed_test.target,
                classification,
                average='macro'), 2)) + ', ' + str(
                    round(
                        metrics.recall_score(
                            stopword_free_data_and_stemmed_test.target,
                            classification,
                            average='macro'),
                        2)) + ', ' + str(
                            round(
                                metrics.f1_score(
                                    stopword_free_data_and_stemmed_test.target,
                                    classification,
                                    average='macro'), 2)) + '\n'


def runconfiguration7(train, test):
    stemmed_train = apply_stemming(train)
    stemmed_test = apply_stemming(test)
    classifier = Pipeline([('vect', CountVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('selector', SelectFromModel(
                               LinearSVC(penalty="l2"))),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(stemmed_train.data,
                                    stemmed_train.target).predict(
                                        stemmed_test.data)
    global output
    output += 'SVM, Stemmed+CountVectorizer+L2, ' + str(
        round(
            metrics.precision_score(
                stemmed_test.target, classification, average='macro'),
            2)) + ', ' + str(
                round(
                    metrics.recall_score(
                        stemmed_test.target, classification, average='macro'),
                    2)) + ', ' + str(
                        round(
                            metrics.f1_score(
                                stemmed_test.target,
                                classification,
                                average='macro'), 2)) + '\n'


def runconfiguration8(train, test):
    stemmed_train = apply_stemming(train)
    stemmed_test = apply_stemming(test)
    classifier = Pipeline([('vect', TfidfVectorizer()), ('tfidf',
                                                         TfidfTransformer()),
                           ('selector', SelectFromModel(
                               LinearSVC(penalty="l2"))),
                           ('clf',
                            LinearSVC(
                                loss='hinge', penalty='l2', random_state=42))])
    classification = classifier.fit(stemmed_train.data,
                                    stemmed_train.target).predict(
                                        stemmed_test.data)
    global output
    output += 'SVM, Stemmed+TfidfVectorizer+L2, ' + str(
        round(
            metrics.precision_score(
                stemmed_test.target, classification, average='macro'),
            2)) + ', ' + str(
                round(
                    metrics.recall_score(
                        stemmed_test.target, classification, average='macro'),
                    2)) + ', ' + str(
                        round(
                            metrics.f1_score(
                                stemmed_test.target,
                                classification,
                                average='macro'), 2)) + '\n'


def classification_exploaration(train, test):
    print('Configuration 1: RemovedStoppedWords+CountVectorizer')
    runconfiguration1(train, test)

    print('Configuration 2: RemovedStoppedWords+TfidfVectorizer')
    runconfiguration2(train, test)

    print('Configuration 3: RemovedStoppedWords+Stemmed+CountVectorizer')
    runconfiguration3(train, test)

    print('Configuration 4: RemovedStoppedWords+Stemmed+TfidfVectorizer')
    runconfiguration4(train, test)

    print('Configuration 5: RemovedStoppedWords+Stemmed+CountVectorizer+L2')
    runconfiguration5(train, test)

    print('Configuration 6: RemovedStoppedWords+Stemmed+TfidfVectorizer+L2')
    runconfiguration6(train, test)

    print('Configuration 7: Stemmed+CountVectorizer+L2')
    runconfiguration7(train, test)

    print('Configuration 8: Stemmed+TfidfVectorizer+L2')
    runconfiguration8(train, test)


def write_to_output_file(file_path):
    with open(file_path + '.txt', 'w') as f:
        f.write(output)
    print('Output Written to the Output File: ', file_path + '.txt')


if __name__ == "__main__":
    output = ''
    training_file_path = sys.argv[1]
    preprocess_data(training_file_path)
    training = sklearn.datasets.load_files(
        'preprocessed' + training_file_path,
        categories=[
            'rec.sport.hockey', 'sci.med', 'soc.religion.christian',
            'talk.religion.misc'
        ],
        encoding="utf-8",
        decode_error="replace",
        shuffle=True,
        random_state=42)

    test_file_path = sys.argv[2]
    preprocess_data(test_file_path)
    test = sklearn.datasets.load_files(
        'preprocessed' + test_file_path,
        categories=[
            'rec.sport.hockey', 'sci.med', 'soc.religion.christian',
            'talk.religion.misc'
        ],
        encoding="utf-8",
        decode_error="replace",
        shuffle=True,
        random_state=42)

    classification_exploaration(training, test)
    write_to_output_file(sys.argv[3])