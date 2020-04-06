from tkinter import *
from tkinter import ttk
import threading
import sys
import datetime
import script
import os
import requests
import webbrowser

class MainWindow():

	def __init__(self, window, frame):

		self.window = window
		self.frame = frame

		if window == None:

			self.window = Tk()
			self.window.minsize(250, 175)
			self.window.iconbitmap("./media/favicon.ico")
			self.window.title("AwesomeTracker")

		else:

			self.window.minsize(250, 175)
			self.window.iconbitmap("./media/favicon.ico")
			self.window.title("AwesomeTracker")

		if frame == None:

			self.frame = Frame(self.window, bg = "yellow")
			self.frame.pack(fill = BOTH, expand = 1)
			
		else:

			self.frame.pack_forget()
			self.frame = Frame(self.window)
			self.frame.pack(fill = BOTH, expand = 1)

		# preparamos el label de bienvenida
		self.greetingsLabel = Label(self.frame, text = "Welcome to AwesomeTracker", bg = "green", relief = "solid", font = ("arial", 12, "bold"))
		self.greetingsLabel.pack(fill = "x")

		# preparamos el label de bienvenida
		self.versionLabel = Label(self.frame, text = "Version - V 0.1 \n\r Version notes: \n\r    -Performance improvements\n\r", relief = "solid", font = ("arial", 12, "bold"))
		self.versionLabel.pack(fill = BOTH, expand = 1)

		# preparamos el boton para continuar al inicio de sesion
		self.nextButton = Button(self.frame, text = "Next ->",bg = "blue", font = ("arial", 12, "bold"), command = lambda: self.checkCon())
		self.nextButton.pack(fill = "x")

		self.window.mainloop()

	def checkCon(self):

		hostname = "awesometracker.ddns.net"

		param = '-n' if sys.platform in ['Windows', 'win32'] else '-c'
		command = ['ping', param, 1, hostname]
		response = os.system(' '.join(str(e) for e in command))

		if response == 0:

			LoginWindow(self.window, self.frame)

		else:

			self.internetProblem = Label(self.frame, text = "Conection error", bg = "red", relief = "solid", font = ("arial", 12, "bold"))
			self.internetProblem.pack(fill = "x")

class LoginWindow():

	def __init__(self, window, frame):

		self.window = window
		self.frame = frame

		if self.window == None:

			self.window = Tk()
			self.window.geometry("350x200")
			self.window.minsize(350, 200)
			self.window.iconbitmap("media/favicon.ico")
			self. window.title("AwesomeTracker")

		else:

			self.window.minsize(350, 200)
			self.window.iconbitmap("media/favicon.ico")
			self.window.title("AwesomeTracker")

		if self.frame == None:

			self.frame = Frame(self.window, bg="lightblue", height = self.window.winfo_height(), width = self.window.winfo_width())
			self.frame.pack(fill = BOTH, expand = 1)

		else:
			
			self.frame.pack_forget()
			self.frame = Frame(self.window, bg = "lightblue", height = self.window.winfo_height(), width = self.window.winfo_width())
			self.frame.pack(fill = BOTH, expand = 1)

			self.frame.columnconfigure(0, weight = 1)
			self.frame.columnconfigure(1, weight = 1)

			self.frame.rowconfigure(0, weight=1)
			self.frame.rowconfigure(1, weight = 1)
			self.frame.rowconfigure(2, weight = 1)
			self.frame.rowconfigure(3, weight = 1)
			self.frame.rowconfigure(4, weight = 0)
			self.frame.rowconfigure(5, weight=0)
			self.frame.rowconfigure(6, weight = 1)

		# preparamos el label
		self.greetingsLabel = Label(self.frame, text = "Log in", bg = "green", relief = "solid", font = ("arial", 12, "bold"))
		self.greetingsLabel.grid(row = 0, column = 0, columnspan = 2,  sticky = N + S + E + W)

		# preparamos los campos para el incio de sesion

		self.userLabel = Label(self.frame, text = "Email or user", bg = "green", relief = "solid", font = ("arial", 12, "bold"))
		self.userLabel.grid(row = 1, column = 0, sticky = N + S + E + W)

		self.userInput = ttk.Entry(self.frame)
		self.userInput.grid(row = 1, column = 1,  sticky = N + S + E + W)

		self.passwordLabel = Label(self.frame, text = "Password", bg = "green", relief = "solid", font = ("arial", 12, "bold"))
		self.passwordLabel.grid(row = 2, column = 0, sticky = N + S + E + W)

		self.passwordInput = ttk.Entry(self.frame, show="*")
		self.passwordInput.grid(row = 2, column = 1, sticky = N + S + E + W)

		self.loginButton = Button(self.frame, text = "start sesion",bg = "blue", font = ("arial", 12, "bold"), command = lambda: self.sessionButton(self.userInput.get(), self.passwordInput.get()))
		self.loginButton.grid(row = 3, column = 0, columnspan = 2, sticky = N + S + E + W);

		self.beforeButton = Button(self.frame, text = "<- Back",bg = "blue", font = ("arial", 12, "bold"), command = lambda: MainWindow(self.window, self.frame))
		self.beforeButton.grid(row = 6, column = 0, columnspan = 2, sticky = N + S + E + W);

	def sessionButton(self, user, password):

		url = "http://awesometracker.ddns.net/access/"
		data = {

			'user': user,
			'password': password

		}
		r = requests.post(url = url, data = data)
		result = r.json()

		if (result and result['status'] and result['status'] == 'ok'):

			TrackerWindow(self.window, self.frame, result['data'])

		else:

			self.clean(self.userInput, self.passwordInput)

			self.errorLabel1 = Label(self.frame, text="User or password invalid", bg="red", relief="solid", font=("arial", 12, "bold"))
			self.errorLabel1.grid(row = 4, column = 0, columnspan = 2, sticky = N + S + E + W)

			self.errorLabel2 = Button(self.frame, text="Forgot password", bg="red", relief="solid", font=("arial", 12, "bold"), command = lambda: webbrowser.open('http://awesometracker.ddns.net/forgotPassword', new=2))
			self.errorLabel2.grid(row = 5, column = 0, columnspan = 2, sticky = N + S + E + W)


	def clean(self, *campos):

		for campo in campos:

			campo.delete(0, "end")


