# EC2 SSH Configuration

HOSTNAME = "ec2-16-171-160-211.eu-north-1.compute.amazonaws.com"   # Public DNS or IP
USERNAME = "ec2-user"          # ubuntu / centos / root depending on AMI

# Path to your private key (.pem or .ppk)
KEY_PATH = r"C:\Users\l\OneDrive\Desktop\Python_datascience\pem-key-for-paramiko.pem"    # or "my-key.ppk"

# Set True only if you are using a .ppk file
USE_PPK = False


# File paths for upload
LOCAL_FILE_PATH = r"C:\Users\l\OneDrive\Desktop\Python_datascience\pem-key-for-paramiko.pem"
REMOTE_FILE_PATH = "/home/ec2-user/test.txt"


# Optional: change SSH port (default is 22)
SSH_PORT = 22
