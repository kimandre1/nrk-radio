import yaml 



"""
Håndterer tilkobling mot .yml og .env filer samt hva enn andre api'er vi føler for etterhvert.
"""

def connect_bot():
    with open("config.yml", "r") as yml_file:
        config = yaml.safe_load(yml_file)
    return (config["discord"]["apikey"])

# Henter kanalene fra liste

def get_channels():
    with open("channels.env", 'r') as file:
        lines = file.readlines()
    channel_names = [line.split('=')[0].strip() for line in lines]
    formatted_channels = "\n".join(f"{idx + 1}. {name}" for idx, name in enumerate(channel_names))
    
    return f"**Tilgjengelige kanaler:**\n{formatted_channels}"


# Kanalvelger
def select_channel(channel_name):
    try:
        with open("channels.env", "r") as file:
            channels = file.readlines()
            for channel in channels:
                if '=' in channel:
                    name, url = channel.split("=", 1)
                    if channel_name.lower() == name.strip().lower():
                        return url.strip()
        return None
    except FileNotFoundError:
        print(f"Feil!! finner ikke channels.env fil")
    except Exception as e:
        print(f"oi faen! her erre noe feil: {e}")
    return None
          
if __name__ == "__main__":
    
    
    print(select_channel("NRK hedmark"))
        