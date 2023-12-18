import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import shutil
import os
from tkinter import filedialog
from tkinter import simpledialog
import ldap3
import time
import pyotp
import qrcode
import datetime
import ssl
from ldap3 import Server, Connection, SUBTREE, ALL, NTLM


class FileManagerApp:
    directory_path = "/home/rgibs23/Classes/2362/PythonCode/userFiles"
    def __init__(self, master):
        self.master = master
        self.master.title("File Management System")

        # Simulated user data with permissions
        self.users = {
            "it1": {"permissions": ["upload", "download"]},
            "acc1": {"permissions": ["download", "delete"]},
            "admin": {"permissions": ["delete", "audit"]}
        }

        # Create and configure Listbox
        self.file_listbox = tk.Listbox(master, selectmode=tk.SINGLE, height=10, width=50)
        self.file_listbox.pack(pady=10)

        # GUI components
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(master, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Listbox to use the scrollbar
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        self.btn_upload = tk.Button(master, text="Upload", command=self.upload_file)
        self.btn_upload.pack(side=tk.LEFT, padx=5)

        self.btn_download = tk.Button(master, text="Download", command=self.download_file)
        self.btn_download.pack(side=tk.LEFT, padx=5)

        self.btn_delete = tk.Button(master, text="Delete", command=self.delete_file)
        self.btn_delete.pack(side=tk.LEFT, padx=5)

        self.btn_logout = tk.Button(master, text="Logout", command=self.logout)
        self.btn_logout.pack(side=tk.RIGHT, padx=5)

        # Simulated user login
        self.current_user = None
        self.login()


    def authenticate(self, username, password):
        server = ldap3.Server('ldap://172.17.0.1:389')
       # server = Server('ldaps://172.17.0.1:636', use_ssl=True, get_info=ALL, allowed_referral_hosts=[('*', True)])
        conn = ldap3.Connection(server, user = 'cn=IT-1,ou=IT,ou=Department,dc=hg,dc=local', password = password, auto_bind= True)
        conn.search('dc=hg,dc=local','(uid={})'.format(username), attributes=['uid'])

        if conn.entries:
            user_dn = conn.entries[0].entry_dn
            try:
                conn = ldap3.Connection(server, user=user_dn, password=password, auto_bind=True)
                #print(f"{user_dn}")
                if self.twoFactorAuth():
                    messagebox.showinfo("You have successfully logged on")
                    self.update_file_list()
                    return True
            except ldap3.core.exceptions.LDAPBindError:
                #print("Not Successful. Code Again")
                messagebox.showerror("You have not successfully logged on")
                return False
        else:
            #print("Nothing ran :(")
            messagebox.showerror("User not found")
            return False


    def authenticate2(self, username, password):
        server = ldap3.Server('ldap://172.17.0.1:389')
        conn = ldap3.Connection(server, user = 'cn=ACC-1,ou=ACC,ou=Department,dc=hg,dc=local', password = password, auto_bind= True)
        conn.search('dc=hg,dc=local','(uid={})'.format(username), attributes=['uid'])
        found = False

        while(found == False):
            conn.search('dc=hg,dc=local','(uid={})'.format(username), attributes=['uid'])
            if conn.entries:
                user_dn = conn.entries[0].entry_dn
                conn = ldap3.Connection(server, user = user_dn, password = password, auto_bind = True)
                if conn.bound and self.twoFactorAuth():
                    messagebox.showinfo("You have logged in")
                    found = True
                    self.update_file_list()
                    return True
                else:
                    messagebox.showinfo("Password not correct")
                    found = True
                    return False
            messagebox.showinfo("User not found")
            found = True
            return False


    def authenticate4(self, username, password):
        server = ldap3.Server('ldap://172.17.0.1:389')
        conn = ldap3.Connection(server, user = 'cn=ELIASBH,ou=ACC,ou=Department,dc=hg,dc=local', password = password, auto_bind= True)
        conn.search('dc=hg,dc=local','(uid={})'.format(username), attributes=['uid'])
        found = False

        while(found == False):
            conn.search('dc=hg,dc=local','(uid={})'.format(username), attributes=['uid'])
            if conn.entries:
                user_dn = conn.entries[0].entry_dn
                conn = ldap3.Connection(server, user = user_dn, password = password, auto_bind = True)
                if conn.bound and self.twoFactorAuth():
                    messagebox.showinfo("You have logged in")
                    found = True
                    self.update_file_list()
                    return True
                else:
                    messagebox.showinfo("Password not correct")
                    found = True
                    return False
            messagebox.showinfo("User not found")
            found = True
            return False



    def authenticate3(self, username, password):
        server = ldap3.Server('ldap://172.17.0.1:389')
        #server = Server('ldaps://172.17.0.1:636', use_ssl=True, get_info=ALL, allowed_referral_hosts=[('*', True)])
        conn = ldap3.Connection(server, user = 'cn=ADMIN,ou=Department,dc=hg,dc=local', password = password, auto_bind= True)
        conn.search('dc=hg,dc=local','(uid={})'.format(username), attributes=['uid'])

        if conn.entries:
            user_dn = conn.entries[0].entry_dn
            try:
                conn = ldap3.Connection(server, user=user_dn, password=password, auto_bind=True)
                #print(f"{user_dn}")
                if self.twoFactorAuth():
                    messagebox.showinfo("You have successfully logged on")
                    self.update_file_list()
                    return True
            except ldap3.core.exceptions.LDAPBindError:
                #print("Not Successful. Code Again")
                messagebox.showerror("You have not successfully logged on")
                return False
        else:
            #print("Nothing ran :(")
            messagebox.showerror("User not found")
            return False


    def twoFactorAuth(self):
        key = "GeeksforGeeksIsBestForEverything"

        uri = pyotp.totp.TOTP(key).provisioning_uri(
            name='Dwaipayan_Bandyopadhyay',
            issuer_name='GeeksforGeeks')
        # Qr code generation step
        qrcode.make(uri).save("qr.png")

        """Verifying stage starts"""

        totp = pyotp.TOTP(key)

        attempts_left = 3  # Number of attempts allowed
        while attempts_left > 0:
            code = simpledialog.askstring("Two-Factor Code", f"Enter code (Attempts left: {attempts_left}):")
            if totp.verify(code):
                return True
            else:
                messagebox.showinfo("Invalid Code", "Incorrect two-factor authentication code. Try again.")
                attempts_left -= 1

        messagebox.showinfo("Login Failed", "You have run out of attempts.")
        return False
                



    def login(self):
        username = simpledialog.askstring("Login", "Enter username:")
        password = simpledialog.askstring("Password", "Enter password:", show='*"')

        if username is not None and password is not None:
            if "it" in username:
                if self.authenticate(username, password):
                    self.current_user = username
                    self.update_file_list()
                    self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} logged in')
            elif "acc" in username:
                if self.authenticate2(username, password):
                    self.current_user = username
                    self.update_file_list()
                    self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} logged in')
            elif "admin" in username:
                if self.authenticate3(username, password):
                    self.current_user = username
                    if self.current_user == "admin":
                        self.btn_audit = tk.Button(self.master, text="Audit", command=self.view_audit)
                        self.btn_audit.pack(side=tk.LEFT, padx=5)

                        self.btn_view_server = tk.Button(self.master, text="View ServerFiles", command=self.view_server_files)
                        self.btn_view_server.pack(side=tk.LEFT, padx=5)
                        self.update_file_list()
                        self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} logged in')
            elif "elias" in username:
                if self.authenticate4(username, password):
                    self.current_user = username
                    self.update_file_list()
                    self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} logged in')
            else:
                messagebox.showerror("Error", "Invalid username or password")
                self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', 'User failed to authenticate')
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def logout(self):
        self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} logged out')
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out")

        # Clear existing buttons and file list
        self.clear_buttons()
        self.clear_file_list()

        self.login()

    def append_text_to_file(self, file_path, text):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line_to_write = f'{timestamp} - {text}\n'

        with open(file_path, 'a') as file:
            file.write(line_to_write)

    def update_file_list(self):
        #self.listbox.delete(0, tk.END)
        #for file in self.files:
        #    if self.has_permission("download") or self.has_permission("delete"):
        #        self.listbox.insert(tk.END, file)
        
        # Specify the directory containing the files
        directory_path = "/home/rgibs23/Classes/2362/PythonCode/userFiles"

        # Clear existing items in the Listbox
        self.file_listbox.delete(0, tk.END)

        # Get the list of files in the directory
        files = os.listdir(directory_path)

        # Insert each file into the Listbox
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def clear_buttons(self):
        # Clear existing buttons
        if hasattr(self, 'btn_audit'):
            self.btn_audit.destroy()
        if hasattr(self, 'btn_view_server'):
            self.btn_view_server.destroy()


    def clear_file_list(self):
        # Clear existing items in the Listbox
        self.file_listbox.delete(0, tk.END)


    def view_directory_contents(self, title, directory_path):
        files = os.listdir(directory_path)
        contents = "\n".join(files)

        # Create a new window to display the directory contents
        directory_window = tk.Toplevel(self.master)
        directory_window.title(title)

        # Display the directory contents in a Text widget
        directory_text = tk.Text(directory_window, wrap=tk.WORD)
        directory_text.insert(tk.END, contents)
        directory_text.pack(padx=10, pady=10)


    def view_audit(self):
        audit_file_path = "/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt"
        if os.path.exists(audit_file_path):
            with open(audit_file_path, "r") as audit_file:
                audit_contents = audit_file.read()

            # Create a new window to display the audit contents
            audit_window = tk.Toplevel(self.master)
            audit_window.title("Audit Contents")

            # Display the audit contents in a Text widget
            audit_text = tk.Text(audit_window, wrap=tk.WORD)
            audit_text.insert(tk.END, audit_contents)
            audit_text.pack(padx=10, pady=10)
        else:
            messagebox.showinfo("Audit", "Audit file not found.")

    def view_server_files(self):
        server_files_path = "/home/rgibs23/Classes/2362/PythonCode/serverFiles"
        self.view_directory_contents("ServerFiles Contents", server_files_path)


    def has_permission(self, permission):
        return permission in self.users.get(self.current_user, {}).get("permissions", [])

    def download_file(self):
        if self.has_permission("download"):
            # Allow the user to select a file for download from the serverFiles directory
            file_path = filedialog.askopenfilename(initialdir="/home/rgibs23/Classes/2362/PythonCode/serverFiles", title="Select a file for download")

            # Specify the directory where the file should be downloaded
            download_directory = "/home/rgibs23/Classes/2362/PythonCode/userFiles"

            if file_path and file_path.startswith("/home/rgibs23/Classes/2362/PythonCode/serverFiles"):
                # Copy the file to the download directory
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(download_directory, file_name)
                shutil.copy(file_path, destination_path)
                messagebox.showinfo("Download", "File downloaded successfully")
                self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} downloaded {file_name}')

                # Refresh the Listbox to display the updated file list
                self.update_file_list()
            elif file_path:
                messagebox.showerror("Invalid Selection", "You can only download files from the serverFiles directory.")
        else:
            messagebox.showerror("Permission Denied", "You do not have permission to download")

    def upload_file(self):
        if self.has_permission("upload"):
            #selected_file = self.listbox.get(tk.ACTIVE)
            # Implement file download logic here
            #messagebox.showinfo("Download", f"File '{selected_file}' downloaded successfully")
            # Get the selected file from the Listbox
            # Prompt the user to select a file for upload
            file_to_upload = filedialog.askopenfilename(initialdir=self.directory_path, title="Select File to Upload")
            file_name = os.path.basename(file_to_upload)

            if file_to_upload:
                # Specify the destination directory where the file should be uploaded
                upload_directory = "/home/rgibs23/Classes/2362/PythonCode/serverFiles"

                # Copy the file to the upload directory
                destination_path = os.path.join(upload_directory, os.path.basename(file_to_upload))
                shutil.copy(file_to_upload, destination_path)
                messagebox.showinfo("Upload", f"File '{os.path.basename(file_to_upload)}' uploaded successfully")
                self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} uploaded {file_name} to the server')

                # Refresh the Listbox to display the updated file list
                self.update_file_list()
        else:
            messagebox.showerror("Permission Denied", "You do not have permission to upload")


    def delete_file(self):
        if self.has_permission("delete"):
            #selected_file = self.listbox.get(tk.ACTIVE)
            # Implement file delete logic here
            #messagebox.showinfo("Delete", f"File '{selected_file}' deleted successfully")
            # Get the selected file from the Listbox
            selected_file = self.file_listbox.get(tk.ACTIVE)

            if selected_file:
                # Specify the directory where the file is located
                file_path = os.path.join("/home/rgibs23/Classes/2362/PythonCode/userFiles", selected_file)

                # Delete the file
                os.remove(file_path)
                messagebox.showinfo("Delete", f"File '{selected_file}' deleted successfully")
                self.append_text_to_file('/home/rgibs23/Classes/2362/PythonCode/adminFiles/audit.txt', f'{self.current_user} deleted {selected_file}')

                # Refresh the Listbox to display the updated file list
                self.update_file_list()
        else:
            messagebox.showerror("Permission Denied", "You do not have permission to delete")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

