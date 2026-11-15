#!/usr/bin/env python3
"""Installateur d'applications pour Debian, Fedora et Arch Linux."""

from __future__ import annotations

import platform
import re
import shutil
import subprocess
import sys


DISTROS = {
    "1": ("Debian / Ubuntu", "apt-get", ["sudo", "apt-get", "install", "-y"]),
    "2": ("Fedora", "dnf", ["sudo", "dnf", "install", "-y"]),
    "3": ("Arch Linux", "pacman", ["sudo", "pacman", "-S", "--needed", "--noconfirm"]),
}

# Les noms de paquets peuvent varier selon la distribution.
APPS = {
    "1": ("Firefox", {"1": "firefox-esr", "2": "firefox", "3": "firefox"}),
    "2": ("VLC", {"1": "vlc", "2": "vlc", "3": "vlc"}),
    "3": ("GIMP", {"1": "gimp", "2": "gimp", "3": "gimp"}),
    "4": ("LibreOffice", {"1": "libreoffice", "2": "libreoffice", "3": "libreoffice-fresh"}),
    "5": ("Git", {"1": "git", "2": "git", "3": "git"}),
    "6": ("Steam", {"1": "steam", "2": "steam", "3": "steam"}),
}


def detect_distro() -> str | None:
    """Retourne le choix correspondant à /etc/os-release, si reconnu."""
    try:
        values = {}
        with open("/etc/os-release", encoding="utf-8") as os_release:
            for line in os_release:
                if "=" in line:
                    key, value = line.rstrip().split("=", 1)
                    values[key] = value.strip('"').lower()
        identity = f"{values.get('id', '')} {values.get('id_like', '')}"
        if any(name in identity for name in ("debian", "ubuntu", "linuxmint", "pop")):
            return "1"
        if any(name in identity for name in ("fedora", "rhel", "centos")):
            return "2"
        if "arch" in identity or "manjaro" in identity:
            return "3"
    except OSError:
        pass
    return None


def choose_distro() -> str:
    detected = detect_distro()
    print("\nChoisis ta distribution :")
    for key, (name, _, _) in DISTROS.items():
        marker = " (détectée)" if key == detected else ""
        print(f"  {key}. {name}{marker}")
    while True:
        prompt = f"Numéro [{detected or '1'}] : "
        choice = input(prompt).strip() or detected or "1"
        if choice in DISTROS:
            return choice
        print("Choix invalide, entre 1, 2 ou 3.")


def choose_package(distro: str) -> str:
    print("\nApplication à installer :")
    for key, (name, _) in APPS.items():
        print(f"  {key}. {name}")
    print("  7. Autre paquet")
    while True:
        choice = input("Numéro : ").strip()
        if choice in APPS:
            return APPS[choice][1][distro]
        if choice == "7":
            package = input("Nom du paquet : ").strip()
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+_-]*", package):
                return package
            print("Nom de paquet invalide.")
        else:
            print("Choix invalide.")


def main() -> int:
    if platform.system() != "Linux":
        print("Cet installateur fonctionne uniquement sous Linux.")
        return 1

    print("=== Installateur Linux ===")
    distro = choose_distro()
    name, manager, command = DISTROS[distro]
    if shutil.which(manager) is None:
        print(f"Le gestionnaire {manager} est introuvable. Vérifie ta distribution.")
        return 1

    package = choose_package(distro)
    full_command = [*command, package]
    print(f"\nDistribution : {name}\nPaquet : {package}")
    print("Commande : " + " ".join(full_command))
    if input("Lancer l'installation ? [o/N] ").strip().lower() not in {"o", "oui", "y", "yes"}:
        print("Installation annulée.")
        return 0

    try:
        return subprocess.run(full_command, check=False).returncode
    except FileNotFoundError:
        print("Commande introuvable. Vérifie sudo et le gestionnaire de paquets.")
        return 1
    except KeyboardInterrupt:
        print("\nInstallation interrompue.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
