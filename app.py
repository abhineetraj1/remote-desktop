import shutil
import platform
import pyautogui
import os
from flask import*
from flask import render_template, redirect
import socket
import qrcode
import webbrowser

#Getting the IP address of system over network
url="http://"+ socket.gethostbyname(socket.gethostname())+":5000"
img=qrcode.make("http://"+ socket.gethostbyname(socket.gethostname())+":5000")
img.save("qr.png")

print(socket.gethostbyname(socket.gethostname()))
app = Flask(__name__, template_folder="temp")
app.config["SERVER_NAME"] = socket.gethostbyname(socket.gethostname())+":5000"

#Openning the browser to show qrcode, through which user can connect the system
webbrowser.open("http://"+ socket.gethostbyname(socket.gethostname())+":5000/qrcode")

@app.route("/")
#This will list the directories in required folders
def r0():
	if (platform.system() == 'Windows'):
		ptl="C:+"
	else:
		ptl="+root+home+"
	return render_template("a.html", url=url+"/file/"+ptl)

@app.route("/qrcode")
#This will send the connect qrcode to user through browser
def r():
	return send_file("qr.png")

@app.route("/file/<path>")
#This function will send the file from the host to other connected devices
def r1(path):
	file=path.replace("+","/")
	if (os.path.isdir(file) == True):
		return render_template("index.html", file=os.listdir(file), path=path, url=url+"/file/", back=url)
	else:
		return send_file(file)

@app.route("/delete/<path>")
#This function will delete the file in the host from other connected devices
def r3(path):
	try:
		shutil.rmtree(path.replace("+","//"))
		return redirect("/delete/"+path)
	except Exception as ss:
		try:
			os.remove(path.replace("+","//"))
			return redirect("/delete/"+path)
		except Exception as ss:
			return "file not found"

@app.route("/cmd/<command>")
#This function will run Command Prompts commands in terminal of the hosted computer
def r4(command):
	os.system(command.replace("+"," "))
	return "Executed successfully"

@app.route("/screenshot")
#This will send the screenshot of the current screen to the connected client
def r5():
	pyautogui.screenshot("blank.png")
	return send_file("blank.png")

@app.route("/sendfile", methods=["POST"])
#This function will upload file from the connected client to hosted computer
def r6():
	files = request.files.getlist("file[]")
	for file in files:
		print(file)
		file.save("file/"+file.filename)
	return redirect("/")

if __name__ == '__main__':
	app.run(host=socket.gethostbyname(socket.gethostname())+":5000")
