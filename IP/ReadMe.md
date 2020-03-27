Mise en place du serveur :
===========================

### CONFIGURATION de l'EC2 et du S3 :

Préambule :

Sur son compte AWS et Rosetta, générer une paire de clés d'accès ne comportant pas de caractère spéciaux. Uniquement les caractères [a-Z,A-Z,0-9].
Les enregistrer et les garder à l'abris des regards.

S3 Bucket :

Via interface graphique AWS : 
- Je crée un bucket : 'stockagefbsdpfilrougealan' sans accès public
- Je crée deux sous-dossiers : 'Sauvegarde' et 'StockageJSON'
- Je modifie les permissions pour l'accès : je mets tout à oui pour moi.
- Je modifie le management pour la lifecyle : pour tous les objets sur 365 jours

EC2 Instance :

Via interface graphique AWS :
- Je crée une instance EC2 avec : t2.micro, FreeBSD 11.3-STABLE-amd64-2020-02-20 (ami-007d81b0b99039d99), 1 instance
- Je télécharge une clé de connexion : keyPFilRougeAlan.pem, je la stocke sur l'ordinateur local, je la rends exécutable 'chmod 400 keyPFilRougeAlan.pem'
- J'édite le filtre : HTTPS, HTTP et SSH sur toutes les adresses IP

Policy :

Via interface graphique AWS :
- Je crée une policy permettant l'accès à toutes les actions et ressources pour S3 et Rekognition

Via RosettaHub :
- J'autorise Rekognition sur Allowance

Automatisation :

Création de la clé : 
```
aws ec2 create-key-pair --key-name keyPFilRougeAlan --query 'KeyMaterial' --output text > ~/Desktop/PFR/keyPFilRougeAlan.pem
chmod 777 ~/Desktop/PFR/keyPFilRougeAlan.pem
```
Il est nécessaire d'avoir la clé sur un disque dur et non une clé USB pour la rendre exécutable.

Lancement de l'instance :
```
aws ec2 run-instances --image-id ami-007d81b0b99039d99 --count 1 --instance-type t2.micro --key-name keyPFilRougeAlan --security-group-ids sg-0343a6c2fd1cd7510 --subnet-id subnet-7d07601b
````

Je récupère ensuite les adresses IP de mon instance (trouvées uniquement sur l'interface graphique AWS)
```
private IP : 172.31.5.59
public IP : 54.246.242.159
```

### CONFIGURATION de l'OS :

Je me connecte en SSH : 
```
ssh -i ~/Desktop/PFR/keyPFilRougeAlan.pem ec2-user@54.246.242.159
```
ou
```
ssh ec2-user@54.246.242.159
# A l'aide du mot de passe fourni
```

Lorsque je suis dans l'instance EC2, je bascule en root.

J'installe alors les librairies nécessaires à mon serveur :

```
cd /usr/home/ec2-user/
pkg install git
git clone https://github.com/AlanJBX/FilRouge.git
pkg install py37-pip
pkg install py37-pycurl
pkg install py37-pillow
pkg install py37-gunicorn
pkg install py37-redis
pkg install py37-lxml
pkg install openssl
pkg install vim
pip install -r ./IP/requirements.txt
```

Je configuration AWS :

```
aws configure
```
Je rentre alors les informations préalablements enregistrés de mes clés d'accès.

Je configure la date de mon OS :
```
cd /usr/share/zoneinfo/
tzsetup
```

### Lancement du serveur

Lancement programme :
```
cd /usr/home/ec2-user/FilRouge/
gunicorn-3.7 --certfile=certificat.crt --keyfile=certificat.key --bind 0.0.0.0:443 __init__:application
```

Lancement HTTPS, disponible sur https://54.246.242.159/
```
gunicorn-3.7 --bind 0.0.0.0:8000 __init__http:application
```
Lancement HTTP, disponible sur http://54.246.242.159:8000/home

###  Mise en place du PacketFilter

Modification du fichier rc.conf
```
echo 'pf_enable="YES"' >> /etc/rc.conf
echo 'pf_rules="/etc/pf.conf"' >> /etc/rc.conf
echo 'pflog_enable="YES"' >> /etc/rc.conf
echo 'pflog_logfile="/var/log/pflog"' >> /etc/rc.conf
```
Création du fichier pf.conf
```
vim /etc/pf.conf
```
Transfert du fichier pf.conf (modification des IP) via copier/coller

Vérification et lancement :
```
service pf check
service pflog start
service pf start
service pf status
```
Lecture des logs :
```
cat /var/log/pflog
```

### Certification

Je crée mon certificat HTTPS à l'aide du script suivant :
```
cd /usr/home/ec2-user/FilRouge/IP
csh script_ssl.csh
```
Attention, lors de l'enregistrement des différentes informations, pour l'adresse mail, il faut remplacer le '@' par 'at'

Je peux alors créer mon premier répertoire d'utilisateur avec le script suivant :
```
csh script_users.csh
```
Il est possible de modifier les nom d'utilisateur à l'exception de celui d'admin. Unique et nécessaire pour obtenir l'ensemble des fonctions de l'application.