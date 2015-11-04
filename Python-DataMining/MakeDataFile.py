import urllib.request
import os
import platform
import time
import re
import sys
import string
import html


#To get Unix and Windows
platformType = platform.system()

#	Things to fix within Program:
#       Add up to 4 Officials, make sure every line has 4 even if they are blank
#       Get rid of ',Jr.' in players names.
#       Get rid of NA in Position
#       Fix ', ' and ' ,' to ','
#       Get rid of N/A in attendence to ''
#       \' in Names to '
#       
#

def main():

    runningTotal = 0

    totalFile = open('numberOfLines.txt', 'r')
    runTotalStr = str(totalFile.read())
    runningTotal = int(runTotalStr)
    totalFile.close()

    topdeck_dir = os.getcwd()

    os.chdir("..")

    currentDirectory = os.getcwd()

    if platformType == 'Windows':
        MASTERdirectory = currentDirectory + "\\ESPN_HTML_Cache\\"
        directoryName = currentDirectory + "\\ESPN_HTML_Cache\\Day_Files\\"
        NewDirectoryName = MASTERdirectory + "Game_Files\\"
        altDirectoryName = MASTERdirectory + "Game_Files_Done\\"

    else:
        MASTERdirectory = currentDirectory + "/ESPN_HTML_Cache/"
        directoryName = currentDirectory + "/ESPN_HTML_Cache/Day_Files/"
        NewDirectoryName = MASTERdirectory + "Game_Files/"
        altDirectoryName = MASTERdirectory + "Game_Files_Done/"
    
    try: 
        os.makedirs(directoryName)
    except OSError:                    
        if not os.path.isdir(directoryName):
            raise

    os.chdir(MASTERdirectory)

    fileList = os.listdir(NewDirectoryName)

    Main_player_list = []

    #Bool to check if data within each line is correct (checks for '<' and/or '>' and anything other than numbers)
    skip_bool = False

    file_error_list = []

    numDone = 0

    #List of RE Compile Objects:

    RE_team_name_and_score = re.compile('mens-college-basketball.*?">(.*?)</a> <span>(.*?)</span>')
    RE_game_time_loc = re.compile('game-time-location"><p>(.*?)<')
    RE_raw_data_file = re.compile('my-players-table(.*?)"></div></div></div></div>', re.DOTALL)
    RE_officals = re.compile('Officials:</strong> (.*?)<br>')
    RE_attendence = re.compile('Attendance:</strong> (.*?)<br')
    RE_team_data = re.compile('STARTERS(.*?TOTALS)', re.DOTALL)
    RE_team_data_starts = re.compile('STARTERS(.*?</thead><tbody><tr align="right" class=odd>)', re.DOTALL)
    RE_team_data_benchs = re.compile('BENCH(.*?</tbody>)', re.DOTALL)

    RE_type_one_search = re.compile('class="even" align="right"')
    RE_type_one_team_starter_list = re.compile('</thead><tbody><tr class="even" align="right">(.*?)>BENCH</th>', re.DOTALL)
    RE_type_one_team_bench_list = re.compile('/thead><tbody><tr class="odd" align="right">(.*?)>TOTALS', re.DOTALL)

    RE_type_two_search = re.compile('align="right" class=even')
    RE_type_two_team_starter_list = re.compile('</thead><tbody><tr align="right" class=even>(.*?)>BENCH</th>', re.DOTALL)
    RE_type_two_team_bench_list = re.compile('/thead><tbody><tr align="right" class=odd>(.*?)>TOTALS', re.DOTALL)


    RE_team_starters = re.compile('href=".*?>(.*?)</a>, (.*?)</td><td>(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)<.*?">(.*?)</td><td.*?>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)<')
    RE_team_bench = re.compile('href=".*?>(.*?)</a>, (.*?)</td><td>(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)<.*?">(.*?)</td><td.*?>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)<')

    RE_team_starters1 = re.compile('href=".*?>(.*?)</a>, (.*?)</td><td>(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)<.*?">(.*?)</td><td.*?>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)<')
    RE_team_bench1 = re.compile('href=".*?>(.*?)</a>, (.*?)</td><td>(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)<.*?">(.*?)</td><td.*?>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)<')

    RE_team_starters2 = re.compile('href=".*?>(.*?)</a>, (.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)<.*?">(.*?)</td><td.*?>.*?</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)<')
    RE_team_bench2 = re.compile('href=".*?>(.*?)</a>, (.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)</td><td>(.*?)-(.*?)<.*?">(.*?)</td><td.*?>.*?</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)<')


    for i in fileList:

        #Bool to check if data within each line is correct (checks for '<' and/or '>' and anything other than numbers)
        skip_bool = False
        noMins = False
        
        htmlfile = open(NewDirectoryName + i, 'rb')

        textfile = str(htmlfile.read())
        
        htmlfile.close()

        team_names_and_scores = re.findall(RE_team_name_and_score, textfile)

        first_team = team_names_and_scores[0][0]
        first_team_away = "Away"
        first_team_score = team_names_and_scores[0][1]

        second_team = team_names_and_scores[1][0]
        second_team_home = "Home"
        second_team_score = team_names_and_scores[1][1]

        first_team_won = "Loss"
        second_team_won = "Loss"
        
        if first_team_score > second_team_score:
            first_team_won = "Won"
        else:
            second_team_won = "Won"

        game_time_location = re.findall(RE_game_time_loc, textfile)

        raw_data_from_file = re.findall(RE_raw_data_file, textfile)
        
        officals = re.findall(RE_officals, raw_data_from_file[0])
        
        attendence = re.findall(RE_attendence, raw_data_from_file[0])
        
        team_data = re.findall(RE_team_data, textfile)

        starts_data = re.findall(RE_team_data_starts, textfile)
        benchs_data = re.findall(RE_team_data_benchs, textfile)
        
        if len(team_data) == 0 and len(starts_data) != 2 and len(benchs_data) != 2:
            print(i, " file has failed, insufficient data")
            numDone += 1
            file_error_list.append(i)


        else:
