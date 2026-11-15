# Installateur Linux

Petit installateur interactif en Python pour Debian/Ubuntu, Fedora et Arch Linux.
Il propose Firefox, VLC, GIMP, LibreOffice, Git et Steam, ou permet de saisir
un nom de paquet. Il utilise `apt-get`, `dnf` ou `pacman` et demande confirmation
avant de lancer `sudo`.

## Utilisation

Python 3 est requis. Aucun module externe n'est nécessaire.

```bash
python3 installateur.py
```

Le choix de la distribution est toujours proposé. La détection de la machine
sert uniquement à présélectionner la réponse. Sur une distribution dérivée,
vérifie le nom du paquet proposé avant de confirmer.

## Distributions

- Debian et dérivées : `apt-get`
- Fedora : `dnf`
- Arch Linux : `pacman`
