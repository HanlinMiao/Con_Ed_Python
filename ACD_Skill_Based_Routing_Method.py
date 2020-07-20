import csv

class employee:
    def __init__(self, Name, Skill_Index, Years_of_Exp, Location, Status):
        self.Name = Name,
        self.Skill_Index = int(Skill_Index, 10)
        self.Years_of_Exp = int(Years_of_Exp, 10)
        self.Location = Location
        self.Status = Status
#Initialize and read the employee list from a .csv file    
employee_list =  {}
with open('Employee List.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    i = 0
    for row in csv_reader:
        if i == 0:
            (f'Column names are {", ".join(row)}')
            i += 1
        else:
            person = employee(row[0],row[1],row[2],row[3],row[4])
            employee_list[i] = person
            i+=1;
            
#print the list of employees
def print_list(employee_list):
    for i in range(1, len(employee_list)+1):
        print(employee_list[i].Name, employee_list[i].Skill_Index, employee_list[i].Years_of_Exp, employee_list[i].Location, employee_list[i].Status)

#return the new employee list after sorting
def new_employee_list(myDict):
    new_employee_list =  {}
    count = 1
    for i in range(1, len(myDict)+1):
        for j in range(len(myDict[i])):
                new_employee_list[count] = myDict[i][j]
                count += 1
    return new_employee_list
#sort employees by skill level index
def sort_list_skill(employee_list, skill_index):
    myDict = {};
    for i in range(1, skill_index+1):
        myDict[i] = []
    for j in range(1, len(employee_list)+1):
        myDict[employee_list[j].Skill_Index].append(employee_list[j])
    return myDict
skill_table = sort_list_skill(employee_list, 5)

#sort employees by years of experience
def sort_year_of_exp(employee_list):
    max_year = 0
    for i in range(1, len(employee_list)+1):
        if employee_list[i].Years_of_Exp >= max_year:
            max_year = employee_list[i].Years_of_Exp
    myDict = {};
    for i in range(1, max_year+1):
        myDict[i] = []
    for j in range(1, len(employee_list)+1):
        myDict[employee_list[j].Years_of_Exp].append(employee_list[j])
    return myDict
exp_table = sort_year_of_exp(employee_list)




print("Original: ")
print_list(employee_list)
print("List after sorting by skills: ")
print_list(new_employee_list(skill_table))
print("List after sorting by years of experience: ")
print_list(new_employee_list(exp_table))