#       <------------------------------------------------------------------------------------------------------------------------------------------------->
            if len(team_data) == 0:
                
                first_team_starters = re.findall(RE_team_starters, starts_data[0])
                first_team_bench = re.findall(RE_team_bench, benchs_data[0])

                second_team_starters = re.findall(RE_team_starters, starts_data[1])
                second_team_bench = re.findall(RE_team_bench, benchs_data[1])

            else:
                #{

                first_team_data = team_data[0]

                type_one_search = re.search(RE_type_one_search, first_team_data)
                type_two_search = re.search(RE_type_two_search, first_team_data)


                if type_one_search != None:
                    first_team_starters_List = re.findall(RE_type_one_team_starter_list, first_team_data)
                    first_team_bench_List = re.findall(RE_type_one_team_bench_list, first_team_data)

                    first_team_starters = re.findall(RE_team_starters, first_team_starters_List[0])
                    first_team_bench = re.findall(RE_team_bench, first_team_bench_List[0])

                elif type_two_search != None:
                    first_team_starters_List = re.findall(RE_type_two_team_starter_list, first_team_data)
                    first_team_bench_List = re.findall(RE_type_two_team_bench_list, first_team_data)

                    first_team_starters = re.findall(RE_team_starters1, first_team_starters_List[0])
                    first_team_bench = re.findall(RE_team_bench1, first_team_bench_List[0])

                    tempTeamList = []
                    tempTeamList2 = []
                    for p in first_team_starters:
                        tempTeamList = []
                        for o in range(len(p)):
                            if o != 10:
                                tempTeamList.append(p[o])
                        tempTeamList2.append(tuple(tempTeamList))

                    first_team_starters = tempTeamList2

                    tempTeamList = []
                    tempTeamList2 = []
                    for p in first_team_bench:
                        tempTeamList = []
                        for o in range(len(p)):
                            if o != 10:
                                tempTeamList.append(p[o])
                        tempTeamList2.append(tuple(tempTeamList))

                    first_team_bench = tempTeamList2

                else:
                    print("Fatal Error of the type of Data!")

    #       <------------------------------------------------------------------------------------------------------------------------------------------------->

                #Second Team Data Here!
                second_team_data = team_data[1]
            
                type_one_search = re.search(RE_type_one_search, second_team_data)
                type_two_search = re.search(RE_type_two_search, second_team_data)
            

                if type_one_search != None:
                    second_team_starters_List = re.findall(RE_type_one_team_starter_list, second_team_data)
                    second_team_bench_List = re.findall(RE_type_one_team_bench_list, second_team_data)

                    second_team_starters = re.findall(RE_team_starters, second_team_starters_List[0])
                    second_team_bench = re.findall(RE_team_bench, second_team_bench_List[0])

                elif type_two_search != None:
                    second_team_starters_List = re.findall(RE_type_two_team_starter_list, second_team_data)
                    second_team_bench_List = re.findall(RE_type_two_team_bench_list, second_team_data)

                    second_team_starters = re.findall(RE_team_starters1, second_team_starters_List[0])
                    second_team_bench = re.findall(RE_team_bench1, second_team_bench_List[0])

                    tempTeamList = []
                    tempTeamList2 = []
                    for p in second_team_starters:
                        tempTeamList = []
                        for o in range(len(p)):
                            if o != 10:
                                tempTeamList.append(p[o])
                        tempTeamList2.append(tuple(tempTeamList))

                    second_team_starters = tempTeamList2

                    tempTeamList = []
                    tempTeamList2 = []
                    for p in second_team_bench:
                        tempTeamList = []
                        for o in range(len(p)):
                            if o != 10:
                                tempTeamList.append(p[o])
                        tempTeamList2.append(tuple(tempTeamList))

                    second_team_bench = tempTeamList2

                else:
                    print("Fatal Error of the type of Data!")

        #New experimental code
