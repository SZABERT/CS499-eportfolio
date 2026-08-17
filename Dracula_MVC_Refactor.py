# Text Based Game - MVC Refactor
# Author: Robert Szabo
# Enhanced for CS 499

class GameModel:
    """The Model handles data, state, and game logic."""
    def __init__(self):
        # The map is currently a dictionary (to be upgraded to a Graph in Milestone 3)
        self.rooms = {
            'Foyer': {'East': 'Chapel', 'Item': ''},
            'Chapel': {'North': "Groundskeeper's Quarters", 'East': 'Armory', 'South': 'Kitchen', 'Item': 'Holy Water'},
            "Groundskeeper's Quarters": {'South': 'Chapel', 'East': 'Garage', 'Item': 'Wooden Stake'},
            'Garage': {'West': "Groundskeeper's Quarters", 'Item': 'Fuel'},
            'Armory': {'West': 'Chapel', 'North': 'Dungeon', 'Item': 'Silver Bullets'},
            'Kitchen': {'East': 'Study', 'North': 'Chapel', 'Item': 'Garlic Cloves'},
            'Study': {'West': 'Kitchen', 'Item': 'Matches'},
            'Dungeon': {'Item': ''} # Boss room
        }
        self.inventory = []
        self.current_room = 'Foyer'
        
        # Dynamically calculate the number of items needed to win (removing the "magic number")
        self.total_items_needed = sum(1 for room in self.rooms.values() if room.get('Item') != '')

    def move_player(self, direction):
        """Attempts to move the player in a given direction."""
        if direction in self.rooms[self.current_room]:
            self.current_room = self.rooms[self.current_room][direction]
            return True
        return False

    def get_item(self, item_name):
        """Attempts to add an item to the inventory."""
        room_item = self.rooms[self.current_room].get('Item', '')
        if room_item.lower() == item_name.lower():
            self.inventory.append(room_item)
            self.rooms[self.current_room]['Item'] = ''  # Remove item from room
            return True
        return False

    """
    WIN CONDITION EXPLANATION:
    To win the game, the player must collect all required items scattered throughout 
    the castle before entering the Dungeon to face Dracula. The 6 required items are:
    1. Garlic Cloves (Kitchen)
    2. Wooden Stake (Groundskeeper's Quarters)
    3. Holy Water (Chapel)
    4. Silver Bullets (Armory)
    5. Fuel (Garage)
    6. Matches (Study)
    If the player enters the Dungeon without a full inventory, the check_win_condition 
    returns False, triggering the loss sequence.
    """
    def check_win_condition(self):
        """Checks if the player has gathered all necessary items."""
        return len(self.inventory) == self.total_items_needed

class GameView:
    """The View handles all terminal output and user input."""
    @staticmethod
    def print_separator():
        print('-' * 42)

    def display_introduction(self):
        print('Welcome to the Dracula Text Adventure Game!')
        self.print_separator()
        
        # Using a multi-line string for clean formatting
        intro_text = """You are an experienced monster hunter, and you have fought your way through the
forest, defeating werewolves, lesser vampires, and other magical enemies to make
it to Dracula’s castle and defeat him once and for all and earn the renown of
defeating the worlds oldest and most powerful vampire! Through your fighting,
you’ve depleted your supplies. You will need to forage for more through the
castle before attempting to fight Dracula! You will start in the foyer. You will
need garlic cloves from the kitchen, a wooden stake from the groundskeeper’s
quarters, holy water from the chapel, silver bullets to reload your pistol
from the armory, fuel from the garage, and matches from the study to ignite the fuel
and burn the body after Dracula is defeated. Fortunately for you, it is the
daytime, and he is sleeping in his coffin in the dungeon, so you should be able
to move about the castle without disturbing him. However, if you should stumble
into the dungeon unprepared, he will wake up and suck your blood, turning you
into a vampire yourself!"""
        
        print(intro_text)
        self.print_separator()
        print('Commands: "Go North", "Go South", "Go East", "Go West", "Get [Item]", "Exit"')
        self.print_separator()

    def display_status(self, current_room, inventory, room_item):
        print(f'You are in the {current_room}')
        
        if not inventory:
            print('Your inventory is empty.')
        else:
            print(f'Your inventory contains: {", ".join(inventory)}')
            
        if room_item:
            print(f'In this room you see the {room_item}. You\'re going to need that!')
        self.print_separator()

    def display_message(self, message):
        print(message)
        self.print_separator()

    def get_user_input(self):
        """Safely gets input from the user."""
        try:
            return input('Enter your command: ').strip().split()
        except EOFError:
            return []

class GameController:
    """The Controller manages the game loop and orchestrates Model and View."""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_running = True

    def run_game(self):
        self.view.display_introduction()

        while self.is_running:
            # Check for boss encounter
            if self.model.current_room == 'Dungeon':
                self.handle_boss_encounter()
                break

            # Display current room state
            current_item = self.model.rooms[self.model.current_room].get('Item', '')
            self.view.display_status(self.model.current_room, self.model.inventory, current_item)

            # Get and parse input safely
            command_parts = self.view.get_user_input()
            
            if not command_parts:
                self.view.display_message("Please enter a valid command.")
                continue

            action = command_parts[0].capitalize()
            
            if action == 'Exit':
                self.view.display_message("Thank you for playing! Goodbye.")
                self.is_running = False

            elif action == 'Go' and len(command_parts) > 1:
                direction = command_parts[1].capitalize()
                if not self.model.move_player(direction):
                    self.view.display_message("You cannot go that way.")

            elif action == 'Get' and len(command_parts) > 1:
                item_name = " ".join(command_parts[1:]) # Reconstruct multi-word items
                if self.model.get_item(item_name):
                    self.view.display_message(f"You got the {item_name.title()}.")
                else:
                    self.view.display_message("That item is not here.")
            else:
                self.view.display_message("Invalid command format. Use 'Go [Direction]' or 'Get [Item]'.")

    def handle_boss_encounter(self):
        """Processes the win/loss logic for the final room."""
        if self.model.check_win_condition():
            self.view.display_message(
                'You enter the dungeon to find Dracula asleep.\n'
                'Luckily you were prepared! You douse him with holy water,\n'
                'shoot him with a silver bullet, and stab him with the stake.\n'
                'Congratulations! You win the game!'
            )
        else:
            self.view.display_message(
                'You enter the dungeon to find Dracula asleep.\n'
                'You step forward unprepared, and he sits upright in his coffin!\n'
                'The last words you hear are "I vant to suck your blood!"\n'
                'Game Over. Better luck next time!'
            )

if __name__ == "__main__":
    # Initialize components and start the game
    game_model = GameModel()
    game_view = GameView()
    controller = GameController(game_model, game_view)
    controller.run_game()