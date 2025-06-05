from entity import Product

datenbank = {}

# fake von Produkt-Daten
datenbank["products"] = {
    17   : Product(17, "Boots", "Boots zur Jeans", 99.90, ["https://images.pexels.com/photos/23319145/pexels-photo-23319145/free-photo-of-legs-and-boots-of-standing-man.jpeg", "https://images.pexels.com/photos/23319150/pexels-photo-23319150/free-photo-of-hands-of-a-man-holding-a-pair-of-brown-hiking-boots.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", "https://images.pexels.com/photos/23319137/pexels-photo-23319137/free-photo-of-feet-of-a-man-wearing-brown-hiking-boots.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"], False),
    4711 : Product(4711, "Jeans", "Super robuste Jeans", 179.0, ["https://images.pexels.com/photos/6843238/pexels-photo-6843238.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", "https://images.pexels.com/photos/8177655/pexels-photo-8177655.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", "https://images.pexels.com/photos/8432842/pexels-photo-8432842.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"], True)
}

def save(entity_name, id, object):
    if entity_name not in datenbank:
        datenbank[entity_name] = {}
    datenbank[entity_name][id] = object

def find_by_id(entity_name, id):
    if id in datenbank[entity_name]:
        return datenbank[entity_name][id]
    else:
        return None

def find_all(entity_name):
    return datenbank[entity_name].values()

def delete(entity_name, id):
    datenbank.get(entity_name).remove(id)
    # alternativ: datenbank[x]  entspricht immer.  datenbank.get(x)

def update(entity_name, id, object):
    datenbank[entity_name][id] = object

