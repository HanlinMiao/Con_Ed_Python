import pandas as pd
import operator
import xlwt
from xlwt import Workbook


#Input Files
Q_B = pd.read_csv("Input_files/S_and_Q_B.csv")
W_Bronx = pd.read_csv("Input_files/West_and_Bronx.csv")
Man = pd.read_csv("Input_files/Man.csv")
SI = pd.read_csv("Input_files/S_and_Q_B.csv")


#read boros for S_and_Q_B:
current_regions = Q_B['Boro']
current_regions = current_regions.dropna()

#Make a List of Regions:
super_regions = ["S", "Q/B", "W/Br","M"]
#extract a task list
tasks = list(Q_B.columns)
tasks.remove(tasks[0])
tasks.remove(tasks[0])
tasks.remove(tasks[len(tasks)-1])
task_keys ={}
for i in range(1, len(tasks)+1):
    task_keys[i] = tasks[i-1]

key_list = list(task_keys.keys())
value_list = list(task_keys.values())
#extract a worker list for Q/B
workers = Q_B.iloc[:,0]
workers = workers.dropna()
workers = workers.unique()
worker_keys = {}
for i in range(1, len(workers)+1):
    worker_keys[i] = workers[i-1]

workers_Q_B = []
workers_S = []
#separate workers from Q/B from S
for i in range(1, len(current_regions)+1):
    if(current_regions[i] != "S"):
        workers_Q_B.append(workers[i-1])
    else:
        workers_S.append(workers[i-1])
#extract a worker list for W/Br
workers_W_Br = W_Bronx.iloc[:,0]
workers_W_Br = workers_W_Br.dropna()
workers_W_Br = workers_W_Br.unique()
workers_W_Br = list(workers_W_Br)
#extract a worker list for M
workers_M = Man.iloc[:,0]
workers_M = workers_M.dropna()
workers_M = workers_M.unique()
workers_M = list(workers_M)
#dict[region][task][list of skills level]
Q_B.fillna(0)
W_Bronx.fillna(0)
Man.fillna(0)
SI.fillna(0)
myKeyList = {}
for i in range(len(super_regions)):
    myKeyList[super_regions[i]] = {}
    for k in range(1, len(key_list)+1):
        myKeyList[super_regions[i]][k] = []
        if(super_regions[i] == "S"):
            for j in range(1, len(worker_keys)):
                if worker_keys[j] in workers_S:
                    myKeyList[super_regions[i]][k].append(Q_B.loc[j+1, value_list[k-1]])
        elif(super_regions[i] == "Q/B"):
            for j in range(1, len(worker_keys)):
                if worker_keys[j] in workers_Q_B:
                    myKeyList[super_regions[i]][k].append(Q_B.loc[j+1, value_list[k-1]])
        elif(super_regions[i] == "W/Br"):
            for j in range(len(workers_W_Br)):
                myKeyList[super_regions[i]][k].append(W_Bronx.loc[j+1, value_list[k-1]])
        elif(super_regions[i] == "M"):
            for j in range(len(workers_M)):
                myKeyList[super_regions[i]][k].append(Man.loc[j+1, value_list[k-1]])
data = pd.DataFrame.from_dict(myKeyList)
data.to_csv('Evaluation.csv')


output_5 = {}
for i in range(len(super_regions)):
    output_5[super_regions[i]] = {}
    for k in range(1, len(key_list)+1):
        output_5[super_regions[i]][k] = {}
        count5 = 0
        for j in range(len(myKeyList[super_regions[i]][k])):
            try:
                if(int(myKeyList[super_regions[i]][k][j])== 5):
                    count5 += 1
            except ValueError:
                myKeyList[super_regions[i]][k][j] = 0
        output_5[super_regions[i]][k] = round(count5/len(myKeyList[super_regions[i]][k])*100, 2)
    output_5[super_regions[i]] = dict(sorted(output_5[super_regions[i]].items(), key = operator.itemgetter(1)))

output_3plus = {}
for i in range(len(super_regions)):
    output_3plus[super_regions[i]] = {}
    for k in range(1, len(key_list)+1):
        output_3plus[super_regions[i]][k] = {}
        count3 = 0
        for j in range(len(myKeyList[super_regions[i]][k])):
            try:
                if(int(myKeyList[super_regions[i]][k][j])>= 3):
                    count3 += 1
            except ValueError:
                myKeyList[super_regions[i]][k][j] = 0
        output_3plus[super_regions[i]][k] = round(count3/len(myKeyList[super_regions[i]][k])*100, 2)
    output_3plus[super_regions[i]] = dict(sorted(output_3plus[super_regions[i]].items(), key = operator.itemgetter(1)))


output = {}
for i in range(len(super_regions)):
    output[super_regions[i]] = {}
    for k in range(1, len(key_list)+1):
        output[super_regions[i]][k] =100*output_3plus[super_regions[i]][k]+output_5[super_regions[i]][k]
    output[super_regions[i]] = dict(sorted(output[super_regions[i]].items(), key = operator.itemgetter(1)))
#work fulfillment percentage
data = pd.read_csv("Input_files/Task2_Output.csv")
work_percent = {}
for region in super_regions:
    if region == "S":
        work_percent[region] = 1600*len(workers_S)/int(data[region])
    elif region == "Q/B":
        work_percent[region] = 1600*len(workers_Q_B)/int(data[region])
    elif region == "W/Br":
        work_percent[region] = 1600*len(workers_W_Br)/int(data[region])
    else:
        work_percent[region] = 1600*len(workers_M)/int(data[region])

        
workbook = Workbook()
worksheet = workbook.add_sheet('Evaluation')
count = 0
row = 2
col = 0
st = xlwt.easyxf('pattern: pattern solid;align: horiz center')
st.pattern.pattern_fore_colour = 15
index = xlwt.easyxf('pattern: pattern solid;')
index.pattern.pattern_fore_colour = 45

for i in range(len(super_regions)):
    worksheet.write_merge(0,0,1*count, 1*count+2, super_regions[i] + " work fulfilled: "+ "{:.2f}".format(work_percent[super_regions[i]]*100) + " %", st)
    count += 3
    key_list = list(output[super_regions[i]].keys())
    
    worksheet.write(1, col, "Skill Index")
    col+=1
    worksheet.write(1, col, "Percentage of 3 plus's")
    col+=1
    worksheet.write(1, col, "Percentage of 5's")
    col-=2
    for num in key_list:
        worksheet.write(row, col, num)
        col+=1
        worksheet.write(row, col, "{:.2f}".format(output_3plus[super_regions[i]][num])+ " %")
        col+=1
        worksheet.write(row, col, "{:.2f}".format(output_5[super_regions[i]][num])+ " %")
        row+=1
        col-=2
    row = 2
    col = (i+1)*3

workbook.save('Output_files/evaluation.xls')

print("see evaluation result at Output_files/evaluation.xls")

