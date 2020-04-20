# Tezos_Democracy
Simulation d'un système démocratique* avec un smart-contract écrit en PascaLigo. Le but est de simuler des votes, et le peuple est représenté par les différentes adresses. 
*Le terme démocratie, désigne un régime politique dans lequel tous les citoyens participent aux décisions politiques au moins par le vote ^^.

## Objectifs :
+ 2 votes  possible ("yes"  or "no" )
+ Tous les utilisateurs ont le droit de voter
+ Un utilisateur doit pouvoir ne voter qu'une seule fois
+ Le contrat doit avoir un super utilisateur (admin) et son addresse est initialisé au déploiement du contrat
+ L'administrateur n'a pas le droit de voter
+ Le smart contrat doit être mis en pause si 10 personnes ont voté.
+ Quand le smart contract est mis en pause , le resultat du vote doit être calculé et stocké dans le storage.
+ L'administrateur doit pouvoir remettre à zéro le contrat (effacer les votes) + enlever la pause

## Procédure
On part du principe que vous avez un environnement Tezos avec Ligo installé.

Lancez votre sandBox Tezos (environnement de test).

Entrez dans le dossier tezos (cd /home/user/tezos) et executez les commandes suivantes.

Dans un premier terminal : 
```
./src/bin_node/tezos-sandboxed-node.sh 1 --connections 1
```
Dans un deuxième terminal : 
```
./src/bin_node/tezos-sandboxed-node.sh 9 --connections 1
```
Dans un troisième terminal (et c'est celui qu'on va utiliser)
```
eval `./src/bin_client/tezos-init-sandboxed-client.sh 1`
```
```
tezos-client rpc get /chains/main/blocks/head/metadata
```
```
tezos-activate-alpha
```
Pour voir vos adresses pré-configurées
```
tezos-client list known addresses
```
Copiez le contrat, compilez, et compressez le pour ensuite le placer dans le dossier tezos. 
```
ligo compile-contract democracyContract.ligo main > democracyContract.tz
```
Deplacez le .tz dans le dossier tezos
Définir l'état du storage initial et produire le tuple en michelson. Adresse à remplacer avec une de celles données au-dessus.
```
ligo compile-storage democracyContract.ligo main 'record admin = ("tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx": address); paused = False; votes = (map[] : map(address, bool)); end'
```
Se déplacer dans le dossier tezos, et deployer le contrat
```
tezos-client originate contract voteContract voting from bootstrap2  running ./democracyContract.tz --init '(Pair (Pair "tz1KqTpEZ7Yob7QbPE4Hy4Wo8fHG8LhKxZSx" False) {})' --burn-cap 4.178 &
```
```
tezos-client bake for bootstrap2
```
Commandes pour compilation
```
ligo compile-parameter democracyContract.ligo main 'Vote (Vote(record vote = False; end))' 
ligo compile-parameter democracyContract.ligo main 'Reset(0)'
```
## Tests unitaires
Pour les tests unitaires, lancez la commande : 
```
pytest testDemocracyContract.py
```

Pour plus de détail sur la configuration de la sandbox : https://tezos.gitlab.io/user/sandbox.html
