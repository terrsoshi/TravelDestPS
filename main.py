#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#importing required modules and classes
from rule import Rule
from fact import Fact
import sys
import copy

#Function to prompt user input by asking questions
def askQuestion(factList, workingMemory, initialsolList):
    while True:
        try:   
            print("\nPlease enter the number corresponding to a fact to select it from the following facts: \n")
            for i in range (len(factList)):
                print(str(i+1) + ". " + factList[i].subject + " " + factList[i].condition)
            fact_select = int(input(""))
            if fact_select >= 1 and fact_select <= len(factList):
                workingMemory.append(factList[fact_select-1])
                initialsolList.append(factList[fact_select-1])
                break
            else:
                print("You have entered an invalid number, please try again.")
        except ValueError:
            print("You have entered an invalid input, please try again.")

#Function to check if a final output has been identified
def checkGoal(rule, hypothesisList):
    itsGoal = False
    for goals in hypothesisList:
        if rule.then_fact.subject == goals.subject and rule.then_fact.condition == goals.condition:
            itsGoal = True
            break
    return itsGoal

def fire_rules_forward(ruleList, workingMemory, hypothesisList, solutionList):
    goal_found = False
    rules_fired = True
    while rules_fired == True:
        rules_fired = False
        index = 0
        while index < len(ruleList):
            i = ruleList[index]
            for j in workingMemory:
                if i.if_fact.subject == j.subject:
                    if i.if_fact.condition == j.condition:
                        if i.if_and == False:    
                            print("\nRule " + str(i.id) + " has been fired.")
                            print("If " + str(i.if_fact.subject) + " " + str(i.if_fact.condition) + ", then " + str(i.then_fact.subject) + " " + str(i.then_fact.condition) + ".")
                            goal_found = checkGoal(i, hypothesisList)
                            ruleList.remove(i)
                            index -= 1
                            workingMemory.remove(j)
                            workingMemory.append(i.then_fact)
                            solutionList.append(i.then_fact)
                            rules_fired = True
                            break
                        else:
                            for z in workingMemory:
                                if i.if_fact2.subject == z.subject:
                                    if i.if_fact2.condition == z.condition:
                                        print("\nRule " + str(i.id) + " has been fired.")
                                        print("If " + str(i.if_fact.subject) + " " + str(i.if_fact.condition) + " and " + str(i.if_fact2.subject) + " " + str(i.if_fact2.condition) + ", then " + str(i.then_fact.subject) + " " + str(i.then_fact.condition) + ".")
                                        goal_found = checkGoal(i, hypothesisList)
                                        ruleList.remove(i)
                                        index -= 1
                                        workingMemory.remove(j)
                                        workingMemory.remove(z)
                                        workingMemory.append(i.then_fact)
                                        if len(solutionList) >= 0:
                                            concatString = i.if_fact.subject + " " + i.if_fact.condition + ", " + i.if_fact2.subject + " " + i.if_fact2.condition
                                            concatString2 = solutionList[-1].subject + " " + solutionList[-1].condition
                                            if concatString != concatString2:
                                                solutionList.append(Fact((str(i.if_fact.subject) + " " + str(i.if_fact.condition) + ","), (str(i.if_fact2.subject) + " " + i.if_fact2.condition))) 
                                        solutionList.append(i.then_fact)
                                        rules_fired = True
                                        break
            index += 1
    return goal_found
                  
def fire_rules_backward(backwardRuleList, workingMemory, solutionList):
    rules_fired = True
    while rules_fired == True:
        rules_fired = False
        for i in reversed(backwardRuleList):
            for j in workingMemory:
                if i.then_fact.subject == j.subject:
                    if i.then_fact.condition == j.condition:
                        print("\nRule " + str(i.id) + " has been fired.")
                        backwardRuleList.remove(i)
                        workingMemory.remove(j)
                        workingMemory.append(i.if_fact)
                        if len(solutionList) >= 0:
                            concatString = i.then_fact.subject + " " + i.then_fact.condition
                            concatString2 = solutionList[-1].subject + " " + solutionList[-1].condition
                            if concatString != concatString2:
                                solutionList.append(i.then_fact)
                        if i.if_and == True:    
                            workingMemory.append(i.if_fact2)
                            print("If " + str(i.if_fact.subject) + " " + str(i.if_fact.condition) + " and " + str(i.if_fact2.subject) + " " + str(i.if_fact2.condition) + ", then " + str(i.then_fact.subject) + " " + str(i.then_fact.condition) + ".")
                            if len(solutionList) >= 0:
                                concatString = i.if_fact.subject + " " + i.if_fact.condition + ", " + i.if_fact2.subject + " " + i.if_fact2.condition
                                concatString2 = solutionList[-1].subject + " " + solutionList[-1].condition
                                if concatString != concatString2:
                                    solutionList.append(Fact((str(i.if_fact.subject) + " " + str(i.if_fact.condition) + ","), (str(i.if_fact2.subject) + " " + i.if_fact2.condition))) 
                        else:
                            print("If " + str(i.if_fact.subject) + " " + str(i.if_fact.condition) + ", then " + str(i.then_fact.subject) + " " + str(i.then_fact.condition) + ".")
                            solutionList.append(i.if_fact)
                        rules_fired = True
                        break
         