#       <------------------------------------------------------------------------------------------------------------------------------------------------->

                for p in first_team_starters[0]:
                    check_this_string_one = re.search('<', p)
                    check_this_string_two = re.search('>', p)

                    if check_this_string_one != None or check_this_string_two != None:

                        if type_one_search != None:
                            first_team_starters_List = re.findall(RE_type_one_team_starter_list, first_team_data)
                            first_team_bench_List = re.findall(RE_type_one_team_bench_list, first_team_data)

                            first_team_starters = re.findall(RE_team_starters2, first_team_starters_List[0])
                            first_team_bench = re.findall(RE_team_bench2, first_team_bench_List[0])

                        elif type_two_search != None:
                            first_team_starters_List = re.findall(RE_type_two_team_starter_list, first_team_data)
                            first_team_bench_List = re.findall(RE_type_two_team_bench_list, first_team_data)

                            first_team_starters = re.findall(RE_team_starters2, first_team_starters_List[0])
                            first_team_bench = re.findall(RE_team_bench2, first_team_bench_List[0])

                        else:
                            print("Fatal Error of the type of Data!")


                        if type_one_search != None:
                            second_team_starters_List = re.findall(RE_type_one_team_starter_list, second_team_data)
                            second_team_bench_List = re.findall(RE_type_one_team_bench_list, second_team_data)

                            second_team_starters = re.findall(RE_team_starters2, second_team_starters_List[0])
                            second_team_bench = re.findall(RE_team_bench2, second_team_bench_List[0])

                        elif type_two_search != None:
                            second_team_starters_List = re.findall(RE_type_two_team_starter_list, second_team_data)
                            second_team_bench_List = re.findall(RE_type_two_team_bench_list, second_team_data)
                            
                            second_team_starters = re.findall(RE_team_starters2, second_team_starters_List[0])
                            second_team_bench = re.findall(RE_team_bench2, second_team_bench_List[0])

                        else:
                            print("Fatal Error of the type of Data!")

                        noMins = True
                        break
            
            #End the Else Here
            #} 
