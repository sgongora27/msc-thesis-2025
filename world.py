"""This module implements the classes needed to represent the fictional world of the game.

The world class includes references to the several components (Items, Locations, Character),
and methods to update according to the detected changes by a language model.
"""

import re
from typing import Type


class Component:
  """A class to represent a component of the world.

  The components considered in the PAYADOR approach are Items, Locations and Characters.
  """
  def __init__ (self, name:str, descriptions: 'list[str]'):

    self.name = name
    """the name of the component"""

    self.descriptions = descriptions
    """a set of natural language descriptions for the component"""
  
class Puzzle (Component):
  """A class to represent a Puzzle"""

  def __init__(self, name:str, descriptions: 'list[str]', problem: str, answer: str):
    
    super().__init__(name, descriptions)
    """inherited from Component"""

    self.problem = problem
    """the main problem to be solved"""

    self.answer = answer
    """a possible answer to the riddle or puzzle"""

class Item (Component):
  """A class to represent an Item."""
  def __init__ (self, name:str, descriptions: 'list[str]', gettable: bool = True):

    super().__init__(name, descriptions)
    """inherited from Component"""

    self.gettable = gettable
    """indicates if the Item can be taken by the player"""

class Location (Component):
  """A class to represent a Location in the world."""
  def __init__ (self, name:str, descriptions: 'list[str]', items: 'list[Item]' = None, connecting_locations: 'list[Location]' = None):

    super().__init__(name, descriptions)
    """inherited from Component"""

    self.items = items or []
    """a list of the items available in that location"""

    self.connecting_locations = connecting_locations or []
    """a list of the reachable locations from itself."""

    self.blocked_locations = {}
    """a dictionary with the name of a location as key and <location,obstacle,symmetric> as value.
    A blocked passage between self and a location means that it
    will be reachable from [self] after overcoming the [obstacle].
    The symmetric variable is a boolean that indicates if, when unblocked,
    [self] will also be reachable from [location].
    """

  def block_passage(self, location: 'Location', obstacle, symmetric: bool = True):
    """Block a passage between self and location using an obstacle."""
    if location in self.connecting_locations:
      if location.name not in self.blocked_locations:
        self.blocked_locations[location.name] = (location, obstacle, symmetric)
        self.connecting_locations = [x for x in self.connecting_locations if x is not location]
      else:
        raise Exception(f"Error: A blocked passage to {location.name} already exists")
    else:
        raise Exception(f"Error: Two non-conected locations cannot be blocked")

  def unblock_passage(self, location: 'Location'):
    """Unblock a passage between self and location by adding it to the connecting locations of self.

    In case that the block was symmetric, self will be added to the connecting locations of location.
    """
    if self.blocked_locations[location.name]:
      self.connecting_locations += [location]
      if self.blocked_locations[location.name][2] and self not in location.connecting_locations:
        location.connecting_locations += [self]
      del self.blocked_locations[location.name]
    else:
      raise Exception("Error: That is not a blocked passage")

class Character (Component):
  """A class to represent a character."""
  def __init__ (self, name:str, descriptions: 'list[str]', location:Location, inventory: 'list[Item]' = None):

    super().__init__(name, descriptions)
    """inherited from Component"""

    self.inventory = inventory or []
    """a set of Items the carachter has"""

    self.location = location
    """the location of the character"""

    self.visited_locations = {self.location.name: []}
    """a dictionary that contains the successive descriptions of the visited places"""

  def move(self, new_location: Location):
    """Move the character to a new location."""
    if new_location in self.location.connecting_locations:
      self.location = new_location
      if self.location.name not in self.visited_locations:
        self.visited_locations[self.location.name] = []
    else:
      raise Exception(f"Error: {new_location.name} is not reachable")

  def save_item(self,item: Item, item_location_or_owner):
    """Add an item to the character inventory."""
    if item.gettable:
      if item not in self.inventory:
        self.inventory += [item]
        if item_location_or_owner.__class__.__name__ == 'Character':
          item_location_or_owner.inventory = [i for i in item_location_or_owner.inventory if i is not item]
        elif item_location_or_owner.__class__.__name__ == 'Location':
          item_location_or_owner.items = [i for i in item_location_or_owner.items if i is not item]
      else:
        raise Exception(f"Error: {item.name} is already in your inventory")
    else:
      raise Exception(f"Error: {item.name} cannot be taken")

  def drop_item (self, item: Item):
    """Leave an item in the current location."""
    self.inventory = [i for i in self.inventory if i is not item]
    self.location.items += [item]

  def give_item (self, character: 'Character', item: Item):
    """Give an item to another character."""
    try:
      character.save_item(item, self)
    except Exception as e:
      print(e)


