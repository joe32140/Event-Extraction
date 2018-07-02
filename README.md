# Event-Extraction
Under development!

Implementation of event extraction in ["Event2Mind: Commonsense Inference on Events, Intents, and Reactions"](https://arxiv.org/pdf/1706.01331.pdf)
```
Following Pichotta and Mooney (2016a), we developed a
4-tuple event representation (s, v, o, m) where v is a verb, s
is the subject of the verb, o is the object of the verb, and m is
the modifier or “wildcard”, which can be a propositional object,
indirect object, causal complement (e.g., in “I was glad
that he drove,” “drove” is the causal complement to “glad.”),
or any other dependency unclassifiable to Stanford’s dependency
parser.
```
To generalize the content, the author uses Wordnet and Verbnet to replace the original word with higher level one. 

Requirements
=========
- nltk: wordnet, verbnet
- stanford core nlp jar files

To Do List
=========
- [x] Replcing Named Entities
- [x] Genra Clustering
