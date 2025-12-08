# Proposition de solution pour les exercices


## Exo 4

```
# Contexte
Ci joint tu trouveras un document EAC XML provenant des collections de l'UCLouvain.

# Instruction
Je voudrais que tu me génères une page html statique qui reprenne le contenu de cet EAC. Le texte doit être reproduit verbatim. Tu ne peux absolument pas changer le contenu du texte. Tu ne peux que faire en sorte que la mise en forme soit agréable dans un navigateur web.

# Format
Ta réponse doit être un document html self contained. Je dois pouvoir la sauver dans un fichier et la visualiser dans mon navigateur.
```


## Exo 4(bis)

```
# Contexte
Ci joint tu trouveras un exemple de document EAC XML provenant des collections de l'UCLouvain.

# Instruction
Je voudrais que tu me génères une programme python qui me permette de convertir cette notice EAC en page html statique. Le texte de l'EAC être reproduit verbatim. Le contenu du texte. Tu ne peux que faire en sorte que la mise en forme soit agréable dans un navigateur web.

# Format
Ton code python doit produire une page html self contained qui doit être agréable à visualiser dans un navigateur.

# Exemple d'utilisation

Lorsque j'exécute la commande: 

python3 ton_programme.py mon_fichier.eac.xml 

je veux que ton programme produise un fichier nommé "mon_fichier.eac.xml.html" à coté de l'original. Ce fichier doit contenir la page html statique reprenant le contenu exact des informations mentionnées dans "mon_fichier.eac.xml"
```


## Exo 5
```
# Contexte
J'ai une série de fichiers eac.xml que je voudrais convertir en pages html. 
Je dispose déjà d'un programme qui me permette de réaliser cette conversion. 

Pour cela, j'utilise la commande suivante:

python3 conversion.py mon_fichier.eac.xml 

Et ca me produit une page web nommée mon_fichier.eac.xml.html

# Instruction
Ecris moi un programme python qui me permette de faire cette conversion pour tous les fichiers eac.xml qui se trouvent dans un dossier.

# Exemple d'utilisation
python3 ton_programme.py c:/mon_dossier


Ton programme doit appeler "conversion.py" pour chacun des fichiers contenus dans le dossier.
Par exemple si c:/mon_dossier contient les fichiers a.eac.xml, b.eac.xml, c.eac.xml je veux que ton programme fasse la meme chose que

python3 conversion.py c:/mon_dossier/a.eac.xml
python3 conversion.py c:/mon_dossier/b.eac.xml
python3 conversion.py c:/mon_dossier/a.eac.xml

```

## EXO 6

```
# Contexte
Je suis archiviste, et je voudrais récupérer les informations disponibles à propos du oLd baley. 

# Instructions
Ecris moi un script python qui aille récupérer automatiquement les images et les notices associées à chacun des documents disponibles ici:  https://www.oldbaileyonline.org/record/16770425

# Exemple d'utilisation
Je veux pouvoir utiliser le script comme ceci: 

python3 oldbaley.py c:/mon_dossier

Et je veux que toutes les informations soient bien structurées dans le dossier. Par exemple:
c:/mon_dossier/article1/image.jpg
c:/mon_dossier/article1/notice.eac
c:/mon_dossier/article2/image.jpg
c:/mon_dossier/article2/notice.eac

etc...

# Format
Je veux que tu ne fournisse que le code python à coller dans un éditeur de texte.
```