#       <------------------------------------------------------------------------------------------------------------------------------------------------->
            #Main_player_list

            Main_player_list = []

            if len(game_time_location) == 0:
                game_time_location.append("")
            if len(officals) == 0:
                officals.append("")
            if len(attendence) == 0:
                attendence.append("")
            else:
                temp_string = ''
                for z in range(len(attendence[0])):
                    if attendence[0][z] == ',':
                        pass
                    else:
                        temp_string = temp_string + str(attendence[0][z])

                attendence[0] = str(temp_string)

            if noMins == True:
                tempTupleList = []
                for j in first_team_starters:
                    tempTupleList.append(j[:2]+('',)+j[2:])
                first_team_starters = tempTupleList

                tempTupleList = []        
                for j in first_team_bench:
                    tempTupleList.append(j[:2]+('',)+j[2:])
                first_team_bench = tempTupleList

                tempTupleList = []
                for j in second_team_starters:
                    tempTupleList.append(j[:2]+('',)+j[2:])
                second_team_starters = tempTupleList

                tempTupleList = []        
                for j in second_team_bench:
                    tempTupleList.append(j[:2]+('',)+j[2:])
                second_team_bench = tempTupleList



            for j in first_team_starters:
                temp_string = ""
                for k in range(len(j)):
                    if k == 2:
                        temp_string = temp_string + "Starter,"

                    if k == len(j) - 1:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ""
                        else:
                            temp_string = temp_string + j[k]
                    else:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ","
                        else:
                            temp_string = temp_string + j[k] + ","

                temp_string = temp_string + "," + first_team + "," + second_team + "," + game_time_location[0] + "," + first_team_away + "," + first_team_won + "," + officals[0] + "," + attendence[0] + "\n"
                Main_player_list.append(temp_string)


            for j in first_team_bench:
                temp_string = ""
                for k in range(len(j)):
                    if k == 2:
                        temp_string = temp_string + "Bench,"

                    if k == len(j) - 1:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ""
                        else:
                            temp_string = temp_string + j[k]
                    else:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ","
                        else:
                            temp_string = temp_string + j[k] + ","

                temp_string = temp_string + "," + first_team + "," + second_team + "," + game_time_location[0] + "," + first_team_away + "," + first_team_won + "," + officals[0] + "," + attendence[0] + "\n"
                Main_player_list.append(temp_string)


            for j in second_team_starters:
                temp_string = ""
                for k in range(len(j)):
                    if k == 2:
                        temp_string = temp_string + "Starter,"

                    if k == len(j) - 1:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ""
                        else:
                            temp_string = temp_string + j[k]
                    else:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ","
                        else:
                            temp_string = temp_string + j[k] + ","


                temp_string = temp_string + "," + second_team + "," + first_team + "," + game_time_location[0] + "," + second_team_home + "," + second_team_won + "," + officals[0] + "," + attendence[0] + "\n"
                Main_player_list.append(temp_string)


            for j in second_team_bench:
                temp_string = ""
                for k in range(len(j)):
                    if k == 2:
                        temp_string = temp_string + "Bench,"

                    if k == len(j) - 1:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ""
                        else:
                            temp_string = temp_string + j[k]
                    else:
                        if j[k] == "" or j[k] == " ":
                            temp_string = temp_string + ","
                        else:
                            temp_string = temp_string + j[k] + ","


                
                temp_string = temp_string + "," + second_team + "," + first_team + "," + game_time_location[0] + "," + second_team_home + "," + second_team_won + "," + officals[0] + "," + attendence[0] + "\n"
                Main_player_list.append(temp_string)


            numDone += 1
            print('Done',numDone, end=" ")
            print('out of', len(fileList))



            os.chdir(topdeck_dir)

            #textfile = open("raw_data_past_games_individual.txt", 'w')

            temp_string = "Player\tPosition\tStart\tMinutes\tFGM\tFGA\t3PM\t3PA\tFTM\tFTA\tOREB\tREB\tAST\tSTL\tBLK\tTO\tPF\tPTs\tTeam\tOpponent\tDate\tHome/Away\tWin/Loss\tOfficials\tAttendance\n"

            #textfile.write(temp_string)

            #for p in Main_player_list:
            #    textfile.write(p)

            #skip_bool to check for correct lines
            for p in Main_player_list:
                check_this_string_one = re.search('<', p)
                check_this_string_two = re.search('>', p)

                if check_this_string_one != None or check_this_string_two != None:
                    skip_bool = True

            
            if not skip_bool:
                with open("raw_data_past_games_individual_testFINAL5.txt", "a") as myfile:
                    for p in Main_player_list:
                        myfile.write(p)

                #textfile.close()

                runningTotal = runningTotal + len(Main_player_list)

                totalNum = open("numberOfLines.txt", 'w')
                totalNum.write(str(runningTotal))
                totalNum.close()

                #Rename file with a different directory. Moving files. Cannot move across drives.
                #shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo") #to move across drives/disks
                os.rename(NewDirectoryName + i, altDirectoryName + i)


            else:
                skip_bool = False
                print("Something went wrong with forming the string. It was not correct.")
                print(i, " is not formated correctly")
                file_error_list.append(i)
            
            

            #pass

    os.chdir(topdeck_dir)

    #textfile = open("raw_data_past_games_individual.txt", 'w')

    #temp_string = "Player\tPosition\tStart\tMinutes\tFGM\tFGA\t3PM\t3PA\tFTM\tFTA\tOREB\tREB\tAST\tSTL\tBLK\tTO\tPF\tPTs\tTeam\tOpponent\tDate\tHome/Away\tWin/Loss\tOfficials\tAttendance\n"

    #textfile.write(temp_string)

    #for i in Main_player_list:
    #    textfile.write(i)

    #textfile.close()

    error_textfile = open("file_error_list.txt", 'w')

    for i in file_error_list:
        error_textfile.write(i + '\n')

    error_textfile.close()


main()
