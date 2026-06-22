import random

words = [
    "River",
    "Tiger",
    "Cloud",
    "Moon",
    "Coffee",
    "Sun",
    "Ocean"
]

password = (
    random.choice(words)
    + "!"
    + random.choice(words)
    + "#"
    + str(random.randint(10, 99))
)

print("Suggested Password:", password)
