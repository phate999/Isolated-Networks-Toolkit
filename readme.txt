The Cradlepoint Isolated Networks Toolkit is designed to provide a web interface
for pushing license files, NCOS (firmware) files, and configuration files to Cradlepoint routers.

It runs a web interface on http://localhost:9000

You will need a .csv file of routers with 3 columns: IP address, username, password.
Header line is optional.
Default admin port is 8080.  If you use a different port, specify it in the IP address.
Example: 10.0.0.47:80

You will need a license file to license routers.  Contact servicessupport@cradlepoint.com for assistance.

To download NCOS, use the included "Download NCOS.py" script - enter your API keys at the top and run it.

Uploaded License Files are saved in the licenses/ folder
Uploaded NCOS Files are saved in the NCOS/ folder
Uploaded configs are saved in the configs/ folder.
Logs are saved in the logs/ folder.
