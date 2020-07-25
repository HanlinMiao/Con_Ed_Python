import pandas as pd
import openpyxl
import cplex
import random
import operator
import xlwt
from xlwt import Workbook

#Indices
weight1 = 100
weight2 = 1000
weight3 = 100

#return a list of regions
df = pd.read_csv('worker_boro_and_task.csv',index_col=False)
regions = df['Boro']
regions = regions.dropna()
regions = regions.unique()
current_regions = df['Boro']
current_regions = current_regions.dropna()


#return a list of workers in those regions
workers = df.iloc[:,0]
workers = workers.dropna()
workers = workers.unique()
worker_keys = {}
for i in range(1, len(workers)+1):
    worker_keys[i] = workers[i-1]
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
N = df1.to_dict()
N_rm = {}
for region in regions:
    N_rm[region] = {}
    for i in range(len(main_type)):
        N_rm[region][main_type[i]] = N[region][i]

#s_wtl: The skill level of worker w for task t
df = df.fillna(0)
S_wtl = {}
S_wtl["worker: task/skill_level"] = [1, 2, 3, 4, 5]
for i in range(1, len(worker_keys)+1):
    S_wtl[worker_keys[i]] = {}
    for task in tasks:
        S_wtl[worker_keys[i]][task] = []
        for k in range(1, 6):
            if(df.loc[i, task] != "na")and (df.loc[i, task] != "nan") and int(df.loc[i, task])==k:
                S_wtl[worker_keys[i]][task].append(1)
            else:
                S_wtl[worker_keys[i]][task].append(0)


#d_nr: The distance between two regions in miles
distance = {}
distance["n/r"] = list(regions)
for region1 in regions:
    count = 0
    distance[region1] = {}
    for region2 in regions:
        if region1 == region2:
            distance[region1][region2] = 0
        else:
            distance[region1][region2]= random.randint(1, 5)

#y_wn: If the worker w is not currently assigned to region n, then ywn= 1; otherwise  ywn = 0
y_wn = {}
y_wn['worker/region'] = list(regions)
for i in range(len(current_regions)):
    y_wn[workers[i]] = {}
    for region in regions:
        if region != current_regions[i+1]:
            y_wn[workers[i]][region]=1
        else:
            y_wn[workers[i]][region]=0



#Linear Programming Part
my_var_type = ""
my_cons_type = ""
my_ub = []
my_lb = []
my_obj = []
my_cons_L = []
my_cons_R = []

#generating var type, upper bound, lower bound, objective
#x_rw for 52 workers and 4 regions, binary 0, 1
for region in regions:
    for worker in workers:
        my_var_type += "B"
        my_ub.append(1)
        my_lb.append(0)
        my_obj.append(0)
                         
                         
#Phi minimum percentage continuous between 0, 1
my_var_type += "C"
my_ub.append(1)
my_lb.append(0)
my_obj.append(-weight1)


#theta for 57 tasks and 5 skill indices, integer
for level in skill:
    for task in tasks:
        my_var_type += "I"
        my_ub.append(5)
        my_lb.append(0)
        my_obj.append(weight2/(len(tasks)*len(skill)))
        
#z_wnr for 52 workers and 4 regions, binary 0, 1
for region1 in regions:
    for region2 in regions:
        for worker in workers:
            my_var_type += "B"
            my_ub.append(1)
            my_lb.append(0)
            my_obj.append(weight3*distance[region1][region2])

#generating constraint Left hand side and right hand side

#xwr=1
d_var_index = 0
constraint_count = 0
for i in range(len(workers)):
    d_var_index = i 
    my_cons_L.append([[],[]])
    my_cons_R.append(1)
    my_cons_type += "E"
    for j in range(len(regions)):
        d_var_index = i + j*(len(workers))
        my_cons_L[constraint_count][0].append(d_var_index)
        my_cons_L[constraint_count][1].append(1)
    constraint_count +=1

