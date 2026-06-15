import pandas as pd
import streamlit as st
import pypdf
from pypdf import PdfReader
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def rank_resume(job_description, resumes):
    doc = [job_description] + resumes
    vect = TfidfVectorizer().fit_transform(doc)
    vect= vect.toarray()
    
    jd_vector = vect[0].reshape(1, -1)
    res_vector = vect[1:]
    cos_sim = cosine_similarity(jd_vector, res_vector)
    return cos_sim


#STREAMLIT(FRONTEND)
st.title('RESUME RANKER')
st.header("Job Description")
job_description = st.text_area('Enter the job description')
st.header("Upload Resumes")
resumes = st.file_uploader('Upload resumes', type=['pdf'], accept_multiple_files=True)


if resumes and job_description:
    st.header('Ranking Resumes')
    
    res=[]
    for file in resumes:
        text = read_pdf(file)
        res.append(text)

    score= rank_resume(job_description, res)
    
    #display scores

    result= pd.DataFrame({"res":[file.name for file in resumes], "score":score[0]})
    result= result.sort_values(by='score', ascending=False)
    st.write(result)