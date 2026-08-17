# Text Based Game
# Robert Szabo

def introduction():
    # print an intro to the game
    print('Welcome to the Dracula Text Adventure Game!')
    print('------------------------------------------')
    print('You are an experienced monster hunter, and you have fought your way through the '
          'forest, defeating werewolves, lesser vampires, and other magical enemies to make'
          'it to Dracula’s castle and defeat him once and for all and earn the renown of', '\n' +
          'defeating the worlds oldest and most powerful vampire! Through your fighting, ', '\n' +
          'you’ve depleted your supplies. You will need to forage for more through the ', '\n' +
          'castle before attempting to fight Dracula! You will start in the foyer. You will' +
          'need garlic cloves from the kitchen, a wooden stake from the groundskeeper’s ', '\n' +
          'quarters, holy water from the chapel, silver bullets to reload your pistol '
          'from the armory, fuel from the garage, and matches from the study to ignite the fuel' +'\n' +
          'and burn the body after Dracula is defeated. Fortunately for you, it is the ', '\n' +
          'daytime, and he is sleeping in his coffin in the dungeon, so you should be able '
          'to move about the castle without disturbing him. However, if you should stumble '
          'into the dungeon unprepared, he will wake up and suck your blood, turning you ', '\n' +
          'into a vampire yourself!')


def instructions():
    # explain how to play the game
    print('Your move commands are: "Go North", "Go South", "Go East", "Go West".')
    print('------------------------------------------')
    print('Add to Inventory: Get "Item Name"')
    print('------------------------------------------')

def good_luck():
    print('Good luck with the game!')
    print('------------------------------------------')

def add_keys_nested_dict(d, keys):
    for key in keys:
        if key not in d:
            d[key] = {}
        d = d[key]
    d.setdefault(keys[-1], 1)

def add_item(current_room, rooms, inventory):
    inventory.append(rooms[current_room]['Item'])
    rooms_update = {'Item': ''}
    rooms[current_room].update(rooms_update)


def main():
    rooms = {
        'Foyer': {'East': 'Chapel', 'Item': ''},
        'Chapel': {'North': "Groundskeeper's Quarters", 'East': 'Armory', 'South': 'Kitchen',
                   'Item': 'Holy Water'},
        "Groundskeeper's Quarters": {'South': 'Chapel', 'East': 'Garage', 'Item': 'Wooden Stake'},
        'Garage': {'West': "Groundskeeper's Quarters", 'Item': 'Fuel'},
        'Armory': {'West': 'Chapel', 'North': 'Dungeon', 'Item': 'Silver Bullets'},
        'Kitchen': {'East': 'Study', 'North': 'Chapel', 'Item': 'Garlic Cloves'},
        'Study': {'West': 'Kitchen', 'Item': 'Matches'}
    }

    # create empty inventory as a list
    inventory = []

    # create variable for starting room
    starting_room = 'Foyer'

    # assign starting room variable to new variable, current room
    current_room = starting_room

    introduction()

    instructions()

    good_luck()

    while True:
        # encountering the villain
        if current_room == 'Dungeon':
            # winning the game
            if len(inventory) == 6:
                print('You enter the dungeon to find Dracula asleep, ', '\n' +
                      'luckily you were prepared with all you needed to defeat him', '\n' +
                      'you place the garlic around your neck and douse him with holy water', '\n' +
                      'he wakes up with a start, and you shoot him with a silver bullet,', '\n' +
                      'following it up with a stab through the heart with a stake.', '\n' +
                      'You have defeated Dracula, so you douse him in fuel and toss', '\n' +
                      'a lit match on his corpse, freeing the world of his terror!', '\n' +
                      'Congratulations! You win the game! Thanks for playing!')
                break
            # losing the game
            else:
                print('You enter the dungeon to find Dracula asleep.', '\n' +
                      'You take a step and he sits upright in his coffin', '\n' +
                      'staring directly at you with blood lust. The last', '\n' +
                      'words you hear are "I vant to suck your blood!"')
                print('Thanks for playing! Better luck next time!')
                break

        # tell user their current room and inventory
        print('You are in the {}'.format(current_room))
        print('------------------------------------------')

        if not inventory:  # empty inventory
            print('Your inventory is empty.')
            print('------------------------------------------')
        else:  # if items in inventory list
            print('Your inventory contains:', ', '.join(inventory))
            print('------------------------------------------')

        # notify the player of any items in the room
        if current_room != 'Dungeon' and 'Item' in rooms[current_room].keys():
            if rooms[current_room]['Item'] != '':
                print('In this room you see the {}. You\'re going to need that!'.format(rooms[current_room]['Item']))
                print('------------------------------------------')

        # tell player to enter a new command
        command = input('Enter your command:').split()[-1].capitalize()
        print('------------------------------------------')

        # exit the game
        if command == 'Exit':
            print('Thank you for playing the game! Hope you had a good time!')
            break

        # move around
        elif command in rooms[current_room]:
            current_room = rooms[current_room][command]

        # adding item to inventory
        elif command in rooms[current_room]['Item']:
            print('You got the {}.'.format(rooms[current_room]['Item']))
            print('------------------------------------------')
            add_item(current_room, rooms, inventory)
            continue

        # bad input
        else:
            print('That command is invalid.')
            print('------------------------------------------')
            continue

main()
