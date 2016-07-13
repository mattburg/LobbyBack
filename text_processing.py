
import elasticsearch
import re
import string
import urllib2
from pprint import pprint
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

#custom modules
#from database import ElasticConnection

def clean_text(text, lower = True):
    '''
    variables:
        text: string corresponding to text of bill
        bill_name: string corresponding to bill_id

    returns:
        string that is cleaned up text 
    decription:
        clean text 
    '''
    #make text lowercase
    if lower == True:
        text = text.lower()
    
    #parse by line
    text_list =  text.splitlines()
    #replace funky symbols and multipe new lines
    ntext_list = []
    for line in text_list:
        line = line.replace(u'\xa0', u' ')
        line = line.replace(u'>>', u' ')
        line = line.replace(u'\xa7', u' ')
        line = line.replace(u'\xe2', u' ')
        line = line.replace(u'\u201c', u' ')
        line = line.replace(u'\u201d', u' ')
        line = line.replace(u'\xbb', u' ')
        line = line.replace(u'\xa9', u' ')
        line = line.replace(u'{ font-family: courier, arial, sans-serif; font-size: 10pt; } table { empty-cells:show; }', u' ')
        line = re.sub( '\s+', ' ', line)
        if len(line) >= 1:
            ntext_list.append(line)
    
    clean_string = "\n".join(ntext_list)
    clean_string = re.sub("(\n |\n)+","\n",clean_string)
    
    clean_string = re.sub('\\n\s[0-9][0-9]|\\n[0-9][0-9]|\\n[0-9]|\\n\s[0-9]','',clean_string)
    
    return clean_string
 
def bill_sent_chunk_tokenize(bill_text,min_sentence_length = 20):
    
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc','1','2','3','4','5','6','7','8','9'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    
    bill_sentences = sentence_splitter.tokenize(bill_text)
    
    bill_sentences = [s for s in bill_sentences if len(s) > min_sentence_length]
    
    return bill_sentences

def extract_bill_document_sentences(bill_docs,min_sentence_length = 20):
    """
        Args: 
            
            bill_docs: list of bill_doc dictionary objects

            min_sentence_length: the minumum length of a sentence for it
                                 to be included in the set of returned sentences

        
        Returns:

            sentences: list of tuples that contain (sentence_text,bill_name)

    """
    
    sentences = []
    
    for doc in bill_docs:
        
        bill_text = doc['bill_text']
                
        for s in bill_sent_chunk_tokenize(bill_text,min_sentence_length):
            
            s = clean_text(s,lower = False)
            sentences.append( (s,doc['name']) )
    
    return sentences




def main():
    import pickle
    G_ego = pickle.load(open("/Users/mattburg/Desktop/www.alec.org_355.p"))
    
    bill_docs = [v for v in G_ego[1].vs if v['type'] == "state_bill"]
    bill_docs = [{"bill_text":x['bill_text'],"name":x['name'],"bill_date":x['bill_date']} for x in bill_docs]
    
    print extract_bill_document_sentences(bill_docs)

    
    

if __name__ == "__main__":
    main()

