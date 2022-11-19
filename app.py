import shutil
import platform
import pyautogui
import os
from flask import*
from flask import render_template, redirect
import socket
import qrcode
import webbrowser

url="http://"+ socket.gethostbyname(socket.gethostname())+":5000"
img=qrcode.make("http://"+ socket.gethostbyname(socket.gethostname())+":5000")
img.save("qr.png")

print(socket.gethostbyname(socket.gethostname()))
app = Flask(__name__, template_folder="temp")
app.config["SERVER_NAME"] = socket.gethostbyname(socket.gethostname())+":5000"
webbrowser.open("http://"+ socket.gethostbyname(socket.gethostname())+":5000/qrcode")

@app.route("/")
def r0():
	if (platform.system() == 'Windows'):
		ptl="C:+"
	else:
		ptl="+root+home+"
	return render_template("a.html", url=url+"/file/"+ptl)

@app.route("/qrcode")
def r():
	return send_file("qr.png")

@app.route("/file/<path>")
def r1(path):
	file=path.replace("+","/")
	if (os.path.isdir(file) == True):
		return render_template("index.html", file=os.listdir(file), path=path, url=url+"/file/", back=url)
	else:
		return send_file(file)

@app.route("/delete/<path>")
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
def r4(command):
	os.system(command.replace("+"," "))
	return "Executed successfully"

@app.route("/screenshot")
def r5():
	pyautogui.screenshot("blank.png")
	return send_file("blank.png")

@app.route("/sendfile", methods=["POST"])
def r6():
	files = request.files.getlist("file[]")
	for file in files:
		print(file)
		file.save("file/"+file.filename)
	return redirect("/")

if __name__ == '__main__':
	app.run(host=socket.gethostbyname(socket.gethostname())+":5000")