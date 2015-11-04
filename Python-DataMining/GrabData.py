import urllib.request
import os
import platform
import time
import re
import sys
import string
import html
import smtplib


#To get Unix and Windows
platformType = platform.system()

#	Format:
#
#
#

def main():

    master_link = "http://espn.go.com/mens-college-basketball/schedule?date="
    date_to_start_at = 2012
    month_to_start_at = 10
    day_to_start_at = 25
    secondary_link = ""

    thirty_day_list = [4, 6, 9, 11]
    thirtyone_day_list = [1, 3, 5, 7, 8, 10, 12]

    new_link = master_link + str(date_to_start_at) + str(month_to_start_at) + str(day_to_start_at)

    loop_variable = "15 4 2015"
    while_loop_variable = "25 10 2012"

    currentDirectory = os.getcwd()

    if platformType == 'Windows':
        MASTERdirectory = currentDirectory + "\\ESPN_HTML_Cache\\"
        directoryName = MASTERdirectory + "\\Day_Files\\"
        NewDirectoryName = MASTERdirectory + "\\Game_Files\\"

    else:
        MASTERdirectory = currentDirectory + "/ESPN_HTML_Cache/"
        directoryName = MASTERdirectory + "/Day_Files/"
        NewDirectoryName = MASTERdirectory + "/Game_Files/"
    
    try: 
        os.makedirs(directoryName)
    except OSError:                    
        if not os.path.isdir(directoryName):
            raise

    os.chdir(directoryName)

    fileList = os.listdir(directoryName)
    

    while (while_loop_variable != loop_variable):

        temp_var = while_loop_variable + ".HTML"
        
        if (temp_var) in fileList:
            #print("Skipped " + while_loop_variable)
            pass

        else:
            try:
                urllibHTML = urllib.request.urlopen(new_link).read()
                time.sleep(2)
            except:
                print('Request 1 Failed. Trying again in 30 seconds.')
                time.sleep(30)
                try:
                    urllibHTML = urllib.request.urlopen(new_link).read()
                    time.sleep(2)
                except:
                    print('Request 2 Failed. Trying again in 30 seconds.')
                    time.sleep(30)
                    try:
                        urllibHTML = urllib.request.urlopen(new_link).read()
                        time.sleep(2)
                    except:
                        print('Request 3 Failed. Trying again in 30 seconds.')
                        time.sleep(30)
                        try:
                            urllibHTML = urllib.request.urlopen(new_link).read()
                            time.sleep(2)
                        except:
                            print('Request 4 Failed. Trying again in 30 seconds.')
                            time.sleep(30)
                            try:
                                urllibHTML = urllib.request.urlopen(new_link).read()
                                time.sleep(2)
                            except:
                                print('Request 5 Failed. Program can\'t continue')
                                return -1


        if (while_loop_variable + ".HTML") in fileList:
            pass

        else:
            print("Saving " + while_loop_variable)
            textfile = open(while_loop_variable + '.HTML', 'wb')

            textfile.write(urllibHTML)

            textfile.close()


        






        
        
        if day_to_start_at == 28:
            if month_to_start_at == 2 and (date_to_start_at % 4 != 0):
                month_to_start_at += 1
                day_to_start_at = 0

        elif day_to_start_at == 29:
            if date_to_start_at % 4 == 0:
                if month_to_start_at == 2:
                    month_to_start_at += 1
                    day_to_start_at = 0

        elif day_to_start_at == 30:
            if month_to_start_at in thirty_day_list:
                month_to_start_at += 1
                day_to_start_at = 0

        elif day_to_start_at == 31:
            if month_to_start_at in thirtyone_day_list:
                month_to_start_at += 1
                day_to_start_at = 0

        #Skip from april to oct, not basketball during that time
        if day_to_start_at > 15 and month_to_start_at == 4:
            month_to_start_at = 10
            day_to_start_at = 25

        #increment year and reset month
        if month_to_start_at == 13:
            month_to_start_at = 1
            date_to_start_at += 1

        day_to_start_at += 1



        if month_to_start_at < 10:
            if day_to_start_at < 10:
                new_link = master_link + str(date_to_start_at) + "0" + str(month_to_start_at) + "0" + str(day_to_start_at)
            else:
                new_link = master_link + str(date_to_start_at) + "0" + str(month_to_start_at) + str(day_to_start_at)
        else:
            if day_to_start_at < 10:
                new_link = master_link + str(date_to_start_at) + str(month_to_start_at) + "0" + str(day_to_start_at)
            else:
                new_link = master_link + str(date_to_start_at) + str(month_to_start_at) + str(day_to_start_at)


        #print(str(day_to_start_at) + " " + str(month_to_start_at) + " " + str(date_to_start_at))
        #print(new_link)

        while_loop_variable = str(day_to_start_at) + " " + str(month_to_start_at) + " " + str(date_to_start_at)
        


            
    fileList = os.listdir(directoryName)

    list_of_urls = []
    list_of_game_ids = []

    for i in fileList:
        
        htmlfile = open(directoryName + i, 'rb')

        textfile = htmlfile.read()

        #href="(http://espn\.go\.com/ncb/boxscore\?id=(.*?))">Box Score

        box_scores_list = re.findall('href="http://espn\.go\.com/ncb/boxscore\?id=(.*?)">Box Score', str(textfile))

        for j in range(len(box_scores_list)):
            list_of_game_ids.append(box_scores_list[j])

        #print(box_scores_list)

    #Get rid of Dups in list_of_game_ids
    list_of_game_ids = list(set(list_of_game_ids))


    for i in range(len(list_of_game_ids)):
        list_of_urls.append('http://espn.go.com/ncb/boxscore?id=' + list_of_game_ids[i])

    #print(list_of_game_ids)

    try: 
        os.makedirs(NewDirectoryName)
    except OSError:                    
        if not os.path.isdir(NewDirectoryName):
            raise

    os.chdir(NewDirectoryName)  

    fileList = os.listdir(NewDirectoryName)

    for i in range(len(list_of_urls)):

        temp_var = list_of_game_ids[i] + ".HTML"

        if (temp_var) in fileList:
            #print("Skipped " + while_loop_variable)
            pass

        else:
            try:
                urllibHTML = urllib.request.urlopen(list_of_urls[i]).read()
                time.sleep(2)
            except:
                print('Request 1 Failed. Trying again in 30 seconds.')
                time.sleep(30)
                try:
                    urllibHTML = urllib.request.urlopen(list_of_urls[i]).read()
                    time.sleep(2)
                except:
                    print('Request 2 Failed. Trying again in 30 seconds.')
                    time.sleep(30)
                    try:
                        urllibHTML = urllib.request.urlopen(list_of_urls[i]).read()
                        time.sleep(2)
                    except:
                        print('Request 3 Failed. Trying again in 30 seconds.')
                        time.sleep(30)
                        try:
                            urllibHTML = urllib.request.urlopen(list_of_urls[i]).read()
                            time.sleep(2)
                        except:
                            print('Request 4 Failed. Trying again in 30 seconds.')
                            time.sleep(30)
                            try:
                                urllibHTML = urllib.request.urlopen(list_of_urls[i]).read()
                                time.sleep(2)
                            except:
                                print('Request 5 Failed. Program can\'t continue')
                                return -1


        if (temp_var) in fileList:
            pass

        else:
            print("Saving " + temp_var)
            textfile = open(temp_var, 'wb')

            textfile.write(urllibHTML)

            textfile.close()

main()
