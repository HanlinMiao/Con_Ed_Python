import pandas as pd
import cplex
import random

#Indices

#return a list of regions
df = pd.read_csv('worker_boro_and_task.csv',index_col=False)
regions = df['Boro']
regions = regions.dropna()
regions = regions.unique()
current_regions = df['Boro']
current_regions = current_regions.dropna()
print(current_regions)




#return a list of workers in those regions
workers = df.iloc[:,0]
workers = workers.dropna()
workers = workers.unique()
print(workers)

worker_keys = {}
for i in range(2, len(workers)+1):
    worker_keys[i-1] = workers[i-1]
    
#return a list of maintenance type
main_type = ["PM","CM","FM"]

#return a list of task keys
tasks = list(df.columns)
tasks.remove(tasks[0])
tasks.remove(tasks[0])
tasks.remove(tasks[len(tasks)-1])
task_keys ={}
for i in range(1, len(tasks)):
    task_keys[i] = tasks[i-1]


#return a list of task skill level possible
skill = [1, 2, 3, 4, 5]

#Input Parameters

#labor hours per worker
labor_hours = 1600
#N_rm: task2 output
df1 = pd.read_csv('Task2_Output.csv')
#s_wtl: The skill level of worker w for task t
df = df.fillna(0)
S_wtl = {}
S_wtl["worker: task/skill_level"] = [1, 2, 3, 4, 5]
for i in range(1, len(worker_keys)+1):
    for task in tasks:
        S_wtl[worker_keys[i]+ ": "+task] = []
        for k in range(1, 6):
            if(df.loc[i, task] != "na")and (df.loc[i, task] != "nan") and int(df.loc[i, task])==k:
                S_wtl[worker_keys[i]+ ": "+task].append(1)
            else:
                S_wtl[worker_keys[i]+ ": "+task].append(0)
df2 = pd.DataFrame(S_wtl)
df2 = df2.T
df2.to_csv('s_wtl.csv', header = False)
#d_nr: The distance between two regions in miles
distance = {}
distance["n/r"] = list(regions)
for region1 in regions:
    count = 0
    distance[region1] = []
    for region2 in regions:
        if region1 == region2:
            distance[region1].append(0)
        else:
            distance[region1].append(random.randint(0, 5))
df3 = pd.DataFrame(distance)
df3 = df3.T
df3.to_csv('d_nr.csv', header = False)
#y_wn: If the worker w is not currently assigned to region n, then ywn= 1; otherwise  ywn = 0
y_wn = {}
y_wn['worker/region'] = list(regions)
for i in range(len(current_regions)):
    y_wn[workers[i]] = []
    for region in regions:
        if region != current_regions[i+1]:
            y_wn[workers[i]].append(1)
        else:
            y_wn[workers[i]].append(0)

df4 = pd.DataFrame(y_wn)
df4 = df4.T
df4.to_csv('y_wn.csv', header = False)
