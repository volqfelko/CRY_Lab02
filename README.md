# CRY_Lab02

## 1 CBC (1.5 pts)
1. Quel est l’algorithme (précis) utilisé pour chiffrer ces salaires ? N’oubliez pas la taille de la clef.
Le code source vous est donné dans le fichier cbc.py. 

    **Réponse : AES mode CBC avec une clé de 32 bytes**
2. Vous avez trouvé le salaire chiffré (ct) ainsi que l’IV correspondant d’un dirigeant d’USB (ils sont
dans votre fichier de paramètres). Récupérez le salaire ! Expliquez votre attaque en détails. Le
paramètre ID dans votre fichier de paramètres est l’identifiant du dirigeant dont vous souhaitez
connaitre le salaire.
3. Comment pouvez-vous corriger le problème ? Proposez un code n’ayant pas cette vulnérabilité.
4. Est-ce que cette attaque s’applique aussi à AES-CTR ? Justifiez.

## 2 CCM modifié (2 pts)
1. Plusieurs éléments sont modifiés par rapport à CCM. Lesquels ?
2. Vous avez intercepté deux textes clairs (m1 et m2) de test ainsi que les textes chiffrés, IVs, et
tags correspondants. Utilisez ces informations pour casser la construction. Utilisez vos paramètres
pour implémenter votre attaque et donnez le résulta

## 3 Bruteforce intelligent (1.5 pts)
1. Vous trouverez dans votre fichier de paramètres un texte clair (plaintext) et un texte chiffré
(ciphertext). Récupérez les deux clefs secrètes (en base64) et expliquez comment vous avez
procédé.
Indice : Il peut être utile de stocker des résultats intermédiaires dans un dictionnaire.
2. Décrivez votre algorithme. Quelle est la complexité pire-cas de votre attaque ? Comment se
compare-t-elle à un bruteforce des deux clefs ?
3. Qu’est-ce que votre attaque implique sur la complexité du bruteforce sur 3-key 3DES ?