#1600wxrw /mNrm ≥ φ
d_var_index = 0
for region in regions:
    work_hour = 0
    work_hour += N_rm[region]["PM"]+N_rm[region]["CM"]+N_rm[region]["FM"]
    my_cons_L.append([[],[]])
    my_cons_R.append(0)
    my_cons_type += "L"
    for worker in workers:
        my_cons_L[constraint_count][0].append(d_var_index)
        my_cons_L[constraint_count][1].append(-1600/work_hour)
        d_var_index = d_var_index+1
    my_cons_L[constraint_count][0].append(208)
    my_cons_L[constraint_count][1].append(1)
    constraint_count +=1

# wxwr1swtl - wxwr2swtl ≤ Θ_tl
d_var_index = 209
for task in tasks:
    for i in range(5):
        for r1 in range(len(regions)):
            r2 = 0
            while(r2<len(regions)):
                if r2==r1:
                    r2+=1
                else:
                    my_cons_L.append([[],[]])
                    my_cons_R.append(0)
                    my_cons_type += "L"
                    x_wr2_index = len(workers)*r2
                    x_wr1_index = len(workers)*r1
                    for worker in workers:
                        my_cons_L[constraint_count][0].append(x_wr1_index)
                        my_cons_L[constraint_count][0].append(x_wr2_index)
                        my_cons_L[constraint_count][1].append(S_wtl[worker][task][i])
                        my_cons_L[constraint_count][1].append(-(S_wtl[worker][task][i]))
                        x_wr1_index+=1
                        x_wr2_index+=1
                    my_cons_L[constraint_count][0].append(d_var_index)
                    my_cons_L[constraint_count][1].append(-1)
                    constraint_count += 1
                    r2+=1
        d_var_index += 1

# Zwnr >= (xwr - ywn)
# xwr - zwnr <= ywn
x_wr_index = 0
for region1 in regions:
    x_wr_index = 0
    for region2 in regions:
        for worker in workers:
            my_cons_L.append([[],[]])
            my_cons_type += "L"
            my_cons_L[constraint_count][0].append(x_wr_index)
            my_cons_L[constraint_count][0].append(d_var_index)
            my_cons_L[constraint_count][1].append(1)
            my_cons_L[constraint_count][1].append(-1)
            my_cons_R.append(y_wn[worker][region1])
            constraint_count += 1
            x_wr_index += 1
            d_var_index += 1

#sum(z_wnr) = 1
z_wnr_index = 494
starting_index = 494
for i in range(len(workers)):
    my_cons_L.append([[],[]])
    my_cons_R.append(1)
    my_cons_type += "E"
    for n in range(len(regions)):
        z_wnr_index_n = starting_index + 4 * len(workers) * n
        for r in range(len(regions)):
            z_wnr_index_r = z_wnr_index_n + len(workers) * r
            my_cons_L[constraint_count][0].append(z_wnr_index_r)
            my_cons_L[constraint_count][1].append(1)
            z_wnr_index = z_wnr_index + 1
    constraint_count += 1
    starting_index += 1

#calling Cplex
my_prob = cplex.Cplex()

my_prob.objective.set_sense(my_prob.objective.sense.minimize)
my_prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub, types=my_var_type)

my_prob.linear_constraints.add(lin_expr=my_cons_L, senses=my_cons_type, rhs=my_cons_R)
my_prob.solve()

# get objective value
obj_val = my_prob.solution.get_objective_value()

# get variable value
var_vals = my_prob.solution.get_values()
#Output Section
#Total Number of Worker Assigned
count = 0
for i in range(208):
    if var_vals[i] > 0.5:
        count += 1

print("Worker Assigned: "+str(count))

#Percentage of Work Fulfilled
count = 0
for i in range(208, 209):
    print("Work fulfilled: " + str(var_vals[208]*100) +"%")
    
#Average Skill differential
total = 0

