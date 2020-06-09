class candidate:
    def __init__(self, name, java, oracle, unix, accounting):
        self.name = name
        self.java = java
        self.oracle = oracle
        self.unix = unix
        self.accounting = accounting

    def skill_index(self, java, oracle, unix, accounting):
        my_skill_list = {}
        my_skill_list["java"] = java
        my_skill_list["oracle"] = oracle
        my_skill_list["unix"] = unix
        my_skill_list["accounting"] = accounting
        return my_skill_list
        
        

class job:
    def __init__(self, name, Skill_1, Skill_2, level_1, level_2, Weight_1, Weight_2):
        
        self.name = name
        self.Skill_1 = Skill_1
        self.weight_1 = Weight_1
        self.level_1 = level_1
        self.Skill_2 = Skill_2
        self.weight_2 = Weight_2
        self.level_2 = level_2

Sr_Dev = job("Sr_Dev", "java", "oracle", 5, 2, 0.6, 0.4)
Jr_QA = job("Jr_QA", "unix", "oracle", 3, 1, 0.6, 0.4)
Jr_Dev = job("Jr_Dev", "java", "oracle", 3, 2, 0.5, 0.5)
Sr_QA = job("Sr_QA", "unix", "oracle", 4, 3, 0.5, 0.5)
job_list = [Sr_Dev, Jr_QA, Jr_Dev, Sr_QA]

Andrew = candidate("Andrew", 5, 2, 2, 0)
Joel = candidate("Joel", 3, 2, 2, 0)
Pascal = candidate("Pascal", 4, 2, 1, 0)
Chris = candidate("Chris", 1, 3, 4, 0)
Tom = candidate("Tom", 2, 2, 2, 2)
employee_list =[Andrew, Joel, Pascal, Chris, Tom]

def best_fit_score(candidate, job):
    skill_list = candidate.skill_index(candidate.java, candidate.oracle, candidate.unix, candidate.accounting)
    score = min(skill_list[job.Skill_1]/job.level_1, 1)*job.weight_1 + min(skill_list[job.Skill_2]/job.level_2, 1)*job.weight_2

    

    return min(round(score, 2), 1)

andrew_score_sr_dev = best_fit_score(Joel, Sr_Dev)

print(andrew_score_sr_dev)

allocation = {}
for employee in employee_list:
    allocation[employee.name] = {}
    for job in job_list:
        allocation[employee.name][job.name] = best_fit_score(employee, job)

print(allocation)
    

