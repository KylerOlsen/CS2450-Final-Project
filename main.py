# Kyler Olsen
# CS 2450 Final Project
# Apr 2025

import random

def name_gen():
    adjectives = [
        "able", "active", "adaptable", "adventurous", "agreeable", "alert",
        "amazing", "amiable", "ample", "artistic", "attractive", "balanced",
        "beautiful", "blissful", "bold", "brave", "bright", "brilliant",
        "bubbly", "calm", "capable", "careful", "charming", "cheerful", "clean",
        "clear", "clever", "colorful", "comfortable", "compassionate",
        "confident", "considerate", "cool", "cooperative", "courageous",
        "creative", "cultured", "cute", "daring", "decent", "delightful",
        "detailed", "determined", "dignified", "disciplined", "dynamic",
        "eager", "easygoing", "elegant", "energetic", "engaging",
        "enthusiastic", "excellent", "exciting", "expressive", "fair",
        "faithful", "fancy", "fascinating", "flexible", "focused", "friendly",
        "fun", "funny", "generous", "gentle", "genuine", "gifted", "glad",
        "gleaming", "good", "graceful", "gracious", "great", "handsome",
        "happy", "harmonious", "helpful", "honest", "hopeful", "humble",
        "imaginative", "impressive", "independent", "innocent", "inspiring",
        "intelligent", "interesting", "intuitive", "jolly", "jovial", "joyful",
        "kind", "lively", "logical", "lovely", "loyal", "lucky", "mature",
        "mindful", "modest",
    ]
    animals = [
        "aardvark", "albatross", "alligator", "alpaca", "ant", "anteater",
        "antelope", "ape", "armadillo", "baboon", "badger", "barracuda", "bat",
        "bear", "beaver", "bee", "beetle", "bison", "boar",
        "bobcat", "buffalo", "butterfly", "camel", "canary", "capybara",
        "caracal", "caribou", "cassowary", "cat", "caterpillar", "cattle",
        "chameleon", "cheetah", "chicken", "chimpanzee", "chinchilla", "cobra",
        "cockatoo", "cougar", "cow", "coyote", "crab", "crane", "crocodile",
        "crow", "deer", "dingo", "dog", "dolphin", "donkey", "dove",
        "dragonfly", "duck", "eagle", "echidna", "eel", "elephant", "elk",
        "emu", "falcon", "ferret", "finch", "firefly", "fish", "flamingo",
        "fly", "fox", "frog", "gazelle", "gecko", "giraffe", "goat", "goldfish",
        "goose", "gorilla", "grasshopper", "pig", "gull", "hamster",
        "hare", "hawk", "hedgehog", "hippopotamus", "horse",
        "hummingbird", "hyena", "iguana", "jackal", "jaguar",
        "jellyfish", "kangaroo", "kingfisher", "koala", "lemur",
        "leopard", "lion", "lizard", "llama",
    ]

    return random.choice(adjectives).capitalize() + random.choice(animals).capitalize()

def server(host: str='', port: int=7788):
    from library import Library
    lib = Library(host, port)
    lib.serve_forever()

def client(playername: str, host: str='localhost', port: int=7788):
    from ui import UI
    ui = UI(playername, host, port)
    ui.loop()

def main():
    client(name_gen())

if __name__ == "__main__":
    main()