for i in range(209,493):
    total += var_vals[i]
print("Average Skill Differential: "+str(total/(len(tasks)*len(skill))))   


        


#Worker Movement
count = 0
for i in range(494, 1326):
    if var_vals[i] == 1 and my_obj[i] == 0:
        count +=1
print("Worker Stayed: "+ str(count))
count = 0
for i in range(494, 1326):
    if var_vals[i] == 1 and my_obj[i] != 0:
        count +=1
print("Worker Moved: "+ str(count))



#output.csv
result = {}
result["workers/region"] = workers
for j in range(len(regions)):
    result[regions[j]] = []
    for i in range(len(workers)):
        result[regions[j]].append(var_vals[j*len(workers)+i])
      
df = pd.DataFrame.from_dict(result)
df = df.T
df.to_csv('output.csv')

#Movement_of_Workers.csv
output = {}
moved_workers = []
output["worker/region"] = workers
for i in range(len(regions)):
    for j in range(len(regions)):
        output[regions[i]+"->"+regions[j]]=[]
        for k in range(len(workers)):
            output[regions[i]+"->"+ regions[j]].append(var_vals[494+4*len(workers)*i+len(workers)*j+k])
            if regions[i]!=regions[j] and var_vals[494+4*len(workers)*i+len(workers)*j+k] == 1:
                moved_workers.append(workers[k])
df = pd.DataFrame.from_dict(output)
df = pd.DataFrame.transpose(df)
df.to_csv('Movement_of_Workers.csv')

#region:{worker 1, worker 2...}
results= {}
results["workers/region"] = workers
for j in range(len(regions)):
    results[regions[j]] = []
    for i in range(len(workers)):
        if result[regions[j]][i] == 1:
            results[regions[j]].append(workers[i])

        
#sort workers by average skill level
df = pd.read_csv('worker_boro_and_task.csv',index_col=False)
df = df.fillna(0)
table2 = {}
for i in range(len(workers)):
    num = 0
    row = {}
    row = df.iloc[i+1]
    row = row.dropna()
    for task in tasks:
        if row[task] != "na" and row[task] != "nan" and int(row[task]) >= 1 and int(row[task]) <= 5 :
            num += int (row[task])
    table2[workers[i]] = num/len(tasks)
   # table2[workers[i]] = sorted(table2[workers[i]])
table2 = dict(sorted(table2.items(), key = operator.itemgetter(1), reverse = True))

#Assign workers by regions and sorted by average skill levels
table = {}
df = df.fillna(0)
key_list = list(table2.keys()) 
for i in range(len(regions)):
    
    table[regions[i]] = []
    for j in range(len(table2)):
        if key_list[j] in results[regions[i]]:
            table[regions[i]].append(key_list[j] + " " + "(Skill level: " + str(round(table2[key_list[j]], 2)) + ")") 
max = 0
for region in regions:
    if len(table[region]) > max:
        max = len(table[region])

for region in regions:
    while(len(table[region]) < max):
        table[region].append(" ")



#.csv and .xls files output
#csv file
df = pd.DataFrame.from_dict(table)
key_list = list(table.keys())
df.to_csv('result.csv')

#xls file with coloring indicating moved workers
st = xlwt.easyxf('pattern: pattern solid;')

#change pattern_fore_colour here to change the color
st.pattern.pattern_fore_colour = 50
workbook = Workbook()
worksheet = workbook.add_sheet('Sheet 1')
row = 1
col = 0
for key in key_list:
    worksheet.write(row, col, key)
    for i in range(len(table[key])):
        row+=1
        index = table[key][i].find('(')
        if table[key][i][0:index-1] in moved_workers:
            worksheet.write(row, col, table[key][i], st)
        else:
            worksheet.write(row, col, table[key][i])
    col+=1
    row =1
workbook.save('result.xls')
print("see worker assignment at result.xls")
print(var_vals)


