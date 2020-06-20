from flask import Flask, render_template, request, url_for 
import os
import pandas as pd
import numpy as np
import csv
import random
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from matplotlib import style
style.use('ggplot')
import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab
sns.set_color_codes()
sns.set_style("white")
import time

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
@app.route('/bscstart',methods=['POST', 'GET'])
def bscstart():
	return render_template('bscstart.html') 

@app.route('/bscsubmit',methods=['POST', 'GET'])
def bscsubmit():
	print('rnd', rnd)
	model_pred = dfvisual.iloc[rnd,-2]
	actual_shooter = dfvisual.iloc[rnd,-1]
	user_choice = request.form.get("shooter")
	if user_choice == 'null':
		user_choice = random.choice(['Danny Green','Tim Duncan','LaMarcus Aldridge','Tony Parker','Kawhi Leonard'])

	user_score=0
	model_score=0

	if user_choice == actual_shooter:
		user_score += 1
	if model_pred == actual_shooter:
		model_score += 1

	if user_score == 0:
		answer_display = 'Incorrect Answer!'
	else:
		answer_display = 'Correct Answer!'

	time.sleep(1.5)
	return render_template('bscsubmit.html',
		answer_selection = answer_display,
		model_selection = model_pred,
		user_selection=user_choice,
		shooter = actual_shooter)

