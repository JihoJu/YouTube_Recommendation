import pandas as pd
import spacy
from tqdm import tqdm
import textacy

nlp = spacy.load("en_core_web_md")


def create_tokens(dataframe):
    tokens = []
    for doc in tqdm(nlp.pipe(dataframe.astype('unicode').values), total=dataframe.size):
        if doc.is_parsed:
            tokens.append([n.lemma_.lower() for n in doc if (not n.is_punct and not n.is_space and not n.is_stop)])
        else:
            tokens.append("")
    return tokens


raw = pd.read_csv("data.csv")
tokens = create_tokens(raw.loc[:, 'commit'])
print(tokens)

text = " ".join(raw.loc[:, 'commit'].tolist())
nlp.max_length = len(text)

keywords = []
for tokenlist in tqdm(tokens):
    doc = nlp(" ".join(tokenlist))
    extract = textacy.extract.keyterms.sgrank(doc, ngrams=(1), window_size=2, normalize=None, topn=2,
                                              include_pos=['NOUN', 'PROPN'])
    for a, b in extract:
        keywords.append(a)

res = sorted(set(keywords), key=lambda x: keywords.count(x), reverse=True)
with open("./keyword.txt", "w") as file:
    for r in res[:100]:
        file.write(r + '\n')