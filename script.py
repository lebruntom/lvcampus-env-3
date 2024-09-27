import platform
import subprocess
import os
import time
from colorama import init, Fore, Style

# Initialisation colorama
init(autoreset=True)

# afficher des messages avec pauses
def display_message(message, color=Fore.WHITE, pause=2):
    print(color + message)
    time.sleep(pause)

# 1. Détecter l'OS
system = platform.system()
if system == "Linux":
    display_message("Vous êtes sur Linux.", Fore.GREEN)

    # Vérifie si l'utilisateur est root
    if os.geteuid() == 0:
        display_message("Vous êtes root.", Fore.GREEN)
    else:
        display_message("Vous n'êtes pas root.", Fore.RED)

    # Détection de la famille Linux
    with open("/etc/os-release", "r") as f:
        os_info = f.read()
    if "debian" in os_info.lower() or "ubuntu" in os_info.lower():
        linux_family = "debian"
        display_message("Famille Linux: Debian/Ubuntu", Fore.BLUE)
    elif "rhel" in os_info.lower() or "fedora" in os_info.lower():
        linux_family = "redhat"
        display_message("Famille Linux: RedHat/Fedora", Fore.BLUE)
    else:
        display_message("Famille Linux inconnue.", Fore.RED)
        exit()

elif system == "Windows":
    display_message("Vous êtes sur Windows.", Fore.GREEN)

else:
    display_message("Système d'exploitation non supporté.", Fore.RED)
    exit()

# 2. Vérifier si Docker est installé
def is_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# 3. Vérifier si VirtualBox est installé
def is_virtualbox_installed():
    try:
        subprocess.run(["C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# 4. Vérifier si le service Docker est actif
def is_docker_active():
    try:
        subprocess.run(["systemctl", "is-active", "--quiet", "docker"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# 5. Afficher les messages d'installation de Docker et VirtualBox
if is_docker_installed():
    display_message("Docker est installé.", Fore.GREEN)
else:
    display_message("Docker n'est pas installé. Téléchargez-le ici : https://docs.docker.com/get-docker/", Fore.RED)

if is_virtualbox_installed():
    display_message("VirtualBox est installé.", Fore.GREEN)
else:
    display_message("VirtualBox n'est pas installé. Téléchargez-le ici : https://www.virtualbox.org/wiki/Downloads", Fore.RED)

# 6. Assurer que le service Docker est actif
if system == "Linux":
    if not is_docker_active():
        display_message("Le service Docker est inactif. Démarrage...", Fore.YELLOW)
        subprocess.run(["systemctl", "start", "docker"], check=True)
        display_message("Service Docker démarré.", Fore.GREEN)

# 7. Création de VM avec VirtualBox
def create_vbox_vm(vm_name, iso_path, cpu=2, memory=4096, storage=60):
    try:
        # Créer une nouvelle VM
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "createvm", "--name", vm_name, "--ostype", "Linux", "--register"
        ], check=True)

        # Configurer la VM
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "modifyvm", vm_name, "--cpus", str(cpu), "--memory", str(memory),
            "--vram", "128", "--nic1", "nat"
        ], check=True)

        # Créer et attacher un disque dur virtuel
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "createhd", "--filename", f"{vm_name}.vdi", "--size", str(storage)
        ], check=True)

        # Ajouter un contrôleur SATA
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata"
        ], check=True)

        # Attacher le disque dur au contrôleur SATA
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "storageattach", vm_name, "--storagectl", "SATA Controller", 
            "--port", "0", "--device", "0", "--type", "hdd", "--medium", f"{vm_name}.vdi"
        ], check=True)

        # Ajouter un contrôleur IDE
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"
        ], check=True)

        # Ajouter le fichier ISO au contrôleur IDE
        subprocess.run([
            "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe", "storageattach", vm_name, "--storagectl", "IDE Controller",
            "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path
        ], check=True)

        display_message(f"VM {vm_name} créée avec succès.", Fore.GREEN)
    except subprocess.CalledProcessError as e:
        display_message(f"Erreur lors de la création de la VM : {e}", Fore.RED)

# 8. Création de conteneurs Docker
def create_container():
    container_count = 0

    
    container_count += 1
    # Choisir le type de conteneur
    display_message("Choisissez un type de conteneur:", Fore.CYAN)
    print("1. Ubuntu/Debian")
    print("2. RedHat/Fedora")
    print("3. Python")
    print("4. MariaDB")
    
    choice = input(Fore.YELLOW + "Votre choix: ")

    if choice == "1":
        image = "ubuntu"
    elif choice == "2":
        image = "fedora"
    elif choice == "3":
        image = "python"
    elif choice == "4":
        image = "mariadb"
    else:
        display_message("Choix invalide.", Fore.RED)
        return

    container_name = f"NOM-OS_A{container_count}"
    # Proposer d'ajouter un volume persistant

    attach_volume = input(Fore.YELLOW + "Souhaitez-vous attacher un volume persistant ? (y/n): ").lower()
    volume_option = ""
    if attach_volume == "y":
        volume_path = input(Fore.YELLOW + "Indiquez le chemin du volume: ")
        volume_option = f"-v {volume_path}:/data"

    # Créer le conteneur
    display_message(f"Création du conteneur {container_name} basé sur {image}...", Fore.YELLOW)
    subprocess.run(f"docker run -d --name {container_name} --network bridge {volume_option} {image} sleep infinity", shell=True)
    display_message(f"Conteneur {container_name} créé avec succès et joignable par pont.", Fore.GREEN)

    # Installer SSH dans le conteneur
    install_ssh(container_name, image)

# 9. Installer SSH et le configurer pour l'accès root
def install_ssh(container_name, image):
    display_message(f"Installation et configuration de SSH dans le conteneur {container_name}...", Fore.YELLOW)

    # Commandes pour installer SSH en fonction de l'image
    if "ubuntu" in image or "debian" in image:
        install_cmd = "apt update && apt install -y openssh-server"
        start_cmd = "service ssh start"
    elif "fedora" in image or "redhat" in image:
        install_cmd = "dnf install -y openssh-server"
        keygen_cmd = "ssh-keygen -A"
        start_cmd = "/usr/sbin/sshd"
    else:
        display_message("Le type de conteneur ne supporte pas l'installation de SSH.", Fore.RED)
        return

    # Exécuter les commandes d'installation SSH dans le conteneur
    subprocess.run(f"docker exec -it {container_name} bash -c '{install_cmd}'", shell=True)

    if "fedora" in image or "redhat" in image:
        subprocess.run(f"docker exec -it {container_name} bash -c '{keygen_cmd}'", shell=True)

    subprocess.run(f"docker exec -it {container_name} bash -c \"echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config\"", shell=True)
    subprocess.run(f"docker exec -it {container_name} bash -c \"echo 'root:rootpassword' | chpasswd\"", shell=True)
    subprocess.run(f"docker exec -it {container_name} bash -c '{start_cmd}'", shell=True)

    display_message(f"SSH installé et configuré dans le conteneur {container_name}.", Fore.GREEN)

# Lancer le processus principal
if __name__ == "__main__":
    while True:
        choice = input(Fore.YELLOW + "Souhaitez-vous créer une VM (1) ou un conteneur Docker (2) ? (0 pour quitter): ")
        if choice == "1":
            iso_path = input(Fore.YELLOW + "Indiquez le chemin de l'ISO : ")
            create_vbox_vm("TestVM", iso_path)
        elif choice == "2":
            create_container()
        elif choice == "0":
            break
        else:
            display_message("Choix invalide.", Fore.RED)