rules = [Rule(1, "Budget", "Medium (RM2,000 - RM4,000)", "Suitable Place is", "Japan", True, "Season", "is Spring"),
         Rule(2, "Suitable Place is", "China", "Recommended Travel Destination is", "Beijing, China", True, "Travelling", "as Couple"),
         Rule(3, "Budget", "High (above RM4,000)", "Suitable Place is", "Europe", True, "Season", "is Winter"),
         Rule(4, "Suitable Place is", "Japan", "Recommended Travel Destination is", "Tokyo, Japan", True, "Travelling", "with Family"),
         Rule(5, "Suitable Place is", "South Korea", "Recommended Travel Destination is", "Jeju Island, South Korea", True, "Travelling", "as Couple"),
         Rule(6, "Suitable Place is", "United Kingdom", "Recommended Travel Destination is", "Edinburgh, Scotland", True, "Travelling", "as Couple"),
         Rule(7, "Suitable Place is", "China", "Recommended Travel Destination is", "Guangzhou, China", True, "Travelling", "with Friends"),
         Rule(8, "Budget", "High (above RM4,000)", "Suitable Place is", "United States of America", True, "Season", "is Summer"),
         Rule(9, "Budget", "High (above RM4,000)", "Suitable Place is", "Europe", True, "Season", "is Spring"),
         Rule(10, "Suitable Place is", "Japan", "Recommended Travel Destination is", "Osaka, Japan", True, "Travelling", "with Friends"),
         Rule(11, "Suitable Place is", "Thailand", "Recommended Travel Destination is", "Chiang Mai, Thailand", True, "Travelling", "with Family"),
         Rule(12, "Budget", "Low (below RM2,000)", "Suitable Place is", "Vietnam", True, "Season", "is Fall"),
         Rule(13, "Suitable Place is", "Europe", "Recommended Travel Destination is", "Amsterdam, Netherland", True, "Travelling", "with Friends"),
         Rule(14, "Budget", "Medium (RM2,000 - RM4,000)", "Suitable Place is", "South Korea", True, "Season", "is Fall"),
         Rule(15, "Suitable Place is", "Australia", "Recommended Travel Destination is", "Perth, Australia", True, "Travelling", "as Couple"),
         Rule(16, "Suitable Place is", "United States of America", "Recommended Travel Destination is", "Las Vegas, Nevada", True, "Travelling", "with Family"),
         Rule(17, "Suitable Place is", "Vietnam", "Recommended Travel Destination is", "", True, "Travelling", "with Friends"),
         Rule(18, "Budget", "High (above RM4,000)", "Suitable Place is", "United Kingdom", True, "Season", "is Fall"),
         Rule(19, "Budget", "Low (below RM2,000)", "Suitable Place is", "China", True, "Season", "is Winter"),
         Rule(20, "Suitable Place is", "Europe", "Recommended Travel Destination is", "Rome, Italy", True, "Travelling", "with Family"),
         Rule(21, "Suitable Place is", "United Kingdom", "Recommended Travel Destination is", "Belfast, Northern Ireland", True, "Travelling", "with Friends"),
         Rule(22, "Suitable Place is", "Japan", "Recommended Travel Destination is", "Kyoto, Japan", True, "Travelling", "as Couple"),
         Rule(23, "Suitable Place is", "United States of America", "Recommended Travel Destination is", "New York, New York State", True, "Travelling", "with Friends"),
         Rule(24, "Budget", "Medium (RM2,000 - RM4,000)", "Suitable Place is", "Australia", True, "Season", "is Summer"),
         Rule(25, "Budget", "Low (below RM2,000)", "Suitable Place is", "Thailand", True, "Season", "is Summer"),
         Rule(26, "Suitable Place is", "Vietnam", "Recommended Travel Destination is", "Ho Chi Minh, Vietnam", True, "Travelling", "with Family"),
         Rule(27, "Suitable Place is", "Thailand", "Recommended Travel Destination is", "Bangkok, Thailand", True, "Travelling", "with Friends"),
         Rule(28, "Suitable Place is", "Australia", "Recommended Travel Destination is", "Sydney, Australia", True, "Travelling", "with Family"),
         Rule(29, "Suitable Place is", "United Kingdom", "Recommended Travel Destination is", "London, England", True, "Travelling", "with Family"),
         Rule(30, "Suitable Place is", "Thailand", "Recommended Travel Destination is", "Pattaya, Thailand", True, "Travelling", "as Couple"),
         Rule(31, "Suitable Place is", "Europe", "Recommended Travel Destination is", "Paris, France", True, "Travelling", "as Couple"),
         Rule(32, "Budget", "Medium (RM2,000 - RM4,000)", "Suitable Place is", "Japan", True, "Season", "is Winter"),
         Rule(33, "Suitable Place is", "Australia", "Recommended Travel Destination is", "Melbourne, Australia", True, "Travelling", "with Friends"),
         Rule(34, "Suitable Place is", "South Korea", "Recommended Travel Destination is", "Seoul, South Korea", True, "Travelling", "with Friends"),
         Rule(35, "Budget", "Low (below RM2,000)", "Suitable Place is", "China", True, "Season", "is Spring"),
         Rule(36, "Suitable Place is", "South Korea", "Recommended Travel Destination is", "Busan, South Korea", True, "Travelling", "with Family"),
         Rule(37, "Budget", "Medium (RM2,000 - RM4,000)", "Suitable Place is", "Japan", True, "Season", "is Spring"),
         Rule(38, "Suitable Place is", "China", "Recommended Travel Destination is", "Shanghai, China", True, "Travelling", "with Family"),
         Rule(39, "Suitable Place is", "United States of America", "Recommended Travel Destination is", "San Francisco, California", True, "Travelling", "as Couple"),
         Rule(40, "Suitable Place is", "Vietnam", "Recommended Travel Destination is", "Hanoi, Vietnam", True, "Travelling", "as Couple")]


