from nltk.corpus import wordnet as wn
from nltk.corpus import verbnet as vn
from nltk.parse.stanford import StanfordDependencyParser

class Generalization():
    def __init__(self, hypernym_level=2):
        self.hypernym_level=hypernym_level

    def run(self, events):
        output=[]
        for e in events:
            tmp=[]
            tmp.append(self.get_hypernym(e[0]))
            tmp.append(self.replace_verb(e[1][0]))#only pass verb
            tmp.append(self.get_hypernym(e[2]))
            tmp.append(self.get_hypernym(e[3]))
            output.append(tmp)
        return output


    def get_hypernym(self, word):
        if word[1]=='PRP':
            return word[0]
        else:
            word=word[0]
        syn_words = wn.synsets(word)
        if len(syn_words)==0:
            print("{} no synset".format(word))
            return word
        #find noun in synset
        flag=0
        for syn_word in syn_words:
            if syn_word.name().split('.')[1]=='n':
                word=syn_word #get 'go'
                flag=1
                break
        if flag==0:
            print("error: no noun \"{}\"".format(word))
            return word

        for l in range(self.hypernym_level):
            hypernym = word.hypernyms()
            # check if word has hypernym and the hypernym is not too general e.g. entity
            if len(hypernym) != 0 and hypernym[0].name().split('.')[0] != "entity":
                word = hypernym[0]
            else:
                print(hypernym)
                break

        return word.name()

    def replace_verb(self, word):
        # I have no idea how to access verbnet by wordnetid, any help is welcome!
        #w_id = wn.synsets(verb)[0].id()
        #verbnet.classids(wordnetid=w_id)

        syn_words = wn.synsets(word) #get 'go.v.01' if verb is 'go', verbnet only takes present tense
        if len(syn_words)==0:
            print("error: no verb \"{}\"".format(word))
            return word

        #find verb in synset
        flag=0
        for syn_word in syn_words:
            syn_word = syn_word.name()
            if syn_word.split('.')[1]=='v':
                verb=syn_word.split('.')[0] #get 'go'
                flag=1
                break
        if flag==0:
            print("error: no verb \"{}\"".format(word))
            return word
        g_verb = vn.classids(lemma=verb)[0]  #'escape-51.1-2'
        return g_verb

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
            tmp={'V':'<empty>', 'S':'<empty>', 'O':'<empty>', 'M':'<empty>'}
            for triple in sent[0]:
                t1, t2, t3 = triple[0], triple[1], triple[2]
                if t2=='nsubj' and t1[1][0]=='V':
                    tmp['V']=t1
                    tmp['S']=t3
                elif t2=='nsubj' and t1[1][0]=='N':
                    tmp['O']=t1
                    tmp['S']=t3
                elif t2=='cop':
                    tmp['O']=t1
                    tmp['V']=t3
                elif t2=='dobj':
                    tmp['V']=t1
                    tmp['O']=t3
                elif t2=='ccomp' or t2=='iobj' or t2=='pobj':
                    tmp['M']=t3
                    continue
                else:
                    continue
            output.append([tmp['S'], tmp['V'], tmp['O'], tmp['M']])
        return output, parsed_sents




if __name__ == '__main__':
    parser = DependencyParser()
    G = Generalization()
    a, parsed_sents=parser.get_SVOM(['she gave me a raise'])
    for i in range(len(a)):
        print("========================")
        print(parsed_sents[i])
        print(a[i])
        print(G.run(a)[i])
