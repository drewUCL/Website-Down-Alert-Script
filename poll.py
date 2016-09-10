import smtplib
import urllib
import time
import yaml

from email.mime.text import MIMEText

class PollNameCoin( object ):
	'''
	A class to poll a site that is down
	and email the user once the site is back up
	and running
	'''
	def __init__( self, website, to_address, subject ):
		self.website = website
		self.to_address = to_address
		self.config_file = yaml.load(open("config.yaml"))
		self.subject = subject
		self.SMTP_USERNAME, self.SMTP_PASSWORD, self.EMAIL_FROM = None,None,None
		self.SMTP_SERVER, self.SMTP_PORT, self.MESSAGE = None,None,None
		
	def checkSite( self ):
		try:
			status =  urllib.urlopen(self.website).getcode()
			return True 
		except:
			return False
			
	def loadServerConfig( self ):
		self.SMTP_USERNAME = self.config_file["root"][0]
		self.SMTP_PASSWORD = self.config_file["root"][1]
		self.EMAIL_FROM = self.config_file["root"][2]
		self.SMTP_SERVER = self.config_file["root"][3]
		self.SMTP_PORT = self.config_file["root"][4]
		self.MASSAGE = self.config_file["root"][5]
		print self.config_file
		
	def emailSuccess( self ):
		self.loadServerConfig()
		co_msg = "NAMECOIN site is now up running a 200 status."
		msg = MIMEText(self.MASSAGE)
		msg['Subject'] = self.subject
		msg['To'], msg['From'] = self.to_address, self.EMAIL_FROM 
		mail = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
		mail.starttls()
		mail.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
		mail.sendmail(self.EMAIL_FROM, self.to_address, msg.as_string())
		mail.quit()
		
	def continuousPolling( self ):
		siteDown = True	
		while siteDown:
			time.sleep(5)
			print "[INFO] Checking sites status"
			if self.checkSite():
				print "[INFO] Site up again"
				siteDown = False
				print "[INFO] Send alert"
				self.emailSuccess()
				break
		
		
def main():
	#website = "https://www.google.co.uk/"
	website = "https://www.namecoin.org/"
	to_address = "drewmann47@yahoo.co.uk"
	subject = "NAMECOIN STATUS"
	siteCheck = PollNameCoin( website, to_address, subject )
	siteCheck.continuousPolling()
	print "\n[INFO] Completed"
	
	
if __name__ == "__main__":
	main()

	

	
'''
misc debug:
----------------------------------------------
debuglevel = True
mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
mail.set_debuglevel(debuglevel)
'''