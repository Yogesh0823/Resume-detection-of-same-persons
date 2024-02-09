## Table of Contents
1. [General Info](#Resume-detection-of-same-persons)
2. [Installation](#Installation)

# Resume-detection-of-same-persons using NLP 
***
* ## NLP PROJECT
1. This is machine learning project for detect the person's same resume from list of resume or from folder's by comparing first in giving list to itself and other in list.
2. Using sentence transformers and embdedding the sentence or word of vector after extracting resune text from pdf & doc many information extract and save in .csv file using pandas dataframe work.
3. You can get 100% perfect result and percentage if the resume belongs to the same person's and also get resume matching percentage and name number email eduaction skills.
***
# Installation
## clone this repo to your folder.
* open terminal.
  
      $ git clone https://github.com/Yogesh0823/Resume-detection-of-same-persons.git
      $ cd Resume-detection-of-same-persons
  
## create virtule environment 
* open terminal in Resume-detection-of-same-persons folder.
  
      $ python -m venv env_name 
* active virtule environment
  
      $ source/env_name/bin/activate
* install requirement.txt
  
      $ pip install -r requirement.txt

## Run Resume_match.py file
     $ python resume_match.py
2. you can change list of resume to your own resume path from resume_match.py file.
3. feel free to contact and ask any query related to the project yogeshsundesha55@gmail.com

## Result output in pandas dataframe
* using pandas dataframe
* First in list always compared by itself and other in list & then it will give how much percentage match the resume in list.
![result](https://github.com/Yogesh0823/Resume-detection-of-same-persons/blob/main/results.png)
* For saving your output in .csv file uncomment the last line of code in from resume_match.py file.
* Now you can sort the data and more using pandas function.

# For extracting resume info like name , number, email, skills, education.
#### using file resume_ext.py you can extract info.
* import extraction fuction in .py file.
* run file info.py
  
      $ python info.py
  
  * all extraction function are define in info.py file.
  * for pdf and docs both file are accept.
  * for pdf use extract_text_from_pdf("your pdf file path") and for docs use extract_text_from_doc("your doc file path")
![result](https://github.com/Yogesh0823/Resume-detection-of-same-persons/blob/main/sample_resume/info_ext.png)
