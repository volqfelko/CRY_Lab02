# CRY_Lab02

## 1 CBC (1.5 pts)
**1. Quel est l’algorithme (précis) utilisé pour chiffrer ces salaires ? N’oubliez pas la taille de la clef.
Le code source vous est donné dans le fichier cbc.py.<br/><br/>**

   Réponse : AES mode CBC avec une clé de 32 bytes<br/><br/>
**2. Vous avez trouvé le salaire chiffré (ct) ainsi que l’IV correspondant d’un dirigeant d’USB (ils sont
dans votre fichier de paramètres). Récupérez le salaire ! Expliquez votre attaque en détails. Le
paramètre ID dans votre fichier de paramètres est l’identifiant du dirigeant dont vous souhaitez
connaitre le salaire.<br/><br/>**

   Réponse : Etant donné que l'IV est uniquement incrementé de 1 entre chaque requêtes de chiffrement envoyée à l'oracle,
   on peut simplement lui envoyer une demande de chiffrement pour récuperer l'IV actuel et ainsi "forgé" des messages
   qui auront comme 128 premiers bits la même entrée que celle du message intercepté.<br/><br/>
   En effet, on sait que : IV XOR 128 premiers bits du plain = b'/X3wXZwiGkLVSJEengCx1w=='<br/><br/>
   Il nous faut donc simplement avoir un texte qui XOR l'IV_Courant+1 = b'/X3wXZwiGkLVSJEengCx1w==' pour avoir le
   même premier bloc en entrée et donc un flux de chiffrement identique au message intercepté.<br/>
   En faisant cela, on peut donc comparer les ciphers en incrémentant le salaire de 0 à 3000 jusqu'à ce que l'on
   trouve un cipher identique à celui intercepté initialement
   ![CBC salaire](/imgs/img.png "CBC salaire")
   <br/>

**3. Comment pouvez-vous corriger le problème ? Proposez un code n’ayant pas cette vulnérabilité.<br/><br/>**

   Réponse : Le problème est qu'un IV prévisible revient au même qu'un IV fixe, il faut donc le rendre aléatoire
   et donc imprévisible entre chaque requêtes.<br/>
   ![CBC salaire](/imgs/IncrementRandom.png "CBC salaire")<br/>
   Une incrémentation aléatoire comme cela devrait faire l'affaire<br/><br/>

**4. Est-ce que cette attaque s’applique aussi à AES-CTR ? Justifiez.<br/><br/>**
  Réponse : Non car dans CTR l'IV et le counter sont chiffrés, et seulement ensuite, le plain est XOR avec ce résultat
  pour donner le cipher.

## 2 CCM modifié (2 pts)
**1. Plusieurs éléments sont modifiés par rapport à CCM. Lesquels ?**

Réponse : Le tag est chiffré, ce qui n'est pas forcément fait de base dans CCM. <br/>
La clé est la même pour chiffré le tag et le message. <br/>
Le même nonce est utilisé pour le chiffrement du tag ainsi que le chiffrement du message ce qui pose problème
au niveau du CTR.<br/>
Il n'y a pas "d'authenticated data" pour la création du tag.

**2. Vous avez intercepté deux textes clairs (m1 et m2) de test ainsi que les textes chiffrés, IVs, et
tags correspondants. Utilisez ces informations pour casser la construction. Utilisez vos paramètres
pour implémenter votre attaque et donnez le résultat**

Réponse : Pour casser la construction il faut dans un premier temps remarquer que le tag est chiffré avec
le même nonce que le premier bloc du message que nous souhaitons chiffrer.<br/>
En effet, on peut voir que le **CTR == 0** pour les 2 opérations étant donné qu'il est réinitialisé au moment
de la création de la nouvelle variable "cipher" qui va permettre de chiffrer le tag.

En constatant cette erreur d'implémentation, on peut donc récuperer le tag déchiffré du message intercepté.<br/>
Comme cela : <br/> 
- Récuperation du keystream = message1 XOR cipher
- Récuperation du tag déchiffré = tagChiffré XOR keystream 

