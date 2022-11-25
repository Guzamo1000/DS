from flask import Flask, render_template,request
import pandas as pd
from model.extrac_feature_data import extract,extract_song
from model.cosin import *


app=Flask(__name__)



data_song=pd.read_csv(r"D:\PTIT\data science\complete_project\data\list_song.csv")
feature_song=pd.read_csv(r"D:\PTIT\data science\complete_project\data\feature_song.csv")
@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
    return render_template("home.html")
@app.route("/recommend", methods=['GET','POST'])
def recommend():
    URL=request.form['URL']

    type_url=URL.split("/")
    if type_url[3]=='track':
        df=extract_song(URL)
    else:
    #using the extract function to get a features dataframe
        df = extract(URL)
    #retrieve the results and get as many recommendations as the user requested
    music_recomment = recommend_from_playlist(data_song, feature_song, df)
    # print(f"edm: {edm_top40['track_pop']}")
    # number_of_recs = int(request.form['number-of-recs'])
    number_of_recs=10
    my_songs = []
    print(f"number record {number_of_recs}")
    if music_recomment is None: 
        return render_template("results.html",songs=None)
    for i in range(number_of_recs):
        my_songs.append([str(music_recomment.iloc[i,2]) + ' - '+ '"'+str(music_recomment.iloc[i,0])+'"', "https://open.spotify.com/track/"+ str(music_recomment.iloc[i,1]).split("/")[-1]])
    return render_template('results.html',songs= my_songs)



if __name__=="__main__":
    app.run(debug=True)