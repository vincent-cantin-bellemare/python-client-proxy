vcl 4.0;

backend default {
    .host = "web";  # Nom du service web dans votre docker-compose
    .port = "5000"; # Port sur lequel le service web est exposé
}

# Called at the beginning of a request, before a cache lookup.
sub vcl_recv {
    # Exemple de règles de mise en cache
    # Mettre en cache toutes les réponses GET pendant 2 minutes.
    if (req.method == "GET") {
        set req.http.Cache-Control = "max-age=120";
    }

    # Ne pas mettre en cache les requêtes à certaines URL
    if (req.url ~ "^/non-cacheable/") {
        return(pass);
    }
}

# Called after a document has been successfully retrieved from the backend.
sub vcl_backend_response {
    # Exemple de personnalisation de la mise en cache des réponses du backend
    # Mettre en cache les réponses pendant 5 minutes.
    set beresp.ttl = 5m;
}

# Called before a cached object is delivered to the client.
sub vcl_deliver {
    # Vous pouvez ajouter ici des en-têtes personnalisés ou effectuer d'autres actions
    # Exemple : Ajouter un en-tête pour indiquer que la réponse provient du cache
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT";
    } else {
        set resp.http.X-Cache = "MISS";
    }
}
