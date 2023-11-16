import cmd
import json
import os
import time
from http import HTTPStatus

from colorama import Fore

from dialogue import DialogueType
from enchantus_api_client import EnchantusAPIClient

os.system('cls')

fixed_time_delay = 1
print(Fore.GREEN + "Welcome to the Enchantus API Client Example!")
time.sleep(fixed_time_delay)
print(Fore.WHITE + "This is a live example which will use the Enchantus API Client to create an entity and generate "
                   "dialogue.")
time.sleep(fixed_time_delay)
print("First, we'll create an Enchantus API Client.")
time.sleep(fixed_time_delay)

print("You'll need to provide your API token to the constructor. We have hidden our API token in this example.")
print(Fore.YELLOW + "\tRemember, you should never share your API token with anyone!")
time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)
print(Fore.LIGHTBLUE_EX + "\n> client = EnchantusAPIClient(api_token='******')\n\n")
client = EnchantusAPIClient(api_token='ortexADZbT4wE20xrKm9dCvFbOJG15m9RQlhEei0')

print(Fore.WHITE + "Next, we'll create an entity. An entity is a character or person that you want to generate "
                   "dialogue for.\n\n")
time.sleep(fixed_time_delay)

print("You can create an entity by calling the create_entity method on the client.")
time.sleep(fixed_time_delay)
print("The entity details are a dictionary of information about the entity.")
time.sleep(fixed_time_delay)
print("These details influences the quality of generated dialogue.")
time.sleep(fixed_time_delay)
print("There is no specific format for this dictionary.")
time.sleep(fixed_time_delay)
print("It should contain information that you think is relevant to the entity.")
time.sleep(fixed_time_delay)
print("If your entity is not using the right tone or style, try adjusting the details.\n\n")
time.sleep(fixed_time_delay)
print("We're going to create an entity for Jerry Seinfeld.")
time.sleep(fixed_time_delay)
print("We'll start by defining character details.\n\n")
time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)

print(Fore.LIGHTBLUE_EX + "> entity_details = {")
time.sleep(0.1)
print("      'occupation': 'comedian',")
time.sleep(0.1)
print("      'hobbies': 'stand-up comedy, writing, dating, hanging out with friends',")
time.sleep(0.1)
print("      'favorite_food': 'cereal',")
time.sleep(0.1)
print("      'favorite_tv_show': 'Seinfeld',")
time.sleep(0.1)
print("      'favorite_superhero': 'Superman',")
time.sleep(0.1)
print("      'friends': ['George Costanza', 'Elaine Benes', 'Cosmo Kramer'],")
time.sleep(0.1)
print("      'enemies': ['Newman', 'Babu Bhatt', 'Uncle Leo'],")
time.sleep(0.1)
print("      'fears': ['clowns', 'spiders', 'public speaking'],")
time.sleep(0.1)
print("      'dreams': ['become a successful comedian', 'get married', 'have kids'],")
time.sleep(0.1)
print("      'family': {")
time.sleep(0.1)
print("          'parents': ['Morty Seinfeld', 'Helen Seinfeld'],")
time.sleep(0.1)
print("          'siblings': ['Uncle Leo', 'Aunt Stella'],")
time.sleep(0.1)
print("      },")
time.sleep(0.1)
print("      'example_dialogues': [")
time.sleep(0.1)
print("          'What\'s the deal with airline food?',")
time.sleep(0.1)
print("          'I mean, it\'s like, you\'re on a plane, and they give you food. What\'s the deal with that?',")
time.sleep(0.1)
print("          'I don\'t know, I guess it\'s just a service they provide.',")
time.sleep(0.1)
print("          'Yeah, but it\'s like, why do they give you food? I mean, you\'re on a plane. You\'re not supposed to "
      "be eating.',")
time.sleep(0.1)
print("      ],")
time.sleep(0.1)
print("  }\n\n")
time.sleep(fixed_time_delay)

entity_details = {
    'occupation': 'comedian',
    'hobbies': 'stand-up comedy, writing, dating, hanging out with friends',
    'favorite_food': 'cereal',
    'favorite_tv_show': 'Seinfeld',
    'favorite_superhero': 'Superman',
    'friends': ['George Costanza', 'Elaine Benes', 'Cosmo Kramer'],
    'enemies': ['Newman', 'Babu Bhatt', 'Uncle Leo'],
    'fears': ['clowns', 'spiders', 'public speaking'],
    'dreams': ['become a successful comedian', 'get married', 'have kids'],
    'family': {
        'parents': ['Morty Seinfeld', 'Helen Seinfeld'],
        'siblings': ['Uncle Leo', 'Aunt Stella'],
    },
    'example_dialogues': [
        'What\'s the deal with airline food?',
        'I mean, it\'s like, you\'re on a plane, and they give you food. What\'s the deal with that?',
        'I don\'t know, I guess it\'s just a service they provide.',
        'Yeah, but it\'s like, why do they give you food? I mean, you\'re on a plane. You\'re not supposed to be '
        'eating.',
    ],
}

