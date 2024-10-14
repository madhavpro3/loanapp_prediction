import streamlit as st
import pickle
import pandas as pd

# inputs needed
#  age, income, emp_length,loan_amount, <loan_percent_income>,
# cred_hist_length, loan_int_rate,home ownership,loan grade,<default on file>,loan_intent

age = st.number_input("Person's age",min_value=1,max_value=80,step=1,key='age')
income = st.number_input("Person's monthly income",min_value=10000,step=10000,key='income')
homeownership = st.selectbox("Home ownership",("OWN","RENT","MORTGAGE","OTHER"),key='home')
emplength=st.number_input("Person's employment length",min_value=0,step=1,key='emplength')
credithist=st.number_input("Person's credit history years",min_value=0,step=1,key='credhist')

intrate = st.number_input("Loan interest rate",min_value=0.1,step=0.01,key='loanint')
loanamnt = st.number_input("Loan amount needed",min_value=10000,step=10000,key='loanamnt')
loangrade=st.selectbox("Loan grade",("A","B","C","D","E","F","G"),key='loangrade')
defaulthist=st.selectbox("Is there any history of defaulting?",("Y","N"),key='loandefault')
loanintent=st.selectbox("Loan purpose",("DEDTCONSOLIDATION","HOMEIMPROVEMENT","EDUCATION","MEDICAL","PERSONAL","VENTURE"),key='loanpurpose')

MODEL_PATH="outputs/loanapp_logreg.pkl"
COLTRANSFORMER_PATH="outputs/loanapp_coltransformer.pkl"
model=pickle.load(open(MODEL_PATH,"rb"))
coltrans=pickle.load(open(COLTRANSFORMER_PATH,"rb"))

def inp_process(inp_pd):

    loangrade_map={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7}
    persondefault_map={'N':0,'Y':1}
    homeownership_map={'OTHER':0,'RENT':1,'MORTGAGE':2,'OWN':3}

    # inp_pd=pd.DataFrame(inp_dict)
    inp_pd['loan_grade']=inp_pd['loan_grade'].replace(loangrade_map)
    inp_pd['cb_person_default_on_file']=inp_pd['cb_person_default_on_file'].replace(persondefault_map)
    inp_pd['person_home_ownership']=inp_pd['person_home_ownership'].replace(homeownership_map)
    inp_processed=coltrans.transform(inp_pd)

    return inp_processed


def predict_credworthiness(inp_dict):
    inp_processed=inp_process(inp_dict)
    return model.predict(inp_processed)


if st.button("Check credit worthiness"):
    loan_per_inc=st.session_state.loanamnt/st.session_state.income
    inputs={"person_age":[st.session_state.age],"person_income":[st.session_state.income],
            "person_home_ownership":[st.session_state.home],"person_emp_length":[st.session_state.emplength],
            "loan_intent":[st.session_state.loanpurpose],"loan_grade":[st.session_state.loangrade],
            "loan_amnt":[st.session_state.loanamnt],"loan_int_rate":[st.session_state.loanint],
            "loan_percent_income":[loan_per_inc],"cb_person_default_on_file":[st.session_state.loandefault],
            "cb_person_cred_hist_length":[st.session_state.credhist]}
    # st.write(pd.DataFrame.from_dict(inputs))
    pred=predict_credworthiness(pd.DataFrame.from_dict(inputs))
    if pred:
        st.write("Loan approved!")
    else:
        st.write("Loan application is rejected")