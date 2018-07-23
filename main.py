from generalization import DependencyParser, Generalization
import json
import re

if __name__ == '__main__':
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
            for j in range(start,end):
                tmp.append(re.sub("\[|\]","",data['annotations'][j][0]['text']))
            #print(tmp)
            parsed_sents, aa = parser.get_SVOM(tmp)
            g_sents = G.run(parsed_sents)
            #print(aa)
            #print(g_sents)
            #if i == 50:exit()
            for j in range(start, end):
                data['annotations'][j][0]['event']=g_sents[j%batch_size]
        json.dump(data, open(f'/home/joe32140/event-visual-storytelling/data/event_clean_{file_path}.json', 'w'), indent=4)
