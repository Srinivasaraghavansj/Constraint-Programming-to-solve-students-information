'''
Srinivasaraghavan Seshadhri R00195470
Decision Analytics Assignment 1 Task 1
MSc Artificial Intelligence MTU 2020-2021 
'''

from ortools.sat.python import cp_model
def main():
    #TASK 1A
    # students are the objects and their names are the values
    students = ["Carol", "Elisa", "Oliver", "Lucas"]
    #The following are the attribute domains for nationalities, genders, studies, universities and name_initials respectively
    nationalities = ["Australia", "USA", "Canada", "South Africa"]
    genders = ["Boy", "Girl"]
    studies = ["History", "Medicine", "Law", "Architecture"]
    universities = ["London", "Cambridge", "Oxford", "Edinburgh"]
    name_initials = ["C", "E", "O", "L"]


    #SolutionPrinter from Zebra example modified to match this application
    #TASK 1D - determine for each student the nationality,the university and the course they chose
    class SolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, nationalities, genders, studies, universities):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.genders_ = genders
            self.nationalities_ = nationalities
            self.studies_ = studies
            self.universities_ = universities
            self.solutions_ = 0

        def OnSolutionCallback(self):
            self.solutions_ = self.solutions_ + 1
            print("+ ---------------------------------------------------------------------------------- +")
            print("| {:^82} |".format("Solution: " + str(self.solutions_)))
            print("+ ---------------------------------------------------------------------------------- +")
            print("+ {:^14} + {:^14} + {:^14} + {:^14} + {:^14} + ".format("--------------","--------------","--------------","--------------","--------------"))
            print("| {:^14} | {:^14} | {:^14} | {:^14} |  {:^13} |".format('STUDENT','NATIONALITY', 'GENDER', 'STUDY FEILD', 'UNIVERSITY'))
            print("+ {:^14} + {:^14} + {:^14} + {:^14} + {:^14} + ".format("--------------","--------------","--------------","--------------","--------------"))

            for student in students:
                stu_ = student
                for n in nationalities:
                    if (self.Value(self.nationalities_[student][n])):
                        name_ = n
                for g in genders:
                    if (self.Value(self.genders_[student][g])):
                        gender_ = g
                for field in studies:
                    if (self.Value(self.studies_[student][field])):
                        field_ = field
                for uni in universities:
                    if (self.Value(self.universities_[student][uni])):
                        uni_ = uni
                print("| {:^14} | {:^14} | {:^14} | {:^14} |  {:^13} |".format(stu_, name_, gender_, field_, uni_))
                print("+ {:^14} + {:^14} + {:^14} + {:^14} + {:^14} + ".format("--------------","--------------","--------------","--------------","--------------"))

    # creating cp_model object
    model = cp_model.CpModel()

    # Creating and adding the 4x4 boolean variables in all possible combinations and permutations of objects and attributes
    student_nationalities = {}
    for student in students:        
        variables = {}
        for n in nationalities:    
            variables[n] = model.NewBoolVar(student+n)
        student_nationalities[student] = variables

    student_genders = {}
    for student in students:        
        variables = {}
        for g in genders:    
            variables[g] = model.NewBoolVar(student+g)
        student_genders[student] = variables

    student_studies = {}
    for student in students:        
        variables = {}
        for s in studies:    
            variables[s] = model.NewBoolVar(student+s)
        student_studies[student] = variables

    student_universities = {}
    for student in students:        
        variables = {}
        for u in universities:    
            variables[u] = model.NewBoolVar(student+u)
        student_universities[student] = variables

    #Assumption of Gender for each student based on Name (Otherwise there are 256 solutions)
    model.AddBoolAnd([
        student_genders["Carol"]["Girl"],student_genders["Carol"]["Boy"].Not(),
        student_genders["Elisa"]["Girl"],student_genders["Elisa"]["Boy"].Not(),       
        student_genders["Oliver"]["Boy"],student_genders["Oliver"]["Girl"].Not(),
        student_genders["Lucas"]["Boy"],student_genders["Lucas"]["Girl"].Not()])


    #TASK 1B

    # Creating First Order Logics - Explicit Constraints

    # One of them is going to London (1).
    # TASK 1E: Taken care by an implicit assumption below, i.e: #Every student attends university
    #This is a redundant sentence which can be ignored and therefore is being ignored

    #Exactly one boy and one girl chose a universities in a city with the same initial of their names (2).
    model.AddBoolOr([
        student_universities["Carol"]["Cambridge"],
        student_universities["Elisa"]["Edinburgh"]])
    model.AddBoolOr([
        student_universities["Carol"]["Cambridge"].Not(),
        student_universities["Elisa"]["Edinburgh"].Not(),])
    model.AddBoolOr([
        student_universities["Oliver"]["Oxford"],
        student_universities["Lucas"]["London"],])
    model.AddBoolOr([
        student_universities["Oliver"]["Oxford"].Not(),
        student_universities["Lucas"]["London"].Not(),])
    model.AddBoolAnd([
        student_universities["Carol"]["Cambridge"],]).\
    OnlyEnforceIf(student_universities["Elisa"]["Edinburgh"].Not())
    model.AddBoolAnd([student_universities["Elisa"]["Edinburgh"],]).OnlyEnforceIf(student_universities["Carol"]["Cambridge"].Not())
    model.AddBoolAnd([
        student_universities["Lucas"]["London"],]).\
    OnlyEnforceIf(student_universities["Oliver"]["Oxford"].Not())
    model.AddBoolAnd([student_universities["Oliver"]["Oxford"],]).OnlyEnforceIf(student_universities["Lucas"]["London"].Not())

    #A boy is from Australia, the other studies History (3).
    model.AddBoolAnd([
        student_nationalities["Oliver"]["Australia"],
        student_nationalities["Lucas"]["Australia"].Not(),
        student_studies['Lucas']['History'],]).\
    OnlyEnforceIf(student_studies['Oliver']['History'].Not())
    model.AddBoolAnd([
        student_nationalities["Oliver"]["Australia"].Not(),
        student_nationalities["Lucas"]["Australia"],
        student_studies['Oliver']['History']]).\
    OnlyEnforceIf(student_studies['Lucas']['History'].Not())

    #A girl goes to Cambridge, the other studies Medicine (4).
    model.AddBoolAnd([
        student_universities["Elisa"]["Cambridge"],
        student_universities["Carol"]["Cambridge"].Not(),
        student_studies["Carol"]["Medicine"]]).\
    OnlyEnforceIf(student_studies["Elisa"]["Medicine"].Not())
    model.AddBoolAnd([
        student_universities["Carol"]["Cambridge"],
        student_universities["Elisa"]["Cambridge"].Not(),
        student_studies["Elisa"]["Medicine"]]).\
    OnlyEnforceIf(student_studies["Carol"]["Medicine"].Not())

    #Oliver studies Law or is from USA; He is not from South Africa (5).
    model.AddBoolOr([
        student_studies["Oliver"]["Law"],
        student_nationalities["Oliver"]["USA"],
        student_nationalities["Oliver"]["South Africa"].Not()])
    model.AddBoolAnd([
        student_studies["Oliver"]["Law"],
        student_nationalities["Oliver"]["South Africa"].Not()]).\
    OnlyEnforceIf(student_nationalities["Oliver"]["USA"].Not())
    model.AddBoolAnd([
        student_nationalities["Oliver"]["USA"],
        student_nationalities["Oliver"]["South Africa"].Not()]).\
    OnlyEnforceIf(student_studies["Oliver"]["Law"].Not())

    #The student from Canada is a historian or will go to Oxford (6).
    for student in students:
        model.AddBoolOr([
            student_studies[student]["History"],
            student_universities[student]["Oxford"]]).\
        OnlyEnforceIf(student_nationalities[student]["Canada"])

    # Sentence 7 - The student from South Africa is going to Edinburgh or will study Law (7).
    for student in students:
        model.AddBoolOr([
            student_universities[student]["Edinburgh"],
            student_studies[student]["Law"],]).\
        OnlyEnforceIf(student_nationalities[student]["South Africa"])

    len_nationalities = len(nationalities)
    len_genders = len(genders)
    len_studies = len(studies)
    len_universities = len(universities)

    #TASK 1C
    #Implicit Constraints are as follows:
    #They are assumptions

    for student in students:
        #Each and every student has one nationality
        variables = []
        for n in nationalities:
            variables.append(student_nationalities[student][n])
        model.AddBoolOr(variables)

        #Each and every student studies one field
        variables = []
        for field in studies:
            variables.append(student_studies[student][field])
        model.AddBoolOr(variables)

        #Each and every student attends one university
        variables = []
        for uni in universities:
            variables.append(student_universities[student][uni])
        model.AddBoolOr(variables)

    for index in range(len(students)):
        for j_index in range(index + 1, len(students)):
            #Every student has unique Nationality
            for k_index in range(len_nationalities):
                model.AddBoolOr([
                    student_nationalities[students[index]][nationalities[k_index]].Not(),
                    student_nationalities[students[j_index]][nationalities[k_index]].Not()])
            #Every student pursues an unique study
            for k_index in range(len_studies):
                model.AddBoolOr([
                    student_studies[students[index]][studies[k_index]].Not(),
                    student_studies[students[j_index]][studies[k_index]].Not()])
            #Every student goes to unique university
            for k_index in range(len_universities):
                model.AddBoolOr([
                    student_universities[students[index]][universities[k_index]].Not(),
                    student_universities[students[j_index]][universities[k_index]].Not()])

    #Initialize/Load Constraint Programming Solver
    solver = cp_model.CpSolver()
    #TASK 1D - Solve the CP-SAT model and determine for each student the nationality,the university and the course they chose
    solver.SearchForAllSolutions(model, SolutionPrinter(
        student_nationalities,
        student_genders,
        student_studies,
        student_universities))

    #Print Final Solution
    for student in students:
        if solver.Value(student_studies[student]["Architecture"]):
            for n in nationalities:
                if solver.Value(student_nationalities[student][n]):
                    print("| {:^82} |".format("The nationality of the Architecture student is " + n))
                    print("+ ---------------------------------------------------------------------------------- +")
                    break
if __name__ == "__main__":
    main()