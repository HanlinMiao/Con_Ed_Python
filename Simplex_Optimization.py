import random
import copy

candidate_job_list = {'Andrew': {'Sr_Dev': 1.0, 'Jr_QA': 0.8, 'Jr_Dev': 1.0, 'Sr_QA': 0.58},
                  'Joel': {'Sr_Dev': 0.76, 'Jr_QA': 0.8, 'Jr_Dev': 1.0, 'Sr_QA': 0.58},
                  'Pascal': {'Sr_Dev': 0.88, 'Jr_QA': 0.6, 'Jr_Dev': 1.0, 'Sr_QA': 0.46},
                  'Chris': {'Sr_Dev': 0.52, 'Jr_QA': 1.0, 'Jr_Dev': 0.67, 'Sr_QA': 1.0},
                  'Tom': {'Sr_Dev': 0.64, 'Jr_QA': 0.8, 'Jr_Dev': 0.83, 'Sr_QA': 0.58}}


# maximize (2x1 + x2 + x3 + x4)


job_list_index = {'Sr_Dev': 1, 'Jr_QA': 2, 'Jr_Dev': 3, 'Sr_QA': 4}
job_list_num = {'Sr_Dev': 2, 'Jr_QA': 1, 'Jr_Dev': 1, 'Sr_QA': 1}
candidate_list = ['Andrew', 'Joel', 'Pascal', 'Chris', 'Tom']
job_list = ['Sr_Dev', 'Jr_QA', 'Jr_Dev', 'Sr_QA']

run_times = 100


def random_position_assignment(num_pos, index, num):
    
    index_key_list = list(index.keys())
    index_val_list = list(index.values())
    num_key_list = list(num.keys())
    num_val_list = list(num.values())
    best_candidate_list = []
    i = 0
    while(i<num_pos):
        p = random.randint(1, len(index))
        if num[index_key_list[index_val_list.index(p)]] > 0:
            num[index_key_list[index_val_list.index(p)]] = num[index_key_list[index_val_list.index(p)]]-1
            best_candidate_list.append(p)
        else:
            i = i - 1

        i = i+1
    
    return best_candidate_list

def max_job_score(candidate_scores,candidates, job, index, num, num_pos, times):
    num1 = num.copy()
    global_sum = 0
    record = []
    for j in range(times):
        print(j)
        print("global_sum: " +str(global_sum))
        num = num1.copy()
        random_list = random_position_assignment(num_pos, index, num)
        local_sum = 0
        if random_list not in record:
            record.append(random_list)
            for i in range(len(random_list)):
                local_sum += candidate_scores[candidates[i]][job_list[random_list[i]-1]]
            if local_sum >= global_sum:
                    global_sum = local_sum     
        else:
            continue;

            
            
    return global_sum

print(max_job_score(candidate_job_list, candidate_list, job_list, job_list_index, job_list_num, 5, run_times))





