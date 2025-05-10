"""Includes two example worlds to experiment with different scenarios."""

import random
from world import Character, Item, Location, Puzzle, World


def get_world(arg: str, language: str ='en') -> World:
    if arg=='1':
        if language == 'es':
            return get_world_1_spanish()
        else:
            return get_world_1_english()
    elif arg=='2':
        if language == 'es':
            return get_world_2_spanish()
        else:
            return get_world_2_english()
    else:
        if language == 'es':
            return get_world_0_spanish()
        else:
            return get_world_0_english()

def get_world_0_english() -> World:
    item_1 = Item("Apple",
                  ["A fruit that can be eaten", "It is round-shaped and green"])
    item_2 = Item("Toy car",
                  ["A tiny toy purple car", "It looks brand new"])
    item_3 = Item("Mate",
                  ["A classical mate, ready to drink!", "It contains some yerba", "You can drink this to boost your energy!"])

    place_1 = Location("Garden",
                       ["A beautiful garden", "There is a statue in the center"],
                       items = [item_2])
    place_2 = Location("Cabin",
                       ["A small cabin", "It looks like no one has lived here for a while"])
    place_3 = Location("Mansion hall",
                       ["A big hall", "There is a big staircase"])
    
    two_random_numbers =  [random.randrange(0, 10) for i in range(2)]
    puzzle1 = Puzzle("puzzle",["There's a symbol of a microphone and below a letter that says how to open the door"],
                      f"To unlock this door, you have to say out loud the sum of {str(two_random_numbers[0])} and {str(two_random_numbers[1])}.",
                      f"The answer is {str(two_random_numbers[0] + two_random_numbers[1])} ")

    place_1.connecting_locations+=[place_2,place_3]
    place_2.connecting_locations+=[place_1]
    place_3.connecting_locations+=[place_1]
    place_1.block_passage(place_3,puzzle1)

    player = Character("Alicia",
                       ["She is wearing a long skirt","She likes to sing"],
                       inventory=[item_1],
                       location=place_1)
    npc = Character("Javier",
                    ["He has a long beard", "He loves to restore furtniture"],
                    inventory=[item_3],
                    location=place_3)

    the_world = World(player)
    the_world.add_locations([place_1, place_2, place_3])
    the_world.add_items([item_1, item_2, item_3])
    the_world.add_character(npc)
    the_world.set_objective(item_2,place_3)

    return the_world

def get_world_0_spanish() -> World:
    item_1 = Item("Manzana",
                  ["Una fruta que puede ser comida", "Es redonda y verde"])
    item_2 = Item("Auto de juguete",
                  ["Un pequeño auto de juguete de color púrpura", "Luce como recién comprado"])
    item_3 = Item("Mate",
                  ["Un mate clásico ¡listo para tomar!", "Contiene algo de yerba", "¡Puedes tomar esto para mejorar tu energía!"])

    place_1 = Location("Jardín",
                       ["Un jardín hermoso", "Hay una estatua en el centro"],
                       items = [item_2])
    place_2 = Location("Cabaña",
                       ["Una pequeña cabaña", "Parece que nadie ha vivido acá por un tiempo"])
    place_3 = Location("Hall de la Mansión",
                       ["Un hall grande", "Hay una enorme escalera principal"])

    two_random_numbers =  [random.randrange(0, 10) for i in range(2)]
    puzzle1 = Puzzle("puzzle",["Hay un dibujo de un micrófono y debajo un letrero, con la premisa para abrir la puerta"],
                      f"Para desbloquear esta puerta, hay que decir en voz alta la suma de {str(two_random_numbers[0])} y {str(two_random_numbers[1])}.",
                      f"La respuesta es {str(two_random_numbers[0] + two_random_numbers[1])} ")

    place_1.connecting_locations+=[place_2,place_3]
    place_2.connecting_locations+=[place_1]
    place_3.connecting_locations+=[place_1]
    place_1.block_passage(place_3,puzzle1)


    player = Character("Alicia",
                       ["Está usando una falda larga","Le gusta cantar"],
                       inventory=[item_1],
                       location=place_1)
    npc = Character("Javier",
                    ["Tiene una barba larga", "Le encanta restaurar muebles"],
                    inventory=[item_3],
                    location=place_3)
    
    

    the_world = World(player)
    the_world.add_locations([place_1, place_2, place_3])
    the_world.add_items([item_1, item_2, item_3])
    the_world.add_character(npc)
    the_world.set_objective(item_2,place_3)

    return the_world

