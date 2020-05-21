import konlpy
import nltk

# 크롤링한 데이터 받아오는 부분
import croll

# pos tag를 달기
sentence = str(croll.h2[0])
words = konlpy.tag.Twitter().pos(sentence)

# 형태소 정의, NP : 명사, VP : 동사, AP : 조사
grammar = """
NP: {<N.*>*<Suffix>?}   
VP: {<V.*>*}            
AP: {<A.*>*}            
"""

parser = nltk.RegexpParser(grammar)
chunks = parser.parse(words)

print(chunks.pprint())

# subtree 표시하는 부분
print("\n print none")
for subtree in chunks.subtrees():
    if subtree.label() == 'NP':
        print(' '.join((e[0] for e in list(subtree))))
        print(subtree.pprint())