budgets = [Fact("Budget", "Low (below RM2,000)"),
         Fact("Budget", "Medium (RM2,000 - RM4,000)"),
         Fact("Budget", "High (above RM4,000)")]

seasons = [Fact("Season", "is Summer"),
         Fact("Season", "is Winter"),
         Fact("Season", "is Spring"),
         Fact("Season", "is Fall")]

travelCompanions = [Fact("Travelling", "as Couple"),
                    Fact("Travelling", "with Family"),
                    Fact("Travelling", "with Friends")]

hypotheses = [Fact("Recommended Travel Destination is", "Tokyo, Japan"),
              Fact("Recommended Travel Destination is", "Jeju Island, South Korea"),
              Fact("Recommended Travel Destination is", "Bangkok, Thailand"),
              Fact("Recommended Travel Destination is", "Da Nang, Vietnam"),
              Fact("Recommended Travel Destination is", "Kyoto, Japan"),
              Fact("Recommended Travel Destination is", "Belfast, Northern Ireland"),
              Fact("Recommended Travel Destination is", "Busan, South Korea"),
              Fact("Recommended Travel Destination is", "Seoul, South Korea"),
              Fact("Recommended Travel Destination is", "Shanghai, China"),
              Fact("Recommended Travel Destination is", "London, England"),
              Fact("Recommended Travel Destination is", "Ho Chi Minh, Vietnam"),
              Fact("Recommended Travel Destination is", "Rome, Italy"),
              Fact("Recommended Travel Destination is", "Hanoi, Vietnam"),
              Fact("Recommended Travel Destination is", "Guangzhou, China"),
              Fact("Recommended Travel Destination is", "Perth, Australia"),
              Fact("Recommended Travel Destination is", "Las Vegas, Nevada"),
              Fact("Recommended Travel Destination is", "San Francisco, California"),
              Fact("Recommended Travel Destination is", "Paris, France"),
              Fact("Recommended Travel Destination is", "Sydney, Australia"),
              Fact("Recommended Travel Destination is", "Amsterdam, Netherland"),
              Fact("Recommended Travel Destination is", "New York, New York State"),
              Fact("Recommended Travel Destination is", "Melbourne, Australia"),
              Fact("Recommended Travel Destination is", "Edinburgh, Scotland"),
              Fact("Recommended Travel Destination is", "Pattaya, Thailand"),
              Fact("Recommended Travel Destination is", "Chiang Mai, Thailand"),
              Fact("Recommended Travel Destination is", "Osaka, Japan"),
              Fact("Recommended Travel Destination is", "Beijing, China")]

