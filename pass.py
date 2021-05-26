from flask import Flask
import subprocess
from flask import jsonify

app = Flask(__name__)
output = [];

@app.route("/")
def hello():
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    f=open("log.txt", "w+")

    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
        
                f.write("Password for {} is {}\r\n".format(i, results[0])) 
                output.append("{} is {}".format(i, results[0]))               
            
            except IndexError:                
                print ("{:<30}|  {:<}".format(i, ""))
                
        except subprocess.CalledProcessError:
            print ("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
    return jsonify(output)

if __name__ == "__main__":
    app.run()