import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl

data = pd.read_csv("Evasive-PDF-Samples.csv")

#Data-preprocessing

#Some columns are irrelevant in all of the 500k samples every OBS attribute has value 0

data = data.drop(columns=["OBS_JS","OBS_Javascript","OBS_Acroform","OBS_OpenAction"])

#There are no missing values

#For now, we think there is no columns that can be aggregated, all of the columns seem to be individually important for the overall statistics.
#But we could arrive at the conclusion that the columns for example obj and endobj are almost identical with a very small diference

#x_obj=data['obj']
#y_endobj=data['endobj']

#mpl.plot(y_endobj,x_obj)
#mpl.show()

#x_stream=data['stream']
#y_endstream=data['endstream']

#mpl.plot(x_stream,y_endstream)
#mpl.show()

#As the plots show, we cant aggregate this types of columns, their plots are not linear so there is no correlation between the two

#Sampling

#There is an inbalance in the number of malign and benign cases, so we will have to undersample the benign cases and oversample the malign cases

benign_cases = data.loc[data['class']==1] 
malign_cases = data.loc[data['class']==0]

#Undersampling to 250k cases
benign_cases = benign_cases.sample(n=250000,random_state=1)

#Oversampling to 250k cases
malign_cases = malign_cases.sample(n=250000,replace=True,random_state=1)

print(malign_cases)

sampled_data = pd.concat([benign_cases,malign_cases])

print(sampled_data)


#print(data)