from flask import Flask, request, render_template
import os, subprocess
from funcHelper import FuncHelper


app = Flask(__name__)
fhp = FuncHelper()
path = '"C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage"'


@app.route("/")
def begin():
	exe = path + ' list -l vms'
	proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	string = out.decode("utf-8")

	fhp.stringToDictList(string)
	myList = fhp.getListDict()

	return render_template("index.html", myList=myList)

@app.route("/create", methods=["POST"])
def create():
	if request.method == "POST":
		name = request.form.get("name")
		memorySize = request.form.get("memorysize")
		numbercpus = request.form.get("numbercpus")
		system = request.form.get("guestos")
		ip = request.form.get("ip")

		local = os.getcwd() + os.sep + system 
		comm = ' import "%s" --vsys 0 --vmname "%s" --memory %d --cpus %d'%(local, name, int(memorySize), int(numbercpus))
		exe = path + comm
		proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()

		addDhcpServer(ip, name)

		return render_template("update.html")


@app.route("/modifymachine", methods=["POST"])
def modifyMachine():
	if request.method == "POST":
		name = request.form.get("name")
		memorySize = request.form.get("memorysize")
		numbercpus = request.form.get("numbercpus")

		if memorySize != "":
			modifyMem(name, memorySize)			
		if numbercpus != "":
			modifyCpu(name, numbercpus)

	return render_template("update.html")

@app.route("/modifyname")
def modifyName(name, newname):
	comm = ' modifyvm "%s" --name %s'%(name, newname)
	exe = path + comm
	proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()  

@app.route("/modifymem")
def modifyMem(name, valorMem):
	comm = ' modifyvm "%s" --memory %d'%(name, int(valorMem))
	exe = path + comm
	proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()  

@app.route("/modifycpu")
def modifyCpu(name, valorCPUs):
	comm = ' modifyvm "%s" --cpus %d'%(name, int(valorCPUs))
	exe = path + comm
	proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()  

@app.route("/startvm", methods=["POST"])
def startvm():
	if request.method == "POST":
		name = request.form.get("name")
		exe = path + ' startvm + %s'%(name)
		proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate() 

	return render_template("update.html")

def addDhcpServer(ip, nome):
	addDhcp = '  modifyvm "%s" --natpf1 "guestssh,tcp,,2222,%s,22"'%(nome,ip)
	exe = path + addDhcp
	proc = subprocess.Popen(exe, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()


if __name__ == '__main__':
	app.run(debug=True)


	#192.168.10.1
	#192.168.56.1