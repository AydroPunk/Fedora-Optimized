import os
import fileinput
import sys

NC = '\033[0m'
Red = '\033[0;31m'  # Red
Green = '\033[0;32m'  # Green
Yellow = '\033[0;33m'  # Yellow


def print_banner():
    print(r'''ᴅᴇsᴛʀᴏʏɪɴɢ ʟɪɴᴜxᴛᴜʙᴇʀs ғʀᴏᴍ ᴡɪᴛʜɪɴ ᴛʜᴇ ᴄᴏᴍᴍᴜɴɪᴛʏ''')


def main():
    sys.tracebacklimit = 0
    print_banner()
    print(f"{Yellow}ユーリWelcome To Fusion Dimension{NC}")


if __name__ == "__main__":
    main()

# Upgrade
os.system("sudo dnf upgrade -y")

# RPM Fusion / NonFree
os.system(
    "sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-38.noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-38.noarch.rpm -y")
os.system("sudo dnf groupupdate core -y")
os.system("sudo dnf install dnf-plugins-core -y")

# Installing Nvidia Driver Akmod-Nvidia
os.system("sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda xorg-x11-drv-nvidia-cuda-libs -y")

# Installing Nvidia Driver Cuda Toolkit
os.system(
    "sudo dnf config-manager --add-repo=https://developer.download.nvidia.com/compute/cuda/repos/fedora37/x86_64/cuda-fedora37.repo -y")
os.system("sudo dnf check-update -y && sudo dnf install cuda -y")

# Increase DNF speed
with open("/etc/dnf/dnf.conf", "a") as f:
    f.write("\n# Para que vaya como el rayo macquen\nfastestmirror=True\nmax_parallel_downloads=10\nkeepcache=True\n")

# Ruta del archivo dnf.conf
file__path = "/etc/dnf/dnf.conf"

# Abrir el archivo en modo de lectura
with open(file__path, "r") as f:
    lines = f.readlines()

# Buscar la línea que contiene "installonly_limit"
for i, line in enumerate(lines):
    if line.startswith("installonly_limit="):
        # Reemplazar el valor de "installonly_limit" con "2"
        lines[i] = "installonly_limit=2\n"
        break

# Escribir las líneas actualizadas en el archivo
with open(file__path, "w") as f:
    f.writelines(lines)

# Installing dnf5
os.system("sudo dnf install dnf5 -y")

# Clean Your System (With DNF5)
os.system("sudo dnf5 clean all && sudo dnf5 autoremove -y && sudo dnf5 update -y")

# Installing tools to extract files and utilities
os.system("sudo dnf5 install p7zip p7zip-plugins unrar unzip gzip bat lsd btop gnome-text-editor kitty nvim -y")

# Obtener el nombre de usuario actual
username = os.getlogin()

# Rutas de los directorios donde se creará el archivo ".aliases"
paths = [f"/home/{username}", "/root"]

# Contenido del archivo ".aliases"
content = '''extract() {
    case "$1" in
        *.tar.bz2|*.tbz2) tar -xjf "$1" ;;
        *.tar.gz|*.tgz) tar -xzf "$1" ;;
        *.tar.xz) tar -xf "$1" ;;
        *.bz2) bunzip2 "$1" ;;
        *.rar) unrar x -f "$1" ;;
        *.gz) gunzip "$1" ;;
        *.tar) tar -xf "$1" ;;
        *.zip) unzip -qq -k "$1" ;;
        *.Z) uncompress "$1" ;;
        *.7z) 7z x -f "$1" ;;
        *) echo "Don't know how to extract '$1'..." ;;
    esac
}

# alias
alias icat="kitty +kitten icat"
alias cat='bat'
alias cls="clear"
alias vim="nvim"
alias top="btop"
alias copy="xclip -selection clipboard"
alias edit="gnome-text-editor"
# colorls
alias ls='lsd --group-directories-first'
alias lsa='lsd -la --group-directories-first'
alias lss="lsd -a --group-directories-first"
alias lst='ls --tree'
'''

# Crear el archivo ".aliases" en cada ruta
for path in paths:
    file_path = os.path.join(path, ".aliases")
    with open(file_path, "w") as f:
        f.write(content)

# Ruta del archivo .zshrc en el directorio de inicio del usuario
user_file_path = f"/home/{username}/.zshrc"

# Ruta del archivo .zshrc en el directorio raíz
root_file_path = "/root/.zshrc"

# Contenido a agregar
content_zsh = f'''
# Agregar alias a .zshrc en /home/{username}
if [ -f ~/.aliases ]; then
    . ~/.aliases
fi

export BAT_THEME="Dracula"
'''

content_zsh_root = f'''
# Agregar alias a .zshrc en /root
if [ -f /root/.aliases ]; then
    . /root/.aliases
fi

export BAT_THEME="Dracula"
'''

# Buscar la línea que contiene "# alias ohmyzsh="mate ~/.oh-my-zsh""
for line in fileinput.input(user_file_path, inplace=True):
    print(line, end="")
    if line.startswith('# alias ohmyzsh="mate ~/.oh-my-zsh"'):
        # Agregar contenido después de la línea correspondiente
        print(content_zsh)

for line in fileinput.input(root_file_path, inplace=True):
    print(line, end="")
    if line.startswith('# alias ohmyzsh="mate ~/.oh-my-zsh"'):
        # Agregar contenido después de la línea correspondiente
        print(content_zsh_root)
