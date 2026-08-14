from features import explain_code, find_bugs, improve_code, generate_tests

def print_menu():
    print("========================")
    print(" AI Developer Assistant ")
    print("========================")
    print("1. Explain code")
    print("2. Find bugs")
    print("3. Improve code")
    print("4. Generate tests")
    print("5. Exit")

def main():
    while True:
        print_menu()
        action = input("Input action: ")

        match action:
            case "1":
                explain_code()
            case "2":
                find_bugs()
            case "3":
                improve_code()
            case "4":
                generate_tests()
            case "5":
                break
            case _:
                print("Invalid.")