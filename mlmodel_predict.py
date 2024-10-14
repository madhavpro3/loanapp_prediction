from pickle import load
# from sklearn.ensemble import RandomForestClassifier

MODEL_PARAM_PATH='model/loanapp_rf_sm.pkl'
DATA_PIPELINE_PATH='model/loanapp_coltransformer_rf_sm.pkl'

loangrade_map={'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7}
persondefault_map={'N':0,'Y':1}
homeownership_map={'OTHER':0,'RENT':1,'MORTGAGE':2,'OWN':3}

def predict():
    # list has person_age,
    model = load(open(MODEL_PARAM_PATH, 'rb'))
    coltrans = load(open(DATA_PIPELINE_PATH, 'rb'))

    print("Hello world!")
    
    # df_test['loan_grade']=df_test['loan_grade'].replace(loangrade_map)
    # df_test['cb_person_default_on_file']=df_test['cb_person_default_on_file'].replace(persondefault_map)
    # df_test['person_home_ownership']=df_test['person_home_ownership'].replace(homeownership_map)
    # X_test=coltrans.transform(df_test)


# model.predict(X_test)
if __name__ == "__main__":
    predict()