from ec2_sftp import SSHClientManager

def main():
    ssh_manager = SSHClientManager()

    ssh_manager.connect()

    local_path = r"C:\Users\l\OneDrive\Desktop\Python_datascience\OOPS\Solid_principle_interface_segaragation.py"
    remote_path = r"\home\ec2-user\Solid_principle_interface_segaragation.py"

    # ssh_manager.upload_file(local_path, remote_path)
    # ssh_manager.download_file(remote_path, local_path)
    # ssh_manager.upload_folder(r"C:\Users\l\OneDrive\Desktop\Python_datascience\OOPS",r"/home/ec2-user/OOPS_EC2")
    ssh_manager.download_folder(r"/home/ec2-user/OOPS_EC2",r"C:\Users\l\OneDrive\Desktop\Python_datascience")

    ssh_manager.close()

if __name__ == "__main__":
    main()
