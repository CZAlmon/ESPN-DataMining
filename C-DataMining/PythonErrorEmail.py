import keyring
import smtplib

def Main():
    #In the "From: " add the email address that is sending the email
    #In the "To: " add the email address(es) that the email is being sent to. Comma delimited
	msg = "\r\n".join([
		"From: ",
		"To: ",
		"Subject: NCAA stats update script has stopped",
		"",
		"The script has stopped running and needs to be restarted."
		])
		
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	
	
	server.login('', keyring.get_password('',''))
	  	#First '' is the email account, second '' is the name of the account in keyring, third '' is the email account in keyring
	
	server.sendmail("ukystatisticsbot@gmail.com", [''], msg)
	  	#The '' here is the recipent's email address(es). Must be comma delimited and all in thier own ''
	
	server.quit()

Main()
