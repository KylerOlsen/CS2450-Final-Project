
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
    nouns = [
        "Cello", "Badger", "Fish", "Apple", "Mountain", "River", "Teacher",
        "Book", "Car", "Tree", "Dog", "House", "Chair", "Phone", "Computer",
        "City", "Ocean", "Guitar", "Desk", "Flower", "Star", "Sky", "Window",
        "Road", "Train", "Plane", "School", "Garden", "Table", "Bottle",
        "Shirt", "Door", "Bridge", "Watch", "Camera", "Bag", "Pencil", "Cup",
        "Hat", "Wall", "Cloud", "Island", "Forest", "Room", "Engine", "Shoe",
        "Candle", "Bed", "Lamp", "Mirror", "Clock", "Keyboard", "Mouse",
        "Blanket", "Pillow", "Soap", "Towel", "Toothbrush", "Backpack",
        "Basket", "Fan", "Television", "Magazine", "Newspaper", "Statue",
        "Painting", "Ladder", "Fence", "Rope", "Ball", "Drum", "Violin",
        "Microphone", "Box", "Shelf", "Ring", "Necklace", "Coin", "Wallet",
        "Purse", "Ticket", "Key", "Lock", "Brush", "Comb", "Notebook",
        "Envelope", "Stamp", "Hammer", "Screwdriver", "Nail", "Saw", "Plank",
        "Brick", "Tile", "Carpet", "Curtain", "Apron", "Oven", "Refrigerator",
        "Blender", "Pot", "Pan",
    ]

    return random.choice(adjectives).capitalize() + random.choice(nouns)

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
