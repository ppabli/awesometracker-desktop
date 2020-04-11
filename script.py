# imports generales
import json
import datetime
import time
import sys
import requests

if sys.platform in ['Windows', 'win32']:

	from win32 import win32gui

else:

	from AppKit import NSWorkspace

# inicializacion de la clase
class Script:

	def __init__(self, user, frame):

		self.frame = frame

		self.actualWindowName = ''
		self.startDate = None
		self.endDate = None

		self.user = user

		self.status = "Stopped"
		self.stopFlag = False

	def start(self):

		self.status = "Active"
		self.frame.winfo_children()[4]['text'] = 'Tracker status: ' + self.status
		self.script()

	def stop(self):

		self.status = "Stopped"
		self.frame.winfo_children()[4]['text'] = 'Tracker status: ' + self.status
		self.frame.winfo_children()[0]['text'] = 'Actual window: No one'
		self.frame.winfo_children()[1]['text'] = "Last window: " + self.actualWindowName
		self.stopFlag = True

	def script(self):

		try:

			while not self.stopFlag:

				self.frame.winfo_children()[0]['text'] = 'Actual window: ' + self.actualWindowName

				# revisa que sistema operativo esta usando el script para seleccionar correctamente el nombre de la aplicacion
				if sys.platform in ['darwin']:

					newWindowName = str(NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])

				else:

					window = win32gui.GetForegroundWindow()
					newWindowName = str(win32gui.GetWindowText(window)).split('-')[-1].strip()

				if self.actualWindowName != newWindowName:

					if self.actualWindowName != "":

						self.endDate = datetime.datetime.now()

						dif = self.endDate - self.startDate

						seconds = dif.seconds

						if seconds >= self.user['diff']:

							url = "http://awesometracker.ddns.net/addLog"
							data = {'userCode': self.user['code'], 'trackerLogs.app': str(self.actualWindowName), 'trackerLogs.start': str(self.startDate), 'trackerLogs.stop': str(self.endDate)}
							r = requests.post(url = url, data = data)

						self.frame.winfo_children()[1]['text'] = "Last window: " + self.actualWindowName + " - Time: " + str(seconds)

					self.actualWindowName = newWindowName

					self.startDate = datetime.datetime.now()

				time.sleep(.35)

			self.endDate = datetime.datetime.now()

			dif = self.endDate - self.startDate

			seconds = dif.seconds

			if seconds >= self.user['diff']:

				url = "http://awesometracker.ddns.net/addLog"
				data = {'userCode': self.user['code'], 'trackerLogs.app': str(self.actualWindowName), 'trackerLogs.start': str(self.startDate), 'trackerLogs.stop': str(self.endDate)}
				r = requests.post(url = url, data = data)

		except Exception as e:

			f = open('errors.log', 'a')
			f.write(str(datetime.datetime.now()) + str(e) + "\r\n")
			f.close()
			self.frame.winfo_children()[0]['text'] = "Error: " + str(e)