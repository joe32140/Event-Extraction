# Event-Extraction
Under development!

Implementation of "Event2Mind: Commonsense Inference on Events, Intents, and Reactions"
"""
Following Pichotta and Mooney (2016a), we developed a
4-tuple event representation hs, v, o, mi where v is a verb, s
is the subject of the verb, o is the object of the verb, and m is
the modifier or “wildcard”, which can be a propositional object,
indirect object, causal complement (e.g., in “I was glad
that he drove,” “drove” is the causal complement to “glad.”),
or any other dependency unclassifiable to Stanford’s dependency
parser.
"""
To generalize the content, the paper use Wordnet and Verbnet to replace the original word with higher level one. 
