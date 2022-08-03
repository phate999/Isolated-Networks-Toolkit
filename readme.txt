The Cradlepoint Isolated Networks Toolkit is designed to provide a web interface
for pushing license files and NCOS (firmware) files to Cradlepoint routers.

It runs a web interface on http://localhost:9000

You will need a .csv file of routers with 3 columns: IP address, username, password.
Header line is optional.
Default admin port is 8080.  If you use a different port, specify it in the IP address.
Example: 10.0.0.47:80

You will need a license file to license routers.  Contact servicessupport@cradlepoint.com for assistance.

You will need to download the NCOS file to upgrade your NCOS (firmware).  
To download NCOS, use the included "get_fw.py" script - enter your API keys at the top and run it.

Uploaded License Files are saved in the licenses/ folder
Uploaded NCOS Files are saved in the NCOS/ folder
Logs are saved in the logs/ folder.

aterrell@cradlepoint.com

