import json
import random

def parse_name(full_name):
    """
    Splits the full name into firstName and lastName.
    This is a simple heuristic:
       - lastName is the last token
       - firstName is everything before
    """
    tokens = full_name.strip().split()
    if len(tokens) == 1:
        return full_name, ""  # No clear lastName
    else:
        return " ".join(tokens[:-1]), tokens[-1]

def infer_sex_from_model(model_type):
    """
    A simple inference: if 'female' is in model_type (case-insensitive), mark sex as 'female';
    if 'male' is in model_type, mark as 'male';
    otherwise, 'unknown'.
    """
    model_type_lower = model_type.lower()
    if 'female' in model_type_lower:
        return 'female'
    elif 'male' in model_type_lower:
        return 'male'
    else:
        return 'unknown'

def convert_wagon_to_new_json_structure(wagon_data):
    """
    Given one wagon's data:
      {
        "id": 1,
        "theme": "...",
        "passcode": "...",
        "passengers": [ {...}, ... ]
      }

    Returns three pieces of data:
      1) wagonNames   -> for the "names" array
      2) wagonDetails -> for the "player_details" array
      3) wagonEntry   -> for the "wagons" array
    """
    wagon_id = wagon_data.get("id", 0)
    theme = wagon_data.get("theme", "Unknown Theme")
    passcode = wagon_data.get("passcode", "no-passcode")
    passengers = wagon_data.get("passengers", [])

    # Example: wagon_id = 1 -> wagonKey = "wagon-1"
    wagon_key = f"wagon-{wagon_id}"

    # 1) Build an object for "names"
    #    Format: {
    #       "wagonId": "wagon-1",
    #       "players": [
    #          { "playerId": "player-1", "firstName": "...", "lastName": "...", "sex": "...", "fullName": "..." },
    #          ...
    #       ]
    #    }
    wagonNames = {
        "wagonId": wagon_key,
        "players": []
    }

    # 2) Build an object for "player_details"
    #    Format: {
    #       "wagonId": "wagon-1",
    #       "players": [
    #          {
    #            "playerId": "player-1",
    #            "profile": { "name": "...", "age": 47, ...}
    #          },
    #          ...
    #       ]
    #    }
    wagonDetails = {
        "wagonId": wagon_key,
        "players": []
    }

    # 3) Build the "wagons" array entry
    #    Format:
    #    {
    #      "id": 1,
    #      "theme": "...",
    #      "passcode": "...",
    #      "people": [
    #         {
    #           "uid": "wagon-1-player-1",
    #           "position": [0.23, 0.77],
    #           "rotation": 0.55,
    #           "model_type": "...",
    #           "items": []
    #         }
    #      ]
    #    }
    wagonEntry = {
        "id": wagon_id,
        "theme": theme,
        "passcode": passcode,
        "people": []
    }

    # For each passenger, create the entries in "names", "player_details", and "wagons"
    for i, passenger in enumerate(passengers, start=1):
        player_key = f"player-{i}"
        full_name = passenger.get("name", "Unknown")
        first_name, last_name = parse_name(full_name)

        model_type = passenger.get("characer_model", "character-unknown")
        sex = infer_sex_from_model(model_type)

        # -- "names" --
        wagonNames["players"].append({
            "playerId": player_key,
            "firstName": first_name,
            "lastName": last_name,
            "sex": sex,
            "fullName": full_name
        })

        # -- "player_details" --
        profile_dict = {
            "name": full_name,
            "age": passenger.get("age", 0),
            "profession": passenger.get("profession", ""),
            "personality": passenger.get("personality", ""),
            "role": passenger.get("role", ""),
            "mystery_intrigue": passenger.get("mystery_intrigue", "")
        }
        wagonDetails["players"].append({
            "playerId": player_key,
            "profile": profile_dict
        })

        # -- "wagons" (the "people" list) --
        person_dict = {
            "uid": f"wagon-{wagon_id}-player-{i}",
            # random position in [0..1], random rotation in [0..1]
            "position": [round(random.random(), 2), round(random.random(), 2)],
            "rotation": round(random.random(), 2),
            "model_type": model_type,
            "items": []
        }
        wagonEntry["people"].append(person_dict)

    return wagonNames, wagonDetails, wagonEntry

def convert_and_return_jsons(wagon_data):
    """
    Takes a list of wagons. For each wagon, we build its piece of:
      - wagonNames (for final "names" array)
      - wagonDetails (for final "player_details" array)
      - wagonEntry (for final "wagons" array)
    Then merges them into the new combined JSON structure:

    {
      "player_details": [ { ... }, { ... } ],
      "wagons": [ { ... }, { ... } ],
      "names": [ { ... }, { ... } ]
    }
    """
    names_list = []
    player_details_list = []
    wagons_list = []

    for wagon in wagon_data:
        # Convert one wagon to the new partial outputs
        wagonNames, wagonDetails, wagonEntry = convert_wagon_to_new_json_structure(wagon)
        # Accumulate them
        names_list.append(wagonNames)
        player_details_list.append(wagonDetails)
        wagons_list.append(wagonEntry)

    # Now build the final JSON structure
    final_data = {
        "player_details": player_details_list,
        "wagons": wagons_list,
        "names": names_list
    }
    return final_data