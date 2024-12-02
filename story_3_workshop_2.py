import os
import io
from sklearn.feature_extraction.text import CountVectorizer
#quelques variables globales utiles
PATH_TO_HAM_DIR = r"C:\Users\marwane.boukili\Documents\Github\workshop\emails\ham"
PATH_TO_SPAM_DIR = r"C:\Users\marwane.boukili\Documents\Github\workshop\emails\spam"
 
SPAM_TYPE = "SPAM"
HAM_TYPE = "HAM"
 
#les tableaux X et Y seront ordonnés et de la même taille
# X représente l'input Data (ici les mails)
X = []
#indique s'il s'agit d'un mail ou non
Y = [] #les etiquettes (labels) pour le training set
 
 
def readFilesFromDirectory(path, classification):
    os.chdir(path)
    files_name = os.listdir(path)
    for current_file in files_name:
        message = extract_mail_body(current_file)
        X.append(message)
        Y.append(classification)
        
            
 
def extract_mail_body(file_name_str):
    inBody = False
    lines = []
    file_descriptor = io.open(file_name_str,'r', encoding='latin1')
    for line in file_descriptor:
        if inBody:
            lines.append(line)
        elif line == '\n':
            inBody = True
        message = '\n'.join(lines)
    file_descriptor.close()
    return message
 
 
readFilesFromDirectory(PATH_TO_HAM_DIR, HAM_TYPE)
readFilesFromDirectory(PATH_TO_SPAM_DIR, SPAM_TYPE)

vectorizer = CountVectorizer()
 
counts = vectorizer.fit_transform(training_set['X'].values)

classifier = MultinomialNB()
targets = training_set['Y'].values
classifier.fit(counts, targets)