@app.route('/bsc',methods=['POST', 'GET'])
def bsc():
	global rnd, dfvisual
	# read datafile
	filename = 'static/bsc_data/df_w_predicted.csv'
	data = pd.read_csv(filename) 

	if True:
		# pre-processing
		pred = data[['Predicted']] # get predictions, i.e. name of player who shot the ball)
		whoshot = data[['PLAYER1_NAME']]
		data = data.iloc[:,37:] # get the x,y coordinates
		df = pd.concat([data,pred,whoshot],axis=1) # merge datasets

		# select 5 players
		newcol_lst = []
		for item in df.columns[:-2]:
		    player = item.split(',')[2][2:][:-2] # getting player names from columns
		    if (player=="Danny Green"):
		        pass
		    elif player=="Kawhi Leonard":
		        pass
		    elif player=="LaMarcus Aldridge":
		        pass
		    elif player=="Tim Duncan":
		        pass
		    elif player=="Tony Parker":
		        pass
		    else:
		        newcol_lst.append(item)
		df.drop(newcol_lst, axis=1,inplace=True)
		df.dropna(axis=0,how='any',subset=df.columns[:-2],inplace=True)
		dfvisual = df # rename variable

	def PlotGen(rnd):
    
	    # rnd is the indexed play, randomly generated
	    
	    '''We will do this for Danny Green first'''
	    DGlstx = [] # create an empty list where we store the columns for x values for each player
	    DGlsty = [] # create an empty list where we store the columns for y values for each player
	    DGlstname = [] # create an empty list where we store the player's name

	    # we store the number of the columns for x values in our dataframe into the list DGlstx
	    i=0 # 
	    count = 0
	    while count < 30:
	        DGlstx.append(i)
	        i += 5 # we find the next value after 4 other players, hence the +5 increment
	        count += 1

	    # we store the number of the columns for x values in our dataframe into the list DGlsty
	    i = 150 # this number will change depending on the player
	    count = 0
	    while count < 30:
	        DGlsty.append(i)
	        i += 5 # we find the next value after 4 other players, hence the +5 increment
	        count += 1

	    # add name of player to each item of the list DGlstname
	    count = 0
	    while count < 30:
	        DGlstname.append("Danny Green")
	        count += 1

	    DGlstxv = []  # create an empty df where we store the x values
	    DGlstyv = [] # create an empty df where we store the y values

	    # we select the x coordinate entires using iloc
	    for i in DGlstx:
	        DGlstxv.append(dfvisual.iloc[rnd,i]) #rnd is the row/index number, i is the column number

	    # we select the y coordinate entires using iloc
	    for i in DGlsty:
	        DGlstyv.append(dfvisual.iloc[rnd,i]) #rnd is the row/index number, i is the column number

	    dfDG = pd.DataFrame([DGlstname, DGlstxv, DGlstyv]).T # we transpose our dataframe

	    '''We will do this now for the rest of the players'''
	    '''Tim Duncan'''
	    TDlstx = []
	    TDlsty = []
	    TDlstname = []

	    i=3
	    count = 0
	    while count < 30:
	        TDlstx.append(i)
	        i += 5
	        count += 1

	    i = 153
	    count = 0
	    while count < 30:
	        TDlsty.append(i)
	        i += 5
	        count += 1

	    count = 0
	    while count < 30:
	        TDlstname.append("Tim Duncan")
	        count += 1

	    TDlstxv = []
	    TDlstyv = []

	    for i in TDlstx:
	        TDlstxv.append(dfvisual.iloc[rnd,i])

	    for i in TDlsty:
	        TDlstyv.append(dfvisual.iloc[rnd,i])

	    dfTD = pd.DataFrame([TDlstname, TDlstxv, TDlstyv]).T

	    '''Kawhi Leonard'''
	    KLlstx = []
	    KLlsty = []
	    KLlstname = []

	    i=1
	    count = 0
	    while count < 30:
	        KLlstx.append(i)
	        i += 5
	        count += 1

	    i = 151
	    count = 0
	    while count < 30:
	        KLlsty.append(i)
	        i += 5
	        count += 1

	    count = 0
	    while count < 30:
	        KLlstname.append("Kawhi Leonard")
	        count += 1

	    KLlstxv = []
	    KLlstyv = []

	    for i in KLlstx:
	        KLlstxv.append(dfvisual.iloc[rnd,i])

	    for i in KLlsty:
	        KLlstyv.append(dfvisual.iloc[rnd,i])

	    dfKL = pd.DataFrame([KLlstname, KLlstxv, KLlstyv]).T

	    '''LaMarcus Aldridge'''
	    LAlstx = []
	    LAlsty = []
	    LAlstname = []

	    i=2
	    count = 0
	    while count < 30:
	        LAlstx.append(i)
	        i += 5
	        count += 1

	    i = 152
	    count = 0
	    while count < 30:
	        LAlsty.append(i)
	        i += 5
	        count += 1

	    count = 0
	    while count < 30:
	        LAlstname.append("LaMarcus Aldridge")
	        count += 1

	    LAlstxv = []
	    LAlstyv = []

	    for i in LAlstx:
	        LAlstxv.append(dfvisual.iloc[rnd,i])

	    for i in LAlsty:
	        LAlstyv.append(dfvisual.iloc[rnd,i])

	    dfLA = pd.DataFrame([LAlstname, LAlstxv, LAlstyv]).T

	    '''Tony Parker'''
	    TPlstx = []
	    TPlsty = []
	    TPlstname = []

	    i=4
	    count = 0
	    while count < 30:
	        TPlstx.append(i)
	        i += 5
	        count += 1

	    i = 154
	    count = 0
	    while count < 30:
	        TPlsty.append(i)
	        i += 5
	        count += 1

	    count = 0
	    while count < 30:
	        TPlstname.append("Tony Parker")
	        count += 1

	    TPlstxv = []
	    TPlstyv = []

	    for i in TPlstx:
	        TPlstxv.append(dfvisual.iloc[rnd,i])

	    for i in TPlsty:
	        TPlstyv.append(dfvisual.iloc[rnd,i])

	    dfTP = pd.DataFrame([TPlstname, TPlstxv, TPlstyv]).T
	    
	    '''Create visual'''
	    df_plt = pd.concat([dfDG, dfTD, dfKL,dfLA,dfTP], axis=1)
	    filename_p2 = 'static/bsc_data/df4plot2.csv'
	    df_plt.to_csv(filename_p2)

	    # taking x,y values
	    DGx,DGy, TDx, TDy, KLx, KLy, LAx, LAy,TPx,TPy=np.loadtxt(filename_p2,unpack=True,                
	                                                             delimiter=',',
	                                                             usecols=(2,3,5,6,8,9,11,12,14,15))
	    DGx,DGy, TDx, TDy, KLx, KLy, LAx, LAy,TPx,TPy = DGx[1:],DGy[1:], TDx[1:], TDy[1:], KLx[1:], KLy[1:], LAx[1:], LAy[1:],TPx[1:],TPy[1:] 

	    imagesource = 'static/bsc_data/fullcourt.png'

	    court=plt.imread(imagesource) 
	    plt.figure(figsize=(15,11.5))

	    plt.imshow(court, zorder=0, extent=[0,94,50,0])
	    plt.xlim(0,94)

	    t=np.arange(30)

	    DG = plt.scatter(DGx,DGy,c=t,cmap='Reds',s=500,zorder=1)
	    TD = plt.scatter(TDx,TDy, c=t,cmap='Blues',s=500,zorder=1)
	    KL = plt.scatter(KLx,KLy, c=t,cmap='Greens',s=500,zorder=1)
	    LA = plt.scatter(LAx,LAy, c=t,cmap='Wistia',s=500,zorder=1)
	    TP = plt.scatter(TPx,TPy, c=t,cmap='Purples',s=500,zorder=1)
 
	    plt.show()
	    pylab.savefig('static/bsc_plots/bsc_play.png',bbox_inches='tight')
	
	rnd = random.randint(0,len(df.index)-1) # random play generator
	print('RAND: ',rnd)
	PlotGen(rnd)

	return render_template('bsc.html') 

#Caching
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
	# app.run(host='0.0.0.0.80', port=80)
	app.run(host='0.0.0.0',port=80,debug=True)