print(Fore.WHITE + "Great! Now we'll create the entity itself.")
time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)
print(Fore.LIGHTBLUE_EX + "\n> entity, resp = client.create_entity(name='Jerry Seinfeld', details=entity_details)\n\n")
time.sleep(fixed_time_delay)

entity, resp = client.create_entity(name='Jerry Seinfeld', details=entity_details)

if resp.status_code != HTTPStatus.CREATED:
    # Print error message and response code
    print(f"Error: status code {resp.status_code} - {resp.reason}")
    exit(1)
else:
    print(Fore.LIGHTBLUE_EX + 'Create Entity Response:\n', json.dumps(entity.to_dict(), indent=4))

print(Fore.WHITE + "\n\nThe create_entity method returns a tuple of the entity object and the response from the API.")
time.sleep(fixed_time_delay)
print("The entity object contains the entity's ID, name, and details.")
time.sleep(fixed_time_delay)
print("Save the entity ID somewhere, because you'll need it to generate dialogue. You can also use the entity ID to "
      "update the entity's details at any time.\n\n")
time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)
print("Now you can use this character to generate dialogue!")
time.sleep(fixed_time_delay)
print("Let's try it out.")
time.sleep(fixed_time_delay)
print("First, we may start by creating some initial dialogue.")
time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)
print(
    Fore.LIGHTBLUE_EX + "\n> added_dialogue, resp = client.add_dialogue(dialogue_type=DialogueType.NPC, content='Well "
                        "hello there!', actor_id=entity.id)\n\n")
time.sleep(fixed_time_delay)

# Example usage of the API client
# Add a new dialogue
added_dialogue, resp = client.add_dialogue(
    dialogue_type=DialogueType.NPC,
    content='Well hello there!',
    actor_id=entity.id,
)

if added_dialogue is None:
    # Print error message and response code
    print(Fore.RED + f"Error: status code {resp.status_code} - {resp.reason}")
else:
    print(Fore.LIGHTBLUE_EX + 'Add Dialogue Response:\n', json.dumps(added_dialogue.to_dict(), indent=4))

time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)

print(Fore.LIGHTBLUE_EX + "\n> added_dialogue, resp = client.add_dialogue(dialogue_type=DialogueType.NPC, "
                          "content='Elaine and I have decided to play a little game with everyone. We\'re doing this "
                          "new thing called \'LARPing\'.', actor_id=entity.id, parent_id=added_dialogue.id)\n\n")

# Add a follow-up dialogue
added_dialogue, resp = client.add_dialogue(
    dialogue_type=DialogueType.NPC,
    content='Elaine and I have decided to play a little game with everyone. We\'re doing this new thing ' \
            'called \'LARPing\'.',
    actor_id=entity.id,
    parent_id=added_dialogue.id,
)

if added_dialogue is None:
    # Print error message and response code
    print(Fore.RED + resp.json())
else:
    print(Fore.LIGHTBLUE_EX + 'Add Dialogue Response:\n', json.dumps(added_dialogue.to_dict(), indent=4))

print(Fore.WHITE + "\n\nThe add_dialogue method returns a tuple of the dialogue object and the response from the API.")
time.sleep(fixed_time_delay)
print("The dialogue object contains the dialogue's ID, type, content, actor ID, and parent ID.")
time.sleep(fixed_time_delay)
print("Now let's generate a follow-up dialogue.")
time.sleep(fixed_time_delay)
print("This is created dynamically by the API using cutting-edge GenAI technology based on the dialogue you just "
      "created.")

time.sleep(fixed_time_delay)
time.sleep(fixed_time_delay)

print(Fore.LIGHTBLUE_EX + "\n> generated_dialogue, resp = client.generate_dialogue(parent_id=added_dialogue.id, "
                          "actor_id=entity.id)\n\n")
time.sleep(fixed_time_delay)

# Generate a dialogue
generated_dialogue, resp = client.generate_dialogue(parent_id=added_dialogue.id, actor_id=entity.id)

if generated_dialogue is None:
    # Print error message and response code
    print(Fore.RED + resp.json())
else:
    print(Fore.LIGHTBLUE_EX + 'Generate Dialogue Response:\n', json.dumps(generated_dialogue.to_dict(), indent=4))

time.sleep(fixed_time_delay)
print(Fore.GREEN + "\n\nCongratulations! You've successfully created your first character and dialogue!")
print("Feel free to play around with the API and create your own characters and dialogues.")
