maps_by_screen = [
    # Screen 1
    [("MONKEY MEADOW", "BEGINNER"), ("IN THE LOOP", "BEGINNER"), ("MIDDLE OF THE ROAD", "BEGINNER"),
     ("TINKERTON", "BEGINNER"), ("TREE STUMP", "BEGINNER"), ("TOWN CENTER", "BEGINNER")],
    # Screen 2
    [("ONE TWO TREE", "BEGINNER"), ("SCRAPYARD", "BEGINNER"), ("THE CABIN", "BEGINNER"),
     ("RESORT", "BEGINNER"), ("SKATES", "BEGINNER"), ("LOTUS ISLAND", "BEGINNER")],
    # Screen 3
    [("CANDY FALLS", "BEGINNER"), ("WINTER PARK", "BEGINNER"), ("CARVED", "BEGINNER"),
     ("PARK PATH", "BEGINNER"), ("ALPINE RUN", "BEGINNER"), ("FROZEN OVER", "BEGINNER")],
    # Screen 4
    [("CUBISM", "BEGINNER"), ("FOUR CIRCLES", "BEGINNER"), ("HEDGE", "BEGINNER"),
     ("END OF THE ROAD", "BEGINNER"), ("LOGS", "BEGINNER")],
    # Screen 5
    [("LUMINOUS COVE", "INTERMEDIATE"), ("SULFUR SPRINGS", "INTERMEDIATE"), ("WATER PARK", "INTERMEDIATE"),
     ("POLYPHEMUS", "INTERMEDIATE"), ("COVERED GARDEN", "INTERMEDIATE"), ("QUARRY", "INTERMEDIATE")],
    # Screen 6
    [("QUIET STREET", "INTERMEDIATE"), ("BLOONARIUS PRIME", "INTERMEDIATE"), ("BALANCE", "INTERMEDIATE"),
     ("ENCRYPTED", "INTERMEDIATE"), ("BAZAAR", "INTERMEDIATE"), ("ADORA'S TEMPLE", "INTERMEDIATE")],
    # Screen 7
    [("SPRING SPRING", "INTERMEDIATE"), ("KARTSNDARTS", "INTERMEDIATE"), ("MOON LANDING", "INTERMEDIATE"),
     ("HAUNTED", "INTERMEDIATE"), ("DOWNSTREAM", "INTERMEDIATE"), ("FIRING RANGE", "INTERMEDIATE")],
    # Screen 8
    [("CRACKED", "ADVANCED"), ("STREAMBED", "ADVANCED"), ("CHUTES", "ADVANCED"),
     ("RAKE", "ADVANCED"), ("SPICE ISLANDS", "ADVANCED")],
    # Screen 9
    [("LAST RESORT", "ADVANCED"), ("ANCIENT PORTAL", "ADVANCED"), ("CASTLE REVENGE", "ADVANCED"),
     ("DARK PATH", "ADVANCED"), ("EROSION", "ADVANCED"), ("MIDNIGHT MANSION", "ADVANCED")],
    # Screen 10
    [("SUNKEN COLUMNS", "ADVANCED"), ("X FACTOR", "ADVANCED"), ("MESA", "ADVANCED"),
     ("GEARED", "ADVANCED"), ("SPILLWAY", "ADVANCED"), ("CARGO", "ADVANCED")],
    # Screen 11
    [("PAT'S POND", "ADVANCED"), ("PENINSULA", "ADVANCED"), ("HIGH FINANCE", "ADVANCED"),
     ("ANOTHER BRICK", "ADVANCED"), ("OFF THE COAST", "ADVANCED"), ("CORNFIELD", "ADVANCED")],
    # Screen 12
    [("UNDERGROUND", "ADVANCED")],
    # Screen 13
    [("GLACIAL TRAIL", "EXPERT"), ("DARK DUNGEONS", "EXPERT"), ("SANCTUARY", "EXPERT"),
     ("RAVINE", "EXPERT"), ("FLOODED VALLEY", "EXPERT"), ("INFERNAL", "EXPERT")],
    # Screen 14
    [("BLOODY PUDDLES", "EXPERT"), ("WORKSHOP", "EXPERT"), ("QUAD", "EXPERT"),
     ("DARK CASTLE", "EXPERT"), ("MUDDY PUDDLES", "EXPERT"), ("#OUCH", "EXPERT")]
]

# Function to print all maps with their difficulties for verification
def print_maps_by_screen():
    for i, screen in enumerate(maps_by_screen, 1):
        print(f"Screen {i}:")
        for map_name, difficulty in screen:
            print(f"  {map_name}: {difficulty}")

if __name__ == "__main__":
    print_maps_by_screen()