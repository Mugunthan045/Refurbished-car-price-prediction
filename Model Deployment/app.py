from flask import Flask,render_template,request
import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)

@app.route('/',methods=['GET'])
def html():
    return render_template("index.html")

@app.route('/',methods=["GET","POST"])
def predict():
    Maker = request.form['Maker']
    model = request.form['model']
    Distance = request.form['Distance']
    Owner_Type = request.form['Owner Type']
    manufacture_year = request.form['manufacture_year']
    engine_displacement = request.form['engine_displacement']
    engine_power = request.form['engine_power']
    door_count = request.form['door_count']
    seat_count = request.form['seat_count']
    body_type = request.form['body_type']
    Vroom_Audit_Rating = request.form['Vroom Audit Rating']
    fuel_type = request.form['fuel_type']
    transmission = request.form['transmission']
    Location = request.form['Location']

    DF = pd.DataFrame(columns=['Distance ', 'Owner Type', 'manufacture_year', 'engine_displacement',
                                'engine_power', 'door_count', 'seat_count', 'Maker_bmw',
                                'Maker_fiat', 'Maker_hyundai', 'Maker_maserati', 'Maker_nissan',
                                'Maker_skoda', 'Maker_toyota', 'model_avensis', 'model_aygo',
                                'model_citigo', 'model_coupe', 'model_i30', 'model_juke', 'model_micra',
                                'model_octavia', 'model_panda', 'model_q3', 'model_q5', 'model_q7',
                                'model_qashqai', 'model_rapid', 'model_roomster', 'model_superb',
                                'model_tt', 'model_x1', 'model_x3', 'model_x5', 'model_yaris',
                                'model_yeti', 'body_type_van', 'Vroom Audit Rating_5',
                                'Vroom Audit Rating_6', 'Vroom Audit Rating_7', 'Vroom Audit Rating_8',
                                'fuel_type_petrol', 'Location_Bangalore', 'Location_Chennai',
                                'Location_Coimbatore', 'Location_Delhi', 'Location_Hyderabad',
                                'Location_Jaipur', 'Location_Kochi', 'Location_Kolkata',
                                'Location_Mumbai', 'Location_Pune', 'transmission_man'])

    
    
    
    DF.loc[0,'Distance '] = Distance
    DF.loc[0,'manufacture_year'] = manufacture_year
    DF.loc[0,'engine_displacement'] = engine_displacement
    DF.loc[0,'engine_power'] = engine_power
    DF.loc[0,'door_count'] = door_count
    DF.loc[0,'seat_count'] = seat_count
    
    
    MAKER = Maker
    Maker_arr  = ["bmw","hyundai","fiat","maserati","nissan","skoda","toyota"]
    for i in Maker_arr:
        if MAKER == i:
            DF.loc[0,"Maker_"+i] = 1
        else:
            DF.loc[0,"Maker_"+i] = 0


    MODEL = model
    model_arr = ["avensis","aygo","citigo","coupe","i30","juke","micra","octavia","panda","q3","q5","q7"
                ,"qashqai","rapid","roomster","superb","tt","x1","x3","x5","yaris","yeti"]
    for i in model_arr:
        if MODEL == i:
            DF.loc[0,"model_"+i] = 1
        else:
            DF.loc[0,"model_"+i] = 0
    
    VROOMAUDITRATNG = Vroom_Audit_Rating
    v_arr = ['5','6','7','8']
    for i in v_arr:
        if VROOMAUDITRATNG == i:
            DF.loc[0,"Vroom Audit Rating_"+i] = 1
        else:
            DF.loc[0,"Vroom Audit Rating_"+i] = 0
    
    LOCATION = Location 
    loc_arr  = ["Bangalore","Chennai","Delhi","Coimbatore","Delhi","Hyderabad","Jaipur","Kochi","Kolkata"
                ,"Mumbai","Pune"]
    for i in loc_arr:
        if LOCATION == i:
            DF.loc[0,"Location_"+i] = 1
        else:
            DF.loc[0,"Location_"+i] = 0
    
    FUELTYPE = fuel_type
    if FUELTYPE  == "petrol":
        DF.loc[0,"fuel_type_petrol"] = 1
    else:
        DF.loc[0,"fuel_type_petrol"] = 0
    
    
    TRANSMISSION = transmission
    if TRANSMISSION == "man":
        DF.loc[0,"transmission_man"] = 1
    else:
        DF.loc[0,"transmission_man"] = 0
    
    
    BODYTYPE = body_type
    if BODYTYPE == "van":
        DF.loc[0,"body_type_van"] = 1
    else:
        DF.loc[0,"body_type_van"] = 0
    
    
    OWNERTYPE = Owner_Type
    if OWNERTYPE=='First':
        DF.loc[0,'Owner Type']=1
    elif OWNERTYPE=='Second':
        DF.loc[0,'Owner Type']=2
    elif OWNERTYPE=='Third':
        DF.loc[0,'Owner Type']=3
    elif OWNERTYPE=='Fourth & Above':
        DF.loc[0,'Owner Type']=4

    DB = DF

    for i in DB:
        DB[i] = pd.to_numeric(DB[i])

    print(DB.dtypes)

    loaded_model = pickle.load(open('lgbm.pk1', 'rb'))  # Load the frozen model
    output=loaded_model.predict(DB)

    return render_template("index.html",prediction_text="Price = ₹{}".format(output[0]))
if __name__  == '__main__':
    app.run(port=3000,debug=True)