# Installation de Proxmox

Proxmox à été installé sur un serveur Dell équipé de 2 Intel Xeon de 6 coeurs chacuns, avec 96Go de RAM et 5 HDD de 300Go.  Un système RAID 0 est utilisé pour l'OS Proxmox, et RAID V pour les machines virtuelles au sein de Proxmox.

Pour plus d'informations, voir la documentation [ici](https://www.proxmox.com/en/products/proxmox-virtual-environment/get-started).

# Configuration

Notre proxmox est dans le réseau LAN, derriere le parefeu OPNsense qui fait également office de DHCP. Pour la config réseau dans Proxmox il faut éditer `/etc/network/interfaces`:

Pour le DHCP, il faut remplacer la configuration par celle-ci:
```ini
iface vmbr0 inet dhcp
```

Et pour une IP fixe:
```ini
iface vmbr0 inet static
    address X.X.X.X
    netmask Y.Y.Y.Y
    gateway Z.Z.Z.Z
```

Puis, redémarrer le service networking:
```bash
systemctl restart networking

```


# Infrastructure interne

Proxmox nous est utile pour centraliser nos machines virtuelles sur un seul serveur. Cela nous permet de mettre en oeuvre un environnement de test avec moins de matériel et plus rapidement, mais aussi de réduire le coût et la maintenance de l'environement de production si Proxmox est conservé. Voici les VMs déployées au sein du Proxmox:

![proxmox](images/proxmox.png)