def get_world_1_english() -> World:

    item_1 = Item("Turtle",["A small turtle", "Emma's pet", "Emma calls it 'Hojita'"])
    item_2 = Item("Key",
                  ["A key to open a lock", "It is golden", "There is a strange coat of arms engraved on it"])
    item_3 = Item("A grey hammer",
                  ["A big grey hammer that can be used to break things", "It is so heavy..."])
    item_4 = Item("Lock",
                  ["A strong lock with a coat of arms engraved on it", "It seems that it cannot be opened with your bare hands"])
    item_5 = Item("A green hammer",
                  ["A small green hammer", "It is just a toy and you cannot break anything with it"])

    place_3 = Location ("Garden",
                        ["The garden of the house", "It is relatively small, about 5 square meters."],
                        items = [item_1])
    place_2 = Location("Kitchen",
                       ["The kitchen of the house", "It's not huge, but it's not the smallest kitchen in the world either.", "A lot of light comes in through the windows"])
    place_2.connecting_locations = [place_3]
    place_2.block_passage(place_3, item_4)
    place_3.connecting_locations = [place_2]

    place_1 = Location("Art studio",
                       ["This is the art studio that Emma's mom has in the house"],
                       items = [item_3, item_5])
    place_1.connecting_locations = [place_2]
    place_2.connecting_locations = [place_1]

    player = Character("Emma",
                       ["A teenager of average height", "She is looking for her pet 'Hojita'"],
                       inventory = [],
                       location = place_1)
    npc = Character("Laura",
                        ["A woman in her 40s", "She is Emma's mom", "She is an artist, and loves oil painting"],
                        inventory = [item_2],
                        location= place_1)

    the_world = World(player)
    the_world.add_locations([place_1,place_2,place_3])
    the_world.add_items([item_1,item_2,item_3,item_4,item_5])
    the_world.add_character(npc)
    the_world.set_objective(item_1,place_2)

    return the_world

def get_world_1_spanish() -> World:
    
    item_1 = Item("Tortuga",["Una tortuga pequeña", "La mascota de Emma", "Emma la llama 'Hojita'"])
    item_2 = Item("Llave",
                  ["Una llave para abrir un candado", "Es dorada", "Tiene grabada la imagen de un extraño escudo de armas"])
    item_3 = Item("Un martillo gris",
                  ["Un martillo gris grande que puede ser usado para romper cosas", "Es muy pesado"])
    item_4 = Item("Candado",
                  ["Un candado fuerte que tiene grabado un escudo de armas", "Parece que no puede ser abierto con las manos"])
    item_5 = Item("Un martillo verde",
                  ["Un pequeño martillo verde", "Es solamente un juguete y no se puede romper nada con él"])

    place_3 = Location ("Jardín",
                        ["El jardín de la casa", "Es relativamente chico, de unos 5 metros cuadrados"],
                        items = [item_1])
    place_2 = Location("Cocina",
                       ["Es la cocina de la casa", "No es enorme, pero tampoco es la cocina más chiquita del mundo", "Por las ventanas entra mucha luz"])
    place_2.connecting_locations = [place_3]
    place_2.block_passage(place_3, item_4)
    place_3.connecting_locations = [place_2]

    place_1 = Location("Taller de pintura",
                       ["Es el taller de pintura que la madre de Emma tiene en su casa"],
                       items = [item_3, item_5])
    place_1.connecting_locations = [place_2]
    place_2.connecting_locations = [place_1]

    player = Character("Emma",
                       ["Una adolescente de estatura promedio", "Está buscando a su mascota 'Hojita'"],
                       inventory = [],
                       location = place_1)
    npc = Character("Laura",
                        ["Una mujer de unos 45 años de edad", "Es la madre de Emma", "Es una artista que pinta al óleo"],
                        inventory = [item_2],
                        location= place_1)

    the_world = World(player)
    the_world.add_locations([place_1,place_2,place_3])
    the_world.add_items([item_1,item_2,item_3,item_4,item_5])
    the_world.add_character(npc)
    the_world.set_objective(item_1,place_2)

    return the_world