class TrackerWindow:

	def __init__(self, window, frame, user):

		self.window = window
		self.frame = frame

		self.script = 0
		self.thread = 0

		if self.window == None:

			self.window = Tk()
			self.window.geometry("1000x750")
			self.window.minsize(750, 600)
			self.window.iconbitmap("media/favicon.ico")
			self.window.title("AwesomeTracker")

		else:

			self.window.minsize(750, 600)
			self.window.iconbitmap("media/favicon.ico")
			self.window.title("AwesomeTracker")

		if self.frame == None:

			self.frame = Frame(self.window, bg="yellow")
			self.frame.pack(fill = BOTH, expand = 1)

		else:

			self.frame.pack_forget()
			self.frame = Frame(self.window, bg="yellow")
			self.frame.pack(fill = BOTH, expand = 1)

		self.generalFrame = Frame(self.frame, bg="blue")
		self.generalFrame.pack(fill=X, anchor=N)

		self.menuFrame = Frame(self.frame, bg="gray")
		self.menuFrame.pack(fill=Y, side=LEFT, anchor=N + W)

		self.contentFrame = Frame(self.frame, bg="white")
		self.contentFrame.pack(fill=BOTH, anchor=CENTER, expand=1)

		# preparamos el label de la barra principal
		self.mainLabel = Label(self.generalFrame, text="User: " + str(user['user']) + " | User code: " + str(user['code']), bg="green", relief="solid", font=("arial", 12, "bold"))
		self.mainLabel.pack(fill=BOTH, anchor=CENTER, expand=1)

		# preparamos las opciones del menu lateral
		self.optionsLabel = Label(self.menuFrame, text="Options", bg="green", relief="solid", font=("arial", 12, "bold"))
		self.optionsLabel.grid(row=0, column=0, sticky=N + S + E + W)

		self.optionsButton = Button(self.menuFrame, text="Actions", bg = "blue", font = ("arial", 12, "bold"), command = lambda: self.changeFrame("options", user))
		self.optionsButton.grid(row=1, column=0, sticky=N + S + E + W)

		self.logOutButton = Button(self.menuFrame, text = "Log out", bg = "blue", font = ("arial", 12, "bold"), command = lambda: self.logOut())
		self.logOutButton.grid(row=2, column=0, sticky=N + S + E + W)

	def changeFrame(self, option, user,):

		if (option == "options"):

			self.contentFrame.pack_forget()
			self.contentFrame = Frame(self.frame, bg="white")
			self.contentFrame.pack(fill = BOTH, anchor = CENTER, expand = 1)

			appLabel = Label(self.contentFrame, text="Actual window: No one", bg = "green", relief="solid", font=("arial", 12, "bold"))
			appLabel.pack(fill = BOTH, anchor = CENTER, expand = 1)

			lastAppLabel = Label(self.contentFrame, text="Last window: No one", bg="green", relief="solid", font=("arial", 12, "bold"))
			lastAppLabel.pack(fill = BOTH, anchor = CENTER, expand = 1)

			startButton = Button(self.contentFrame, text="Start Tracker", bg="blue", font=("arial", 12, "bold"), command=lambda: self.start(user))
			startButton.pack(fill = BOTH, anchor=CENTER, expand = 1)

			stopButton = Button(self.contentFrame, text="Stop Tracker", bg="blue", font=("arial", 12, "bold"), command=lambda: self.stop())
			stopButton.pack(fill = BOTH, anchor = CENTER, expand = 1)

			statusLabel = Label(self.contentFrame, text="Tracker status: Stopped", bg="green", relief="solid", font=("arial", 12, "bold"))
			statusLabel.pack(fill = BOTH, anchor = CENTER, expand = 1)

	def start(self, user):

		if self.script == 0:

			self.script = script.Script(user, self.contentFrame)
			self.thread = threading.Thread(target = self.script.start)
			self.thread.start()

	def stop(self):

		if self.script != 0:

			self.script.stop()
			self.thread.join()
			self.script = 0
			self.thread = 0

	def logOut(self):

		self.stop()
		LoginWindow(self.window, self.frame)

if __name__ == '__main__':
	MainWindow(None , None)