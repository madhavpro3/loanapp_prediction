from flask import Flask, request, render_template
import pickle
import pandas as pd


loanapp=Flask(__name__)

# MODEL_PATH="outputs/loanapp_logreg.pkl"
# COLTRANSFORMER_PATH="outputs/loanapp_coltransformer.pkl"
# model=pickle.load(open(MODEL_PATH,"rb"))
# coltrans=pickle.load(open(COLTRANSFORMER_PATH,"rb"))

MODEL_PATH="model/loanapp_logreg.pkl"
COLTRANSFORMER_PATH="model/loanapp_coltransformer.pkl"
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

def model_predict(inp_dict):
    inp_processed=inp_process(inp_dict)
    return model.predict(inp_processed)

@loanapp.route("/")
def Home():
    # return "Hellow world"  
    return render_template("index.html")

@loanapp.route("/predict_creditworthiness",methods=['GET','POST'])
def predict_creditworthiness():
    # if request.method=='POST':

    loan_per_inc=float(request.form.get("loanamnt"))/float(request.form.get("income"))
                                                               
    inputs={"person_age":[float(request.form.get("age"))],"person_income":[float(request.form.get("income"))],
            "person_home_ownership":[request.form.get("homeownership")],"person_emp_length":[float(request.form.get("emplength"))],
            "loan_intent":[request.form.get("loanintent")],"loan_grade":[request.form.get("loangrade")],
            "loan_amnt":[float(request.form.get("loanamnt"))],"loan_int_rate":[float(request.form.get("intrate"))],
            "loan_percent_income":[loan_per_inc],"cb_person_default_on_file":[request.form.get("defaulthist")],
            "cb_person_cred_hist_length":[float(request.form.get("credhistory"))]}
    # st.write(pd.DataFrame.from_dict(inputs))
    pred=model_predict(pd.DataFrame.from_dict(inputs))
    pred_text="Your loan is approved!"
    if pred==0:
        pred_text="Sorry. Your loan application is rejected"

    return render_template("index.html", prediction_text = pred_text)
    

if __name__=="__main__":
    loanapp.run(host='0.0.0.0',port=5000,debug=False)
    # loanapp.run(, port=5000)