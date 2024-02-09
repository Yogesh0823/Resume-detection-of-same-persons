from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import docx2txt
import spacy
from spacy.matcher import Matcher
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))
# print(STOPWORDS)
# exit()
# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
            'BSc', 'MSc', 'PhD', 'Bachelor', 'MASTER', 'Doctorate',
            'B.Sc', 'M.Sc', 'PhD', 'Bachelors', 'MASTERS', 'Doctorates',
            "Bachelor's", "Master's", "Doctorate","Institute"
        ]
EDUCATION = [i.upper() for i in EDUCATION]

# EDUCATION = ["BACHELOR", "MASTER", "DOCTORATE", "PHD"]
# STOPWORDS = ["A", "AN", "THE"]

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

def extract_text_from_doc(doc_path):
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)


nlp = spacy.load('en_core_web_lg')
matcher = Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', [pattern])  # Wrap the pattern in a list

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text    

def extract_mobile_number(text):
    # Updated regex to capture 10-digit phone numbers
    phone_numbers = re.findall(re.compile(r'\b(?:\+?\d{1,2}\s*)?(?:\(\s*\d{2,4}\s*\)|\d{2,4})\s*(?:[.-]\s*)?\d{3}\s*(?:[.-]\s*)?\d{4}\b'), text)
    
    # Extract only the numeric digits from each matched phone number
    return [''.join(filter(str.isdigit, number)) for number in phone_numbers]

def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
        
def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    # print("NLP SKIlls")
    # print(nlp_text)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    
    # reading the csv file
    data = pd.read_csv("skills.csv")
    
    # extract values
    skills = list(data.columns.values)
    
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # Access noun chunks from the processed nlp_text (Doc object)
    noun_chunks = [chunk.text.lower().strip() for chunk in nlp_text.noun_chunks]
    
    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        if token in skills:
            skillset.append(token)
    # print([i.capitalize() for i in set([i.lower() for i in skillset])])
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [str(sent).strip() for sent in nlp_text.sents]
    # print(nlp_text)

    edu = {}
    # Extract education degree and associated text
    for index, text in enumerate(nlp_text):
        # print(index)
        # print(text)
        # break
        # if "SKILLS" in text or "SKILLS" in text.upper():
        #     skl_edu = text.index("EDUCATION")
        #     skl_indx = text.index("SKILLS")
        for tex in text.split():
            # print(tex)
            # break
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            # print(tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                # skl = [i.upper() for i in extract_skills(text)]
                # Handle multi-word degrees
                degree_text = " ".join([text, nlp_text[index + 1]]) if index + 1 < len(nlp_text) else text
                # print(" ".join([text, nlp_text[index + 1]]) if index + 1 < len(nlp_text) else text)
                # print("test",tex)
                edu[tex] = degree_text
                
    # print("dict from outside loop",edu)

    # Extract year
    education = []
    for key, value in edu.items():
        year_match = re.search(r'(((20|19)(\d{2})))', value)
        if year_match:
            education.append((key, value, ''.join(year_match[0])))
        else:
            education.append((key, value))
    # print("Eduction",education)
    return education


# data = extract_text_from_pdf("test/Alice Clark CV ms.pdf")
# tx = ""
# for i in data:
#     tx += i.lower()
# print(extract_skills(tx))
# print(extract_education(tx))
# print(e)
# print(tx)
# print(extract_name(tx))