from tdl.map import Map;

from random import randint;
from components.ai import BasicMonster;
from components.fighter import Fighter;
from entity import Entity;
from render_functions import RenderOrder;


class GameMap(Map):
    def __init__(self, width, height):
        super().__init__(width, height);
        self.explored = [[False for y in range(height)] for x in range(width)];

# Classe Retângulo.
class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x;
        self.y1 = y;
        self.x2 = x + w;
        self.y2 = y + h;
    
    # center method: returns the center point of a rectangle;
    def center(self):
        center_x = int( (self.x1 + self.x2) / 2);
        center_y = int( (self.y1 + self.y2) / 2);
        return (center_x, center_y);
    
    # intersect method: returns true if two rectangles overlap.
    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

# Create an room method
def create_room(game_map, room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True;
            game_map.transparent[x, y] = True;

## Create an HORIZONTAL TUNNEL
def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True;
        game_map.transparent[x, y] = True;

## Create an VERTICAL TUNNEL
def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True;
        game_map.transparent[x, y] = True;

# Place Entities in the map.
def place_entities(room, entities, max_monster_per_room, colors):
    # Get a random number of monsters
    number_of_monsters = randint(0, max_monster_per_room);

    for i in range(number_of_monsters):
        # Choose a random location in the room
        x = randint(room.x1 + 1, room.x2 - 1);
        y = randint(room.y1 + 1, room.y2 - 1);

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            # CREATE MONSTERS.
            if randint(0, 100) < 80:
                fighter_component = Fighter(hp=10, defense=0, power=3);
                ai_component = BasicMonster();

                monster = Entity(x, y, 'o', colors.get('Orc'), 'Orc', blocks=True,
                    render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component);
            else:
                fighter_component = Fighter(hp=16, defense=1, power=4);
                ai_component = BasicMonster();

                monster = Entity(x, y, 'T', colors.get('Troll'), 'Troll', blocks=True,
                    render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component);
            entities.append(monster);

## Given a game_map object
def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, colors):
    rooms = []; # Rooms list.
    num_rooms = 0;

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size);
        h = randint(room_min_size, room_max_size);
        # random position without going out of the boundaries of the map.
        x = randint(0, map_width - w - 1);
        y = randint(0, map_height - h - 1);

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h);

        # run through the other rooms and se if they intersect with this one.
        for other_room in rooms:
            if new_room.intersect(other_room):
                break;
        else:
            # this means there are no intersections, so this room is valid.

            # "paint" it to the map's tiles
            create_room(game_map, new_room);

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center();

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x;
                player.y = new_y;
            else:
                # all tooms after the first:                
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms -1].center();

                # flip a coin (random number that is either 0 or 1)
                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(game_map, prev_x, new_x, prev_y);
                    create_v_tunnel(game_map, prev_y, new_y, new_x);
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(game_map, prev_y, new_y, new_x);
                    create_h_tunnel(game_map, prev_x, new_x, prev_y);

            # place monsters.
            place_entities(new_room, entities, max_monsters_per_room, colors);

            # finally, append the new room to the list
            rooms.append(new_room);
            num_rooms += 1;