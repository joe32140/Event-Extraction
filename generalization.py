from nltk.corpus import wordnet as wn
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.corpus import verbnet as vn
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tag import StanfordPOSTagger

class Generalization():
    def __init__(self, hypernym_level=2):
        self.hypernym_level=hypernym_level
        self.type_dic={'V':'v', 'N':'n', 'J':'s', 'D':'n', 'R':'n', 'C':'n', 'I':'n', 'W':'n', 'F':'n', 'S':'n', 'U':'n'}

    def run(self, events):
        output=[]
        for e in events:
            #print(e)
            tmp=[]
            #print("============S=============")
            tmp.append(self.get_hypernym(e[0]))
            #print("============v=============")
            tmp.append(self.replace_verb(e[1]))
            #print("============o=============")
            tmp.append(self.get_hypernym(e[2]))
            #print("============m=============")
            tmp.append(self.get_hypernym(e[3], modifier=True))
            output.append(' '.join(tmp))
        return output


    def get_hypernym(self, word, modifier=False):

        word, word_type = word[0], word[1]
        if '_' in word:
            word = word.split('_')[0].lower()

        if word_type=='PRP' or word_type=='PRP$' or word_type=='<empty>' or word=='i' or word == 'one':
            return word
        syn_words = wn.synsets(word)
        if len(syn_words)==0:
            #print("{} no synset".format(word))
            return '<unk>'
        #find noun in synset
        flag=0
        #print(syn_words)
        for syn_word in syn_words:
            #print(syn_word.name())
            if word_type[0] not in self.type_dic.keys():
                continue
            if syn_word.name().split('.')[1]==self.type_dic[word_type[0]] or modifier==True:
                word=syn_word #get 'go'
                flag=1
                break
        if flag==0:
            print("error: no noun \"{}\"".format(word))
            return word

        for l in range(self.hypernym_level):
            hypernym = word.hypernyms()
            # check if word has hypernym and the hypernym is not too general e.g. entity
            if len(hypernym) != 0 and "entity" not in hypernym[0].name().split('.')[0].split("_"):
                word = hypernym[0]
            else:
                print(hypernym)
                break
        #print("Hi",word.name())
        return word.name()

    def replace_verb(self, word):
        # I have no idea how to access verbnet by wordnetid, any help is welcome!
        #w_id = wn.synsets(verb)[0].id()
        #verbnet.classids(wordnetid=w_id)
        word, word_type = word[0], word[1]
        if word_type=='<empty>':
            return word

        syn_words = wn.synsets(word) #get 'go.v.01' if verb is 'go', verbnet only takes present tense
        if len(syn_words)==0:
            print("error: no syn_word \"{}\"".format(word))
            return '<unk>'
        #print(syn_words)
        #find verb in synset
        flag=0
        #print(syn_words)
        for syn_word in syn_words:
            syn_word = syn_word.name()
            if syn_word.split('.')[1]=='v':
                verb=syn_word.split('.')[0] #get 'go'
                flag=1
                break
        if flag==0:
            print("error: no verb 1\"{}\"".format(word))
            return word
        #print(verb)
        g_verbs = vn.classids(lemma=verb)  #'escape-51.1-2'
        if len(g_verbs)==0:
            print("error: no verb 2 \"{}\"".format(word))
            return verb
        return g_verbs[0]

