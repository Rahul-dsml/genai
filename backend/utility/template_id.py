import random

# TEMPLATE_IDS = {
#     "sad": ["61579", "8072285", "56225174"],  # One Does Not Simply, Crying Jordan, Sad Pablo Escobar
#     "funny": ["112126428", "438680", "124822590"],  # Distracted Boyfriend, Batman Slapping Robin, Blank White Template
#     "angry": ["181913649", "97984", "89370399"],  # Drakeposting, Angry Obama, Gru's Plan
#     "disappointed": ["259680", "101470", "178591752"],  # Third World Skeptical Kid, Condescending Wonka, Buff Doge vs Cheems
# }



# Extended categories
TEMPLATE_IDS = {
    "funny": [
        "181913649",  # Drake Hotline Bling
        "112126428",  # Distracted Boyfriend
        "124822590",  # Left Exit 12 Off Ramp
        "438680",     # Batman Slapping Robin
        "252600902",  # Always Has Been
        "196652226",  # Spongebob Ight Imma Head Out
        "91998305",   # Drake Blank
    ],
    "sad": [
        "80707627",  # Sad Pablo Escobar
        "56225174",  # Sad Pablo Escobar 2
        "97984",     # Disaster Girl
        "50421420",  # Disappointed Black Guy
        "4087833",   # Waiting Skeleton
        "131940431", # Gru's Plan
    ],
    "happy": [
        "61520",      # Futurama Fry
        "178591752",  # Tuxedo Winnie The Pooh
        "61544",      # Success Kid
        "123999232",  # The Scroll Of Truth
        "5496396",    # Leonardo DiCaprio Cheers
    ],
    "angry": [
        "89370399",   # Roll Safe Think About It
        "134797956",  # American Chopper Argument
        "52975953",   # Look At Me
        "84341851",   # Evil Kermit
        "114585149",  # Inhaling Seagull
    ],
    "sarcastic": [
        "102156234",  # Mocking Spongebob
        "284929871",  # They Don't Know
        "259237855",  # Laughing Leo
        "145139900",  # Scooby Doo Mask Reveal
        "72525473",   # Say the Line Bart
    ],
    "relatable": [
        "61532",      # The Most Interesting Man In The World
        "101470",     # Y U No
        "3218037",    # This Is Fine
        "61556",      # Grandmother Finds The Internet
        "100777631",  # Is This A Pigeon?
    ],
    "wholesome": [
        "1035805",    # Boardroom Suggestion
        "27813981",   # Who Would Win?
        "89370399",   # Roll Safe Think About It
        "222403160",  # Among Us Drip
        "4087833",    # Waiting Skeleton
    ],
    "motivational": [
        "8072285",    # Crying Michael Jordan
        "405658",     # Confession Bear
        "61544",      # Success Kid
        "17496002",   # X All The Y
        "14292065",   # I Have No Idea What I’m Doing
    ],
    "sarcastic-positive": [
        "16464531",   # But That’s None Of My Business
        "101511",     # Awkward Moment Sealion
        "92214739",   # Aaaaand It’s Gone
        "74191766",   # Tired SpongeBob
        "132769734",  # Hard To Swallow Pills
    ],
    "work": [
        "563423",     # What Do You Want Me To Do?
        "1035805",    # Boardroom Suggestion
        "21604248",   # Grumpy Cat
        "74191766",   # Tired SpongeBob
        "61532",      # The Most Interesting Man In The World
    ],
    "sports": [
        "129242436",  # Surprised Pikachu
        "6235864",    # Evil Toddler
        "188390779",  # Buff Doge vs Cheems
        "129242436",  # Surprised Pikachu
        "8072285",    # Crying Michael Jordan
    ],
    "school": [
        "61546",      # Ancient Aliens
        "61585",      # Bad Luck Brian
        "1232104",    # Professor Oak
        "89370399",   # Roll Safe Think About It
        "124822590",  # Left Exit 12 Off Ramp
    ],
    "technology": [
        "89370399",   # Roll Safe Think About It
        "102156234",  # Mocking SpongeBob
        "178591752",  # Tuxedo Winnie The Pooh
        "61544",      # Success Kid
        "132769734",  # Hard To Swallow Pills
    ],
    "gaming": [
        "61579",      # One Does Not Simply
        "61532",      # The Most Interesting Man In The World
        "100777631",  # Is This A Pigeon?
        "196652226",  # Spongebob Ight Imma Head Out
        "129242436",  # Surprised Pikachu
    ],
    "relationship": [
        "112126428",  # Distracted Boyfriend
        "132769734",  # Hard To Swallow Pills
        "123999232",  # The Scroll Of Truth
        "259237855",  # Laughing Leo
        "4087833",    # Waiting Skeleton
    ]
}



def get_random_template(category):
    templates = TEMPLATE_IDS.get(category)
    if not templates:
        raise ValueError(f"No templates found for category '{category}'")
    return random.choice(templates)


import requests

def generate_meme(template_id, text0, username, password):
    url = "https://api.imgflip.com/caption_image"
    payload = {
        "template_id": template_id,
        "username": "g_user_116826138871546871081",
        "password": "hackathon",
        "text0": text0,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()

        response_data = response.json()
        if response_data.get("success"):
            meme_url = response_data["data"]["url"]
            print(f"Generated Meme: {meme_url}")
            return meme_url
        else:
            print(f"Error: {response_data.get('error_message', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Imgflip API: {e}")
        return None