solution = []

#Main Program

#Main Menu
while True:
    try:
        print("\n-------------------------------------------------------------------------------------------------------------")
        print("Enter 1 for forward chaining, 2 for backward chaining, 3 to print the list of rules or 4 to exit the program:")
        print("-------------------------------------------------------------------------------------------------------------")
        user_input = int(input(""))
        if user_input >= 1 and user_input <=2:
            break
        elif user_input == 3:
            print("")
            for i in rules:
                if i.if_and == False:
                    print(str(i.id) + " If " + str(i.if_fact.subject) + " " + str(i.if_fact.condition) + ", then " + str(i.then_fact.subject) + " " + str(i.then_fact.condition) + ".")
                else:
                    print(str(i.id) + " If " + str(i.if_fact.subject) + " " + str(i.if_fact.condition) + " and " + str(i.if_fact2.subject) + " " + str(i.if_fact2.condition) + ", then " + str(i.then_fact.subject) + " " + str(i.then_fact.condition) + ".")
        elif user_input == 4:
            sys.exit()
        else:
            print("You have entered an invalid number, please try again.")
    except ValueError:
        print("You have entered an invalid input, please try again.")

#Forward Chaining
if user_input == 1:
    working_memory=[]
    initial_sol = []
    
    #Select Facts
    askQuestion(budgets, working_memory, initial_sol)
    askQuestion(seasons, working_memory, initial_sol)
    askQuestion(travelCompanions, working_memory, initial_sol)
    
    #Group all facts chosen together in the solution list
    concat_subject = ""
    for i in range(len(initial_sol)-1):
        concat_subject += initial_sol[i].subject + " " + initial_sol[i].condition + ","
        if i+1 != len(initial_sol)-1:
            concat_subject += " "
    solution.append(Fact(concat_subject, (initial_sol[-1].subject + " " + initial_sol[-1].condition)))

    #Firing rules forward
    goal_found = fire_rules_forward(rules, working_memory, hypotheses, solution)
    
    #Conclusion from forward chaining process
    print("")
    if goal_found == True:
        sol = working_memory[-1]
        print("The conclusion deduced: " + str(sol.subject) + " " + str(sol.condition))
    else:
        print("A conclusion cannot be made from the facts chosen and rules fired.")
    
#Backward Chaining
else:
    working_memory = []
    
    #Choose Hypothesis
    while True:
        try:   
            print("\nPlease enter the number corresponding to a hypothesis to select it from the following hypotheses: \n")
            for i in range (len(hypotheses)):
                print(str(i+1) + ". " + hypotheses[i].subject + " " + hypotheses[i].condition)
            hypothesis_select = int(input(""))
            if hypothesis_select >= 1 and hypothesis_select <= len(hypotheses):
                working_memory.append(hypotheses[hypothesis_select-1])
                hypothesis_selected = hypotheses[hypothesis_select-1]
                solution.append(hypotheses[hypothesis_select-1])
                break
            else:
                print("You have entered an invalid number, please try again.")
        except ValueError:
            print("You have entered an invalid input, please try again.")
            
    #Firing rules backward
    rules_backward = copy.deepcopy(rules)
    fire_rules_backward(rules_backward, working_memory, solution)
    
    #Finish backward chaining and list all facts found from hypothesis chosen
    print("\nBackward chaining is done, facts found:\n")
    for i in working_memory:
        print("- "+ str(i.subject) + " " + str(i.condition))   
        
    #Perform forward chaining to prove hypothesis chosen
    print("\nPerforming forward chaining with facts found to check if hypothesis is correct.")    
    
    #Firing rules forward to check hypothesis selected
    goal_found = fire_rules_forward(rules, working_memory, hypotheses, solution)
                           
    #Conclusion from backward chaining process     
    if goal_found == True:
        sol = working_memory[-1]
        if sol.subject == hypothesis_selected.subject and sol.condition == hypothesis_selected.condition:
            sol = working_memory[-1]
            print("\nHypothesis selected: " + str(hypothesis_selected.subject) + " " + str(hypothesis_selected.condition))
            print("Conclusion deduced from facts gathered: " + str(sol.subject) + " " + str(sol.condition))
            print("\nTherefore, the hypothesis is proven.\n")
        else:
            print("\nHypothesis cannot be proved.")
            
            
#Inference process printing
print("\nInference process:")
for i in range(len(solution)):
    if i != (len(solution)-1):
        print("| " + solution[i].subject + " " + solution[i].condition + " | => ", end = '')
    else:
        print("| " + solution[i].subject + " " + solution[i].condition + " |")
    
                    

    
    
    