Cette opération fonctionne car on a la même valeur (IV || CTR = 0) qui est utilisée pour chiffrer le tag ainsi que le message
étant donné que le CTR = 0 dans les 2 cas.<br/>

![img.png](/imgs/Schema_Ctr0.png)<br/>
(J'ai fait un schéma pour m'aider à comprendre)

En ayant le tag déchiffré, non pouvons donc nous attaquer à CBC-MAC (comme vu en classe) et casser l'integrité des 
messages si on intercepte un message et son tag correspondant.<br/>

![img.png](/imgs/CBC-MAC-Attack.png)

Le schéma ci-dessus illustre parfaitement l'attaque, pour forger un message ayant un tag valide il ne reste donc qu'a
faire : forged_message = message || (message XOR tagDechiffré)<br/>
Ce message aura donc le même tag (donc valide) que le message initial intercepté alors que ce n'est pas un message légitime.<br/>
L'integrité est donc cassée !

**4. Corrigez l’implémentation et faites en sorte que le chiffrement CCM soit correct !**

Réponse : Pour corriger l'implémentation il suffit de ne pas réinitialiser le ctr et donc ne pas utiliser le même nonce.<br/>
On peut le faire simplement comme cela : ` cipher = AES.new(key, mode = AES.MODE_CTR, nonce = Random.new().read(8))`

## 3 Bruteforce intelligent (1.5 pts)
**1. Vous trouverez dans votre fichier de paramètres un texte clair (plaintext) et un texte chiffré
(ciphertext). Récupérez les deux clefs secrètes (en base64) et expliquez comment vous avez
procédé.**<br/>

Réponse : Pour trouver les clés de chiffrement, il faut appliquer une attaque "Meet-in-the-middle"
Etant donnée que les clefs ne varient que sur les 2 premiers octets, il est facile et rapide de toutes les
calculer et les stocker dans un dictionnaire avec pour chaque entrée : **Key, Value.**<br/>
Ou la **Key** est la clé de chiffrement utilisée pour le premier chiffrement AES et la **Value** étant le cipher résultant
du chiffrement du plaintext donnné par la **Key** calculée.<br/>
Une fois le dictionnaire rempli, il ne reste qu'à bouclé sur toutes les paires de **Key, Value** dedans
et pour chacunes, déchiffrer le Ciphertext de base afin de voir s'il est contenu dans notre dictionnaire.<br/>
Si c'est le cas, nous avons donc trouvé la paire de clés permettant le déchiffrement du cipher.

![Keys Bruteforce](/imgs/meetInTheMiddle.png "Bruteforce")<br/>
**2. Décrivez votre algorithme. Quelle est la complexité pire-cas de votre attaque ? Comment se
compare-t-elle à un bruteforce des deux clefs ?**<br/>

Réponse : J'ai décrit mon implémentation dans la question ci-dessus.<br/>
La complexité de l'algorithme dans le pire des cas est de **O(2^32)** car dans le pire cas il faudra parcourir l'entièreté
des 2^16 clés dans chacune des boucles afin de trouver les bonnes.<br/>
Ce qui donne : **O(2^16)*O(2^16) = O(2^32)***<br/><br/>
La pire complexité d'un bruteforce classique resterait la même que celle de "meet-in-the-middle".
Mais l'avantage de cette technique est le fait de stocker uniquement les résultats intermédiaires et pas toutes les paires 
de clés testées.<br/><br/>
**3. Qu’est-ce que votre attaque implique sur la complexité du bruteforce sur 3-key 3DES ?**<br/>
Réponse : Cette attaque montre que la complexité du brute force sur 3-key 3DES n'est pas aussi élevée qu'on pourrait le penser. <br/>
En effet, il était supposé que la complexité du brute force sur 3-key 3DES était de 2^112, vu qu'il y a 3 clés de 56 bits chacune,
mais cette attaque permet de réduire cette complexité à 2^56.