class World:
  """A class to represent the fictional world, with references to every component."""
  def __init__ (self, player: Character) -> None:

    self.items = {}
    """a dictionary of all the Items in the world, with their names as values"""

    self.characters = {}
    """a dictionary of all the Characters in the world, with their names as values"""

    self.locations =  {}
    """a dictionary of all the Locations in the world, with their names as values"""

    self.player = player
    """a character for the player"""

    self.objective = None
    """the current objective for the player in this world"""

  def set_objective (self, first_component: Type[Component], second_component: Type[Component]):
    
    first_component_class = first_component.__class__.__name__
    second_component_class = second_component.__class__.__name__
    
    if first_component_class == "Character" and second_component_class == "Character":
      self.objective = (first_component, second_component)
    elif (first_component_class == "Character" and second_component_class in ["Location", "Item"]) or (second_component_class == "Character" and first_component_class in ["Location", "Item"]):
      self.objective = (first_component, second_component)
    elif (first_component_class  == "Item" and second_component_class == "Location") or (second_component_class  == "Item" and first_component_class == "Location"):
      self.objective = (first_component, second_component)
    else:
      raise Exception(f"Error: Cannot set objective with classes {first_component_class} and {second_component_class}")

  def check_objective(self) -> bool:

    done = False
    first_component_class = self.objective[0].__class__.__name__
    second_component_class = self.objective[1].__class__.__name__

    if first_component_class == "Character" and second_component_class == "Character":
      if self.objective[0].location == self.objective[1].location: done = True
    elif first_component_class == "Character" and second_component_class == "Location":
      if self.objective[0].location == self.objective[1]: done = True
    elif first_component_class == "Character" and second_component_class == "Item":
      if self.objective[1] in self.objective[0].inventory: done = True
    elif first_component_class == "Item" and second_component_class == "Location":
      if self.objective[0] in self.objective[1].items: done = True

    return done

  def add_location (self,location: Location) -> None:
    """Add a location to the world."""
    if location.name in self.locations:
      raise Exception(f"Error: Already exists a location called '{location.name}'")
    else:
       self.locations[location.name] = location

  def add_item (self, item: Item) -> None:
    """Add an item to the world."""  
    if item.name in self.items:
      raise Exception(f"Error: Already exists an item called '{item.name}'")
    else:
      self.items[item.name] = item

  def add_character (self, character: Character) -> None:
    """Add a character to the world."""
    if character.name in self.characters:
      raise Exception(f"Error: Already exists a character called '{character.name}'")
    else:
      self.characters[character.name] = character

  def add_locations (self,locations: 'list[Location]') -> None:
    """"Add a set of locations to the world."""
    for location in locations:
      self.add_location(location)

  def add_items (self, items: 'list[Item]') -> None:
    """Add a set of items to the world."""
    for item in items:
      self.add_item(item)

  def add_characters (self, characters: 'list[Character]') -> None:
    """Add a set of characters to the world."""
    for character in characters:
      self.add_character(character)

  def render_world(self, *, language:str = 'en', detail_components:bool = True) -> str:
    """Return the fictional world as a natural language description, using simple sentences.

    The components described are only those the player can see in the current location.
    If detail_components is False, then the descriptions for each component are not included.
    """
    rendered_world = ''

    if language == 'es':
      rendered_world = self.__render_world_spanish(detail_components = detail_components)
    else:
      rendered_world = self.__render_world_english(detail_components = detail_components)

    return rendered_world
  
  def __render_world_spanish(self, *,  detail_components:bool = True) -> str:
    """Return the fictional world as a natural language description, using simple sentences in Spanish.

    The components described are only those the player can see in the current location.
    If detail_components is False, then the descriptions for each component are not included.
    """
    player_location = self.player.location
    reachable_locations = [f"<{p.name}>" for p in player_location.connecting_locations]
    blocked_passages = [f"<{p}> bloqueado por <{player_location.blocked_locations[p][1].name}>" for p in player_location.blocked_locations.keys()]
    characters_in_the_scene = [character for character in self.characters.values() if character.location is player_location]

    
    world_description = f'El jugador está en <{player_location.name}>\n'
    
    if reachable_locations:
      world_description += f'Desde <{player_location.name}> el jugador puede ir a: {(", ").join(reachable_locations)}\n'
    else:
      world_description += f'Desde <{player_location.name}> el jugador puede ir a: None\n'

    if blocked_passages:
      world_description += f'Desde <{player_location.name}> hay pasajes bloqueados hacia: {(", ").join(blocked_passages)}\n'
    else:
      world_description += f'Desde <{player_location.name}> hay pasajes bloqueados hacia: None\n'

    if self.player.inventory:
      world_description += f'El jugador tiene los siguientes objetos en su inventario: {(", ").join([f"<{i.name}>" for i in self.player.inventory])}\n'
    else:
      world_description += f'El jugador tiene los siguientes objetos en su inventario: None\n'

    if player_location.items:
      world_description += f'El jugador puede ver los siguientes objetos: {(", ").join([f"<{i.name}>" for i in player_location.items])}\n'
    else:
      world_description += f'El jugador puede ver los siguientes objetos: None\n'
      
    if characters_in_the_scene:
      world_description += f'El jugador puede ver a los siguientes personajes: {(", ").join([f"<{c.name}>" for c in characters_in_the_scene])}'
    else:
      world_description += f'El jugador puede ver a los siguientes personajes: None'

    details = ""
    if detail_components:
      items_in_the_scene = player_location.items + self.player.inventory + [blocked_values[1] for blocked_values in player_location.blocked_locations.values() if isinstance(blocked_values[1], Item)]
      puzzles_in_the_scene = [blocked_values[1] for blocked_values in player_location.blocked_locations.values() if isinstance(blocked_values[1], Puzzle)]

      details += "\nAquí hay una descripción de cada componente.\n"
      details += f"<{player_location.name}>: Este es el lugar en el que está el jugador. {('. ').join(player_location.descriptions)}.\n"
      details += "Personajes:\n"
      details += f"- <Jugador>: El jugador está actuando como <{self.player.name}>. {('. ').join(self.player.descriptions)}.\n"
      if len(characters_in_the_scene)>0:
        for character in characters_in_the_scene:
          details += f"- <{character.name}>: {('. ').join(character.descriptions)}."
          if len(character.inventory)>0:
            details += f"Este personaje tiene los siguientes objetos en su inventario: {(', ').join([f'<{i.name}>' for i in character.inventory])}\n"
            items_in_the_scene+= character.inventory
          else:
            details += "\n"
      if len(items_in_the_scene)>0:
        details+="Objetos:\n"
        for item in items_in_the_scene:
          details += f"- <{item.name}>: {('. ').join(item.descriptions)}\n"
      if len(puzzles_in_the_scene)>0:
        details+="Puzzles:\n"
        for puzzle in puzzles_in_the_scene:
          details+= f'- <{puzzle.name}>: {(". ").join(puzzle.descriptions)}. El acertijo a resolver es: "{puzzle.problem}". La respuesta esperada, que NO PUEDES decirle al jugador (JAMÁS) es: "{puzzle.answer}".\n'

    return world_description + '\n' + details

  def __render_world_english(self, *,  detail_components:bool = True) -> str:
    """Return the fictional world as a natural language description, using simple sentences in English.

    The components described are only those the player can see in the current location.
    If detail_components is False, then the descriptions for each component are not included.
    """
    player_location = self.player.location
    reachable_locations = [f"<{p.name}>" for p in player_location.connecting_locations]
    blocked_passages = [f"<{p}> blocked by <{player_location.blocked_locations[p][1].name}>" for p in player_location.blocked_locations.keys()]
    characters_in_the_scene = [character for character in self.characters.values() if character.location is player_location]

    
    world_description = f'The player is in <{player_location.name}>\n'
    
    if reachable_locations:
      world_description += f'From <{player_location.name}> the player can access: {(", ").join(reachable_locations)}\n'
    else:
      world_description += f'From <{player_location.name}> the player can access: None\n'

    if blocked_passages:
      world_description += f'From <{player_location.name}> there are blocked passages to: {(", ").join(blocked_passages)}\n'
    else:
      world_description += f'From <{player_location.name}> there are blocked passages to: None\n'

    if self.player.inventory:
      world_description += f'The player has the following objects in the inventory: {(", ").join([f"<{i.name}>" for i in self.player.inventory])}\n'
    else:
      world_description += f'The player has the following objects in the inventory: None\n'

    if player_location.items:
      world_description += f'The player can see the following objects: {(", ").join([f"<{i.name}>" for i in player_location.items])}\n'
    else:
      world_description += f'The player can see the following objects: None\n'
      
    if characters_in_the_scene:
      world_description += f'The player can see the following characters: {(", ").join([f"<{c.name}>" for c in characters_in_the_scene])}'
    else:
      world_description += f'The player can see the following characters: None'

    details = ""
    if detail_components:
      items_in_the_scene = player_location.items + self.player.inventory + [blocked_values[1] for blocked_values in player_location.blocked_locations.values() if isinstance(blocked_values[1], Item)]
      puzzles_in_the_scene = [blocked_values[1] for blocked_values in player_location.blocked_locations.values() if isinstance(blocked_values[1], Puzzle)]

      details += "\nHere is a description of each component.\n"
      details += f"<{player_location.name}>: This is the player's location. {('. ').join(player_location.descriptions)}.\n"
      details += "Characters:\n"
      details += f"- <Player>: The player is acting as <{self.player.name}>. {('. ').join(self.player.descriptions)}.\n"
      if len(characters_in_the_scene)>0:
        for character in characters_in_the_scene:
          details += f"- <{character.name}>: {('. ').join(character.descriptions)}."
          if len(character.inventory)>0:
            details += f" This character has the following items: {(', ').join([f'<{i.name}>' for i in character.inventory])}\n"
            items_in_the_scene+= character.inventory
          else:
            details += "\n"
      if len(items_in_the_scene)>0:
        details+="Objects:\n"
        for item in items_in_the_scene:
          details += f"- <{item.name}>: {('. ').join(item.descriptions)}\n"
      if len(puzzles_in_the_scene)>0:
        details+="Puzzles:\n"
        for puzzle in puzzles_in_the_scene:
          details+= f'- <{puzzle.name}>: {(". ").join(puzzle.descriptions)}. The riddle to solve is: "{puzzle.problem}". The expected answer, that you CANNOT tell the player (EVER) is: "{puzzle.answer}".\n'

    return world_description + '\n' + details

  def update (self, updates: str) -> None:
    """Does the changes in the world according to the output of the language model.

    The possible changes considered are:
      - an object was moved
      - a location is now reachable
      - the position of the player changed.
    """
    self.parse_moved_objects(updates)
    self.parse_blocked_passages(updates)
    self.parse_location_change(updates)

  def parse_moved_objects (self, updates: str) -> None:
    """Parse the output of the language model to update the position of objects.

    There are three cases:
      - the player has a new item
      - the player gave an item to other character
      - the player dropped an item.
    """
    parsed_objects = re.findall(r".*Moved object:\s*(.+)",updates)
    if 'None' not in parsed_objects:
      parsed_objects_split = re.findall(r"<[^<>]*?>.*?<[^<>]*?>",parsed_objects[0])
      for parsed_object in parsed_objects_split:
        pair = re.findall(r"<([^<>]*?)>.*?<([^<>]*?)>",parsed_object)
        try:
          world_item = self.items[pair[0][0]]
          
          if pair[0][1] in ['Inventory', 'Inventario', 'Player',  'Jugador', self.player.name]: #(save_item case)
            item_location = [character for character in list(self.characters.values()) if world_item in character.inventory]
            item_location += [location for location in list(self.locations.values()) if world_item in location.items]
            self.player.save_item(world_item, item_location[0])

          elif pair[0][1] in self.characters: #(give_item case)
            self.player.give_item(self.characters[pair[0][1]], world_item)
          
          else: #(drop_item case)
            self.player.drop_item(world_item)
        except Exception as e:
          print(e)

  def parse_blocked_passages (self, updates: str) -> None:
    """Parse the output of the language model to update the reachable locations."""
    parsed_blocked_passages = re.findall(r".*Blocked passages now available:\s*(.+)",updates)
    if 'None' not in parsed_blocked_passages:
      parsed_blocked_passages_split = re.findall(r"<([^<>]*?)>",parsed_blocked_passages[0])
      for parsed_passage in parsed_blocked_passages_split:
        try:
          self.locations[self.player.location.name].unblock_passage(self.locations[parsed_passage])
        except Exception as e:
          print (e)

  def parse_location_change (self, updates: str) -> None:
    """Parse the output of the language model to update the position of the player."""
    parsed_location_change = re.findall(r".*Your location changed: (.+)",updates)
    if "None" not in parsed_location_change:
      parsed_location_change_split = re.findall(r"<([^<>]*?)>",parsed_location_change[0])
      try:
        self.player.move(self.locations[parsed_location_change_split[0]])
      except Exception as e:
        print(e)

