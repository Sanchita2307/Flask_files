import os
import paramiko
from paramiko import RSAKey
from config import HOSTNAME, USERNAME, KEY_PATH

class SSHClientManager:
    def __init__(self, hostname=HOSTNAME, username=USERNAME, key_path=KEY_PATH):
        self.hostname = hostname
        self.username = username
        self.key_path = key_path
        self.client = None
        self.sftp = None

    def load_private_key(self):
        # Paramiko supports PEM directly
        if self.key_path.endswith(".pem"):
            return paramiko.RSAKey.from_private_key_file(self.key_path)

        # If using a PPK file (Putty key), convert manually using puttygen OR use supported loader
        elif self.key_path.endswith(".ppk"):
            return paramiko.RSAKey.from_private_key_file(self.key_path)

        else:
            raise ValueError("Unsupported key format. Use PEM or PPK.")

    def connect(self):
        try:
            key = self.load_private_key()

            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=key,
                timeout=10
            )

            self.sftp = self.client.open_sftp()
            print("Connected successfully!")
        except Exception as e:
            print(f"Connection failed: {e}")
    
    def upload_file(self, local_path, remote_path):
        try:
            self.sftp.put(local_path, remote_path)
            print(f"Uploaded: {local_path} → {remote_path}")
        except Exception as e:
            print(f"Upload failed: {e}")

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        print("Connection closed.")

    def download_file(self, remote_path, local_path):
        try:
            self.sftp.get(remote_path, local_path)
            print(f"Downloaded: {remote_path} → {local_path}")
        except Exception as e:
            print(f"Download failed: {e}")
    
    def upload_folder(self, local_folder, remote_folder):
        """
        Uploads all files from a local folder to a remote folder (non-recursive folders ok).
        """
        try:
            # Make sure remote folder exists
            try:
                self.sftp.stat(remote_folder)
            except FileNotFoundError:
                self.sftp.mkdir(remote_folder)
                print(f"Created remote folder: {remote_folder}")
    
            # Upload files
            for root, dirs, files in os.walk(local_folder):
                for file in files:
                    local_file = os.path.join(root, file)
                    remote_file = f"{remote_folder}/{file}"
                    self.sftp.put(local_file, remote_file)
                    print(f"Uploaded: {local_file} → {remote_file}")
    
        except Exception as e:
            print(f"Upload folder failed: {e}")

    def download_folder(self, remote_folder, local_folder):
        """
        Recursively download a remote folder to a local folder.
        """
        import stat
        import os
    
        def _download_recursive(r_folder, l_folder):
            os.makedirs(l_folder, exist_ok=True)
            for item in self.sftp.listdir_attr(r_folder):
                remote_path = f"{r_folder}/{item.filename}"
                local_path = os.path.join(l_folder, item.filename)
    
                if stat.S_ISDIR(item.st_mode):
                    _download_recursive(remote_path, local_path)
                else:
                    self.sftp.get(remote_path, local_path)
                    print(f"Downloaded: {remote_path} → {local_path}")
    
        try:
            _download_recursive(remote_folder, local_folder)
            print(f"Folder downloaded successfully to {local_folder}")
        except Exception as e:
            print(f"Download folder failed: {e}")