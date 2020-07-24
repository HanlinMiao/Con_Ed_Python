import pandas as pd
import cplex
import random
import sys

#Indices
weight1 = 0.33
weight2 = 0.33
weight3 = 0.001

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

#d_nr: The distance between two regions in miles
distance = {}
distance["n/r"] = list(regions)
for worker in workers:
    distance[worker] = {}
    for region1 in regions:
        distance[worker][region1] = {}
        for region2 in regions:
            if region1 == region2:
                distance[worker][region1][region2] = 0
            else:
                distance[worker][region1][region2]= random.random()
        



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
        my_ub.append(cplex.infinity)
        my_lb.append(0)
        my_obj.append(weight2/(len(tasks)*len(skill)))
        
#z_wnr for 52 workers and 4 regions, binary 0, 1
for region1 in regions:
    for region2 in regions:
        for worker in workers:
            my_var_type += "B"
            my_ub.append(1)
            my_lb.append(0)
            my_obj.append(weight3*distance[worker][region1][region2])

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

#-1600wxrw /mNrm + φ <= 0
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

    
#wxwr1swtl - wxwr2swtl - Θ_tl<=0
d_var_index = 209
x_wr1_index = 0
x_wr2_index = len(workers)
for task in tasks:
    for i in range(5):
        for r1 in range(len(regions)):
            r2 = r1+1
            while(r2<len(regions)):
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



#xwr -zwnr <= ywn

x_wr_index = 0
d_var_index = 494
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
            d_var_index +=1


            
#sum(z_wnr)<=1
z_wnr_index = 494
starting_index = 494
for i in range(len(workers)):
    my_cons_L.append([[],[]])
    my_cons_R.append(1)
    my_cons_type += "E"
    for n in range(len(regions)):
        z_wnr_index_n = starting_index + 4 *len(workers)*n
        for r in range(len(regions)):
            z_wnr_index_r = z_wnr_index_n  + len(workers)*r
            my_cons_L[constraint_count][0].append(z_wnr_index_r)
            my_cons_L[constraint_count][1].append(1)
    constraint_count +=1
    starting_index += 1


        
        
my_prob = cplex.Cplex()
my_prob.objective.set_sense(my_prob.objective.sense.minimize)
my_prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub, types=my_var_type)
my_prob.linear_constraints.add(lin_expr=my_cons_L, senses=my_cons_type, rhs=my_cons_R)
my_prob.solve()

# get objective value
obj_val = my_prob.solution.get_objective_value()

# get variable value
var_vals = my_prob.solution.get_values()

print(obj_val)
print(var_vals)

count = 0
for i in range(208):
    if var_vals[i] > 0.5:
        count +=1
print("Worker Assigned: "+str(count))
count = 0
for i in range(208, 209):
    print("Work fulfilled: " + str(var_vals[208]*100) +"%")
total = 0
for i in range(209, 493):
    total += var_vals[i]
print("Average Skill Differential: "+str(total/(57*5)))

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

output = {}
output["worker/region"] = workers
for j in range(len(regions)):
    output[regions[j]] = []
    for i in range(len(workers)):
        output[regions[j]].append(var_vals[j*len(workers)+i])
        
df = pd.DataFrame.from_dict(output)
df = pd.DataFrame.transpose(df)
df.to_csv('output.csv')

output = {}
output["worker/region"] = workers

for i in range(len(regions)):
    for j in range(len(regions)):
        output[regions[i]+"->"+regions[j]]=[]
        for k in range(len(workers)):
            output[regions[i]+"->"+ regions[j]].append(var_vals[494+4*len(workers)*i+len(workers)*j+k])
        
df = pd.DataFrame.from_dict(output)
df = pd.DataFrame.transpose(df)
df.to_csv('output1.csv')



