def save_name(name):
    with open("name.txt", "w") as file:
        file.write(name)
def load_name():
    try:
        with open("name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
    