from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

if __name__ == '__main__':
    words = ["fucked","jerked","sucked"]
    opts = ["a","r","v","n"]
    for word in words:
        lemmas = []
        for opt in opts:
            lemma = lemmatizer.lemmatize(word,pos=opt)
            if lemma != word:
                lemmas.append(lemma)
                break
        if len(lemmas) == 0:
            lemmas.append(word)
        print("{:20s} ==> {:20s}".format(word,','.join(lemmas)))