def get_world_2_spanish() -> World:
    
    item_1 = Item("Pinturas",
                  ["Hay algo escrito con una pintura hecha con barro", "Dice 'Hay que confiar en los poderes que se nos han otorgado"], 
                  gettable=False)
    item_2 = Item("Estanque",
                  ["Un estanque de agua cristalina", "El agua es tan clara que funciona como un espejo"],
                   gettable=False)
    item_3 = Item("Un muro de llamas",
                  ["Las llamas son fuertes y dan mucho calor", "Tiene una altura de 3 metros", "Es imposible cruzarlas, ni caminando, ni corriendo, ni saltando."],
                   gettable=False)
    item_4 = Item("Guitarra",
                  ["Una guitarra clásica con 6 cuerdas", "Suena muy bien"])

    puzzle_1 = Puzzle("Puzzle",
                      ["Un encanto mágico que genera un muro intraspasable", "Mágicamente, al acercarse aparecen unas letras azules que explican cuál es el acertijo a resolver"],
                      "Hay que susurrar el nombre del río que baña la costa sur de la Banda Oriental", "Rio de la Plata")

    place_1 = Location ("Claro en el monte",
                        ["Un claro en un monte de eucaliptus cerca del Río Uruguay", "Se puede escuchar el sonido de los animales que viven en los árboles de este monte"],
                        items = [item_1, item_2])
    place_2 = Location("Zona silenciosa",
                       ["El monte continúa en esta parte", "A diferencia de la parte anterior, esta zona está insonorizada y no se escucha ni siquiera un mínimo sonido"])
    place_2.connecting_locations = [place_1]
    place_1.connecting_locations = [place_2]
    place_1.block_passage(place_2, item_3)

    place_3 = Location("Celda",
                       ["Una celda cuadrada de dos metros cuadrados", "La vegetación del monte ya ha ingresado al interior"])
    place_3.connecting_locations = [place_2]
    place_2.connecting_locations = [place_3]
    place_2.block_passage(place_3,puzzle_1)

    npc = Character("José Artigas",
                       ["El héroe nacional de Uruguay", "Está muy debilitado al estar tanto tiempo encerrado"],
                       inventory = [],
                       location = place_3)
    
    player = Character("Venancio",
                        ["Un gaucho uruguayo de 40 años de edad", "Pertenece a los soldados de Artigas", "Tiene el poder mágico de invocar una ola gigante de agua con la que puede apagar fuegos o humedecer la tierra"],
                        inventory = [item_4],
                        location= place_1)

    the_world = World(player)
    the_world.add_locations([place_1,place_2,place_3])
    the_world.add_items([item_1,item_2,item_3])
    the_world.add_character(npc)
    the_world.set_objective(player,npc)

    return the_world

def get_world_2_english() -> World:
    
    item_1 = Item("Writings",
                  ["There is something written on the wall.", "It says 'You have to trust in the powers that have been given to you.'"], 
                  gettable=False)
    item_2 = Item("Pond",
                  ["A pond full of crystal clear water", "The water is so clear that it works like a mirror"],
                   gettable=False)
    item_3 = Item("Firewall",
                  ["The flames are very hot", "It's 3 metres high", "It is impossible to cross them, neither walking, nor running, nor jumping."],
                   gettable=False)
    item_4 = Item("Guitar",
                  ["A classic guitar with 6 strings", "It sounds great"])

    puzzle_1 = Puzzle("Puzzle",
                      ["A strong magic is generating an impassable wall", "Magically, as you get closer, some blue letters appear explaining what the riddle to solve is."],
                      "You have to whisper the name of the river located on the southern coast of the Banda Oriental", "Rio de la Plata")

    place_1 = Location ("Clearing in the woods",
                        ["A clearing in a eucalyptus forest near the Uruguay River", "You can hear the sound of the animals that live in the trees of this forest."],
                        items = [item_1, item_2])
    place_2 = Location("Silent zone",
                       ["The forest continues in this part", "Unlike the previous area, this area is very silent and not even the slightest sound can be heard."])
    place_2.connecting_locations = [place_1]
    place_1.connecting_locations = [place_2]
    place_1.block_passage(place_2, item_3)

    place_3 = Location("Cell",
                       ["A square cell of two square meters", "The interior is full of plants that grew outside"])
    place_3.connecting_locations = [place_2]
    place_2.connecting_locations = [place_3]
    place_2.block_passage(place_3,puzzle_1)

    npc = Character("José Artigas",
                       ["Uruguay's national hero", "He is very weak after being locked up for so long."],
                       inventory = [],
                       location = place_3)
    
    player = Character("Venancio",
                        ["A Uruguayan gaucho in his 40s", "He belongs to the Artigas army", "He has the magical power to summon a giant wave of water with which he can put out fires or moisten the ground."],
                        inventory = [item_4],
                        location= place_1)

    the_world = World(player)
    the_world.add_locations([place_1,place_2,place_3])
    the_world.add_items([item_1,item_2,item_3])
    the_world.add_character(npc)
    the_world.set_objective(player,npc)

    return the_world