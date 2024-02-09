import glob2
import PyPDF2
import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from resume_ext import extract_text_from_pdf, extract_name,extract_email,extract_mobile_number,extract_skills

fl = glob2.glob("data/*.pdf")
path = "paraphrase-MiniLM-L6-v2"
model = SentenceTransformer(path)

# def match_resume(*args):
#     res = []
#     for i in args:
#         pdf = PyPDF2.PdfReader(open(i,"rb"))
#         dt = pdf.pages[0].extract_text()
#         res.append(dt)
#     return res

resume_data = "sample_resume/Alice Clark CV.pdf","sample_resume/Alice Clark CV num-email update.pdf","sample_resume/Alice Clark CV email change.pdf","sample_resume/Alice Clark CV skills update.pdf","sample_resume/Smith Resume.pdf"
# print(len(resume_data))
resume_list = []
name = []
number = []
email = []
skills = []
for i in resume_data:
    # print(indx,i)
    # exit()
    tx = ""
    data = extract_text_from_pdf(i)
    for t in data:
        tx += t.lower()
    resume_list.append(tx)
    name.append(extract_name(tx))
    number.append(extract_mobile_number(tx))
    email.append(extract_email(tx))
    skills.append(extract_skills(tx))
# print(type(resume_list[0]))
num = []
for i in number:
    num.append(''.join(i))
# print(num)
# exit()
emb = model.encode(resume_list)
# sk_emd = model.encode(skills)
# sk_cos = cosine_similarity(sk_emd)
# print(sk_cos[0]*100)
# exit()
# print(emb)
# print(cosine_similarity(emb))
cos = cosine_similarity(emb,emb)
for indx,i in enumerate(cos[0]*100):
    print(indx,resume_data[indx],"Match Percentage :",round(i,2))
# print(cos[0]*100)
dt = cos[0]*100
# print(dt)
print(""*50+"*"*10+"pandas".upper()+"*"*10)
data = pd.DataFrame({"Path":resume_data,"Percentage":dt,"Name":name,"Number":num,"Email":email})
# print(data.dtypes)
# print(data["Percentage"] >= 85.00)
print(data.sort_values(by="Percentage",ascending=False))
# data.to_csv("resume-data.csv")
