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

def run_app():
    while True:
        print_menu()
        action = input("Input action: ")
        if action == "1":
            explain_code()
        elif action == "2":
            find_bugs()
        elif action == "3":
            improve_code()
        elif action == "4":
            generate_tests()
        elif action == "5":
            break
        else:
            print("Invalid.")