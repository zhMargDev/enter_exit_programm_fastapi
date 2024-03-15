import subprocess

command = f"cd backup && sudo docker cp work_prog_container:/app/database.db . && cd ../ && sudo chmod 777 backup"

try:
    subprocess.run(command, shell=True, check=True)
    print("Command executed successfully!")
except subprocess.CalledProcessError as error:
    print(f"Command failed with error: {error}")