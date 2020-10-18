from flask import Flask, render_template, request
import pickle
import numpy as np

app =  Flask(__name__)
filename = 'insurance_price.pkl'
regressor = pickle.load( open(filename,'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        region = request.form['region']
        if region == 'northeast':
            temp_array = temp_array + [1,0,0,0]
        elif region == 'northwest':
            temp_array = temp_array + [0,1,0,0]
        elif region == 'southeast':
            temp_array = temp_array + [0,0,1,0]
        elif region == 'southwest':
            temp_array = temp_array + [0,0,0,1]
        
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        gender = request.form['gender']
        if gender =='feamle':
            gender = 0
        else:
            gender = 1
        smoking = request.form['smoking']
        if smoking =='yes':
            smoking = 0
        else:
            smoking = 1
        
        temp_array =  temp_array + [age, bmi, children, gender, smoking] 
        
        data = np.array([temp_array])
        my_prediction= (regressor.predict(data)[0])
        my_prediction= int(regressor.predict(data)[0])
        
    return render_template('index.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5
                           ,prediction_text="Insurance Pice is {}".format(my_prediction))


   
if __name__=="__main__":
    app.run(debug=True, use_reloader=False)