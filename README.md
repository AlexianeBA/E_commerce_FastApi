TODO:

A revoir :

En cours :
- Appliquer une Architecture DDD

- dans domain/ecommerce = use_case = logique des routes
- infra doit hérité de domain mais pas l'inverse
- dans infra/api = routes appelle de la logique des routes présentes dans use_case + DTO
- Créer des Uses Cases afin de clean les endpoints
- infra/spi/repo = database, implémentation des méthodes 
- découper les models
- domain/ecommerce/interfaces = méthodes implémentée (pass)


A faire :
- ajouter une api pour la livraison https://wiki.openstreetmap.org/wiki/API https://openlayers.org/en/latest/apidoc/module-ol_control_Control-Control.html#getMap https://medium.com/applied-data-science/stop-paying-for-apis-to-calculate-distances-and-use-this-open-source-tool-32fbb31470df
- kink https://pypi.org/project/kink/0.1.3/
- route technique : status api 
- implémenter ruff https://docs.astral.sh/ruff/
- pipeline CI/CD (circle ci, github actions...)
- tests (domain)
- coverage
- push image docker sur dockerhub
- sphinx read the doc
- docker compose qui lance le back et le front
- front

Fait :
- Mettre en place un service SMTP pour création de compte, pour mot de passe oublié, recevoir le récap d'une commande par mail, : mailersend
- Créer une table Order avec : status,delivery_date, delivery_status
- Envoyer un mail après réception de la commande pour demander avis
- annulation commande
- ajouter un cron pour le statut des livraisons
- refund commande
- date de création de panier, date modif panier pour supprimer au bout de 3h
- Implémenter le suivi de la commande (nombre de jours pour livraison)
- re implémenter les users avec le même MDP pour tous https://www.mockaroo.com/
- Créer un dashboard admin avec un répac de toutes les ventes sur la plateforme, CA généré moyen,..., nombres d'Orders en Error,In Progress,Done....

