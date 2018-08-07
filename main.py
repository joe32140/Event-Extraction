from generalization import DependencyParser, Generalization, NERparser
import json
import re
from random import randrange

def Dependency_Parsing():
    parser = DependencyParser()
    G = Generalization()
    files = ['train', 'val', 'test']
    for file_path in files:
        print(f"===={file_path}====")
        data = json.load(open(f'/home/bendan0617/Visual-Storytelling/data/sis/partial_parsed_clean_{file_path}.json'))
        batch_size=500

        n_batch = len(data['annotations'])//batch_size
        #n_batch=40
        for i in range(n_batch+1):
            print(f"Batch {i}===============================")

            start = i*batch_size
            end = (i+1)*batch_size if (i+1)*batch_size<len(data['annotations']) else len(data['annotations'])
            tmp=[]
            random_index = randrange(0,(end-start))
            for j in range(start,end):
                tmp.append(re.sub("\[|\]","",data['annotations'][j][0]['text']))
            print("tmp:", tmp[random_index])
            for sentence in tmp:
                for i, word in enumerate(sentence):
                    if word == "'s":
                        sentence[i] = "is"
            parsed_sents, aa = parser.get_SVOM(tmp)
            g_sents = G.run(parsed_sents)
            print("parsed_sents:",parsed_sents[random_index])
            print("aa:",aa[random_index])
            print("g_sents:", g_sents[random_index])
            print(len(tmp),len(parsed_sents),len(aa), len(g_sents))
            #if i == 50:exit()
            for j in range(start, end):
                data['annotations'][j][0]['event']=g_sents[j%batch_size]
        json.dump(data, open(f'/home/cloud60138/Event-Extraction/data/event_clean_{file_path}.json', 'w'), indent=4)

def NER():
    ner_parser = NERparser()
    data = json.load(open(f'/home/joe32140/event-visual-storytelling/data/ROC.json'))
    batch_size=100

    n_batch = len(data)//batch_size
    #n_batch=40
    for i in range(n_batch+1):
        print(f"Batch {i}===============================")

        start = i*batch_size
        end = (i+1)*batch_size if (i+1)*batch_size<len(data) else len(data)
        tmp=[]
        for j in range(start,end):
            tmp.extend([ clear_string(sent) for sent in data[j]['storys'] ])
        parsed_sents = ner_parser.replace(tmp)
        if i == 50:exit()
        for k, j in enumerate(range(start, end)):
            data[j]['story_ner']=parsed_sents[k*5:(k+1)*5]
    json.dump(data, open(f'/home/joe32140/event-visual-storytelling/data/ROC_ner.json', 'w'), indent=4)

def clear_string(x):
    x = re.sub("\[|\]","", x)
    x = re.sub("'s"," is", x)
    return x

if __name__ == '__main__':
    NER()
    #Dependency_Parsing()
