# GerritExtract

Originally Written By "Sriharsha Allenki".

This script is written for extracting the kernel code differences and various upgrades. the extract.py will be collecting all the gerrit diffs and list them by kernels for compare. The output will be in a csv format.

Following are the necessary packages:
NOTE: recommended to use vertual environment in linux
* Python 3.5
* pandas
* request

virtualenv venv1 --python=python3.5
cd venv1/
source bin/activate
pip install requests
pip install pandas
chmod 777 extract.py


COMMAND:
python extract.py -u username -p password from gerrit -f "driver location" -p1 "kernel/msm-5.4:msm-5.4" -p2 "kernel/msm-5.10:msm-5.10"

password here is http_gerrit password generated from gerrit settings

example
python extract.py -u ugoswami -p ***** -f "drivers/usb/dwc3/*" -p1 "kernel/msm-5.4:msm-5.4" -p2 "kernel/msm-5.10:msm-5.10"
