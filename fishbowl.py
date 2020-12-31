import os
import time
import random
import winsound
import numpy as np

def myClue(clue, correct_clues, score,cluesLeft):
    keep_going = True
    action = input("{} ".format(clue)).lower()
    if (action == ""):
        correct_clues.append(clue)
        score = score + 1
        print("    Correct! Point tally: {0}, Remaining Clues: {1}".format(score,cluesLeft-1))
    elif action == "t":
        print("    Time's Up!")
        keep_going = False
    else:
        myClue(clue, correct_clues, score)
    return correct_clues, score, keep_going


def myTurn(my_names,my_team):
    clues = my_names
    random.shuffle(clues)
    correct_clues = []
    score = 0
    for clue in clues:
        clues_left = [i for i in clues if i not in correct_clues]
        correct_clues, score, keep_going = myClue(clue, correct_clues, score ,len(clues_left))
        if not keep_going:
            break

    remaining_clues = [i for i in clues if i not in correct_clues]

    return remaining_clues, score


def myRound(my_names,my_teams):
    score_dict = {t:0 for t in my_teams}

    i = 1
    while len(my_names)>0:
        for t in my_teams:
            ready_to_go = input("Ready? Round {0}, Team {1} (Hit Enter when ready): ".format(i, t))
            print("Clue Keystrokes: Correct ['Enter'] or Time's Up ['t']\n")
            my_names, score = myTurn(my_names,t)
            score_dict[t] = score_dict[t] + score
            print("    Remaining Clues: {}".format(len(my_names)))
            print("    Team {0} Score: {1}".format(t,score_dict[t]))
        i += 1

    print("    End of Round!")
    print("    Round Score: {}".format(score_dict))

    return(score_dict)

def main():
    gameFile = input("Filename: \n")
    if ".txt" not in gameFile:
        gameFile = gameFile + ".txt"
    
    teams = input("Teams (separated by commas): \n")
    my_teams = [x.strip() for x in teams.split(",")]

    fishbowl_names = open(gameFile,"r").read().splitlines()

    team_scores = {x:0 for x in my_teams}

    for i in ["Taboo","Charades","Password"]:
        start_game = input("Teams {0}, are you ready for the {1} Phase? y/n\n".format(" and ".join(my_teams), i)).lower()

        if (start_game == "y") or(start_game == ""):
            print("Alright, let's begin the {} Phase.".format(i))
            scores = myRound(fishbowl_names,my_teams)
            team_scores = {x:team_scores[x] + scores[x] for x in scores.keys()}
            print("{0} Phase Complete.  Team scores: {1}".format(i,team_scores))
        elif start_game == "n":
            print("Skipping the {} Phase.\n".format(i))
    winner = max(team_scores, key=team_scores.get)
    print("Game over.  Congratulations Team {}.  Final Score {}".format(winner,' - '.join(team_scores.values())))


if __name__ == "__main__":
    main()