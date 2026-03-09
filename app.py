import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title='AI Resume Analyzer', layout='wide')
st.title('AI Resume Analyzer')
st.subheader('Upload your resume and check job match percentage')

AI_SKILLS = ['python', 'machine learning', 'deep learning', 'nlp', 'data science',
             'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
             'streamlit', 'flask', 'fastapi', 'sql', 'tableau', 'power bi',
             'computer vision', 'neural network', 'ai', 'artificial intelligence',
             'data analysis', 'matplotlib', 'seaborn', 'keras', 'opencv',
             'langchain', 'llm', 'rag', 'faiss', 'vector database']

JOB_ROLES = {
    'AI/ML Trainer': ['python', 'machine learning', 'ai', 'deep learning', 'nlp', 'teaching', 'training'],
    'Data Analyst': ['python', 'sql', 'pandas', 'tableau', 'power bi', 'data analysis', 'excel'],
    'ML Engineer': ['python', 'tensorflow', 'pytorch', 'scikit-learn', 'deep learning', 'neural network'],
    'Data Scientist': ['python', 'machine learning', 'statistics', 'pandas', 'numpy', 'data science']
}

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return ' '.join(text).lower()

def extract_skills(text):
    found = []
    for skill in AI_SKILLS:
        if skill.lower() in text:
            found.append(skill)
    return found

def match_job(skills, job_skills):
    matched = [s for s in job_skills if s in skills]
    if len(job_skills) == 0:
        return 0
    return int((len(matched) / len(job_skills)) * 100)

uploaded_file = st.file_uploader('Upload Resume PDF', type=['pdf'])

if uploaded_file:
    with st.spinner('Analyzing your resume...'):
        text = extract_text_from_pdf(uploaded_file)
        found_skills = extract_skills(text)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Skills Found in Resume')
        if found_skills:
            for skill in found_skills:
                st.success(skill.upper())
        else:
            st.warning('No AI skills found in resume')

    with col2:
        st.subheader('Job Role Match Percentage')
        for role, required_skills in JOB_ROLES.items():
            match = match_job(found_skills, required_skills)
            st.write(f'{role}')
            st.progress(match)
            st.write(f'{match}% match')
            st.write('---')

    st.subheader('Missing Skills to Improve')
    all_matched = set(found_skills)
    missing = [s for s in AI_SKILLS if s not in all_matched]
    if missing:
        cols = st.columns(3)
        for i, skill in enumerate(missing[:15]):
            cols[i % 3].error(skill.upper())

    st.subheader('Resume Analysis Summary')
    total_skills = len(AI_SKILLS)
    found_count = len(found_skills)
    score = int((found_count / total_skills) * 100)
    st.metric('Overall AI Skills Score', f'{score}%')
    st.metric('Skills Found', found_count)
    st.metric('Skills Missing', total_skills - found_count)

    if score >= 60:
        st.success('Strong AI Profile!')
    elif score >= 30:
        st.warning('Good profile - add more AI skills')
    else:
        st.error('Add more AI skills to your resume')
else:
    st.info('Please upload your resume PDF to start analysis')