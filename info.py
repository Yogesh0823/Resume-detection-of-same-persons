import resume_ext

# extracting text from pdf resume.
pdf_resume = "sample_resume/Alice Clark CV num-email update.pdf"
data = resume_ext.extract_text_from_pdf(pdf_resume)
text_data = ""
for i in data:
    text_data += i.lower()
# print(text_data)
print("Name :",resume_ext.extract_name(text_data))
print("Number :",resume_ext.extract_mobile_number(text_data))
print("Email :",resume_ext.extract_email(text_data))
print("Skills :",resume_ext.extract_skills(text_data))
print("Education :",resume_ext.extract_education(text_data)[0])

        