class DependencyParser():
    def __init__(self):

        path2jar = '/home/bendan0617/stanford-corenlp-full-2018-02-27/stanford-corenlp-3.9.1.jar'
        path2model = '/home/bendan0617/stanford-corenlp-full-2018-02-27/stanford-corenlp-3.9.1-models.jar'
        self.dep_parser = StanfordDependencyParser(path_to_jar=path2jar, path_to_models_jar=path2model, java_options='-mx100g')

    def parse_sents(self, sents):
        """
        Parameters:
        sents: list of string

        Reutrns: list of list of triples
        """
        parsed_sents = self.dep_parser.raw_parse_sents(sents)
        return [[list(parse.triples()) for parse in parsed_sent]for parsed_sent in parsed_sents]

    def get_SVOM(self, sents):
        parsed_sents = self.parse_sents(sents)
        output=[]
        for sent in parsed_sents:
            tmp={'V':('<empty>','<empty>'), 'S':('<empty>','<empty>'),
                    'O':('<empty>','<empty>'), 'M':('<empty>','<empty>')}
            for triple in sent[0]:
                t1, t2, t3 = triple[0], triple[1], triple[2]
                if t2[0:5]=='nsubj' and t1[1][0]=='V':
                    if tmp['V'][0]=='<empty>' and t1[1][0] =='V': tmp['V']=t1
                    if tmp['S'][0]=='<empty>': tmp['S']=t3
                elif t2=='nsubj' and t1[1][0] in 'VJNP':
                    if tmp['O'][0]=='<empty>': tmp['O']=t1
                    if tmp['S'][0]=='<empty>': tmp['S']=t3
                elif t2=='cop':
                    if tmp['O'][0]=='<empty>': tmp['O']=t1
                    if tmp['V'][0]=='<empty>': tmp['V']=t3
                elif t2=='dobj':
                    if tmp['V'][0]=='<empty>': tmp['V']=t1
                    if tmp['O'][0]=='<empty>': tmp['O']=t3
                elif t2=='ccomp' or t2=='iobj' or t2=='pobj' or t2=='xcomp':
                    #if tmp['S'][0]=='<empty>':
                       # tmp['S']=t3
                    if tmp['M'][0]=='<empty>':
                        tmp['M']=t3
                elif t2 == 'auxpass':
                    if tmp['V'][0]=='<empty>': tmp['V']=t1
                    if tmp['S'][0]!='<empty>':
                        tmp['O']=tmp['S']
                        tmp['S']=('<empty>','<empty>')
                #elif t2[0:3] == 'acl':
                #    if tmp['S'][0]=='<empty>': tmp['S']=t1
                elif t2[0:4] == 'nmod':
                   # if tmp['V'][0]=='<empty>' and t1[1][0] =='V': tmp['V']=t1
                    if tmp['O'][0]=='<empty>': tmp['O']=t3
                elif t2 == 'dep':
                    if tmp['S'][0]=='<empty>' and t1[1][0] != 'V' : tmp['M']=t1
                #elif t2 == 'xcomp':
                 #   if tmp['S'][0]=='<empty>' and t1[1][0] != 'V' : tmp['S']=t1
                else:
                    continue
            output.append([tmp['S'], tmp['V'], tmp['O'], tmp['M']])
        return output, parsed_sents


class NERparser():
    def __init__(self):
        self.st = StanfordNERTagger('/home/joe32140/stanford/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
                               '/home/joe32140/stanford/stanford-ner-2018-02-27/stanford-ner.jar',
                                                   encoding='utf-8')

    def getNER_sents(self, sents):
        tokenized_sents = [word_tokenize(sent) for sent in sents]
        classified_sents = self.st.tag_sents(tokenized_sents)
        return classified_sents

    def count_entity(self, entity, table):

        if entity[0] not in table[entity[1]]:
            table[entity[1]][entity[0]]=str(len(table[entity[1]].keys()))
        return table[entity[1]][entity[0]]


    def replace(self, sents):
        classified_sents =self.getNER_sents(sents)
        new_sentences=[]
        for i, sent in enumerate(classified_sents):
            if i%5==0:
                check_repeat={'PERSON':{}, 'LOCATION':{}, 'ORGANIZATION':{}}
            tmp=[]
            for w in sent:
                if w[1]!='O':
                    count = self.count_entity(w, check_repeat)
                    tmp.append(w[1]+'_'+str(count))
                else:
                    tmp.append(w[0])
            new_sentences.append(' '.join(tmp))
        return new_sentences

class POSTagger():
    def __init__(self):
        jar = '/home/joe32140/stanford/stanford-postagger-2018-02-27/stanford-postagger.jar'
        model = '/home/joe32140/stanford/stanford-postagger-2018-02-27/models/english-bidirectional-distsim.tagger'
        self.tagger = StanfordPOSTagger(model, jar, encoding='utf8')

    def getPOS_sents(self, sents):
        tokenized_sents = [word_tokenize(sent) for sent in sents]
        classified_sents = self.tagger.tag_sents(tokenized_sents)
        return classified_sents

    def get_Noun(self, sents):
        classified_sents =self.getPOS_sents(sents)
        new_sentences=[]
        for i, sent in enumerate(classified_sents):
            tmp=[]
            for w in sent:
                if w[1][0] == 'N':
                    tmp.append(w[0])
            new_sentences.append(' '.join(tmp))
        return new_sentences

if __name__ == '__main__':
    #parser = DependencyParser()
    #G = Generalization()
    #ner_parser = NERparser()
    pos_tagger = POSTagger()
    #sents = ['lots of folks come out and set up tables to sell their crafts .']
    sents = ['Ben is a genius boy coming from Taiwan and Mark\'s brother Joe works in Microsoft and Facebook.',
            'Joe\'s young .']
    print(pos_tagger.get_Noun(sents))
    """
    a, parsed_sents=parser.get_SVOM(sents)
    for i in range(len(a)):
        print("========================")
        print(sents[i])
        print(parsed_sents[i])
        print(a[i])
        print(G.run(a)[i])
    """
