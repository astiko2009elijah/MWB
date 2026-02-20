# Habit Tracker with Multiple Users

import json
import os
import tempfile

users = {}
# Example structure:
# {
#   "Alice": {
#       "Exercise": [1, 0, 1, 1, 0, 1, 0],
#       "Read":     [1, 1, 1, 0, 0, 1, 1]
#   },
#   "Bob": {
#       "Meditation": [1, 1, 0, 1, 1, 0, 1]
#   }
# }

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def add_user(username):
    """
    Add a new user to the tracker.
    """
    if username in users:
        print(f"User '{username}' already exists.")
        return False
    users[username] = {}
    print(f"User '{username}' created successfully.")
    save_users()
    return True

def add_habit(username, name):
    """
    Add a new habit for a user with 7 days initialized to 0.
    """
    if username not in users:
        print(f"User '{username}' does not exist.")
        return False
    if name in users[username]:
        print(f"Habit '{name}' already exists for {username}.")
        return False
    users[username][name] = [0] * 7
    print(f"Habit '{name}' added for {username}.")
    save_users()
    return True

def mark_done(username, habit_name, day_index):
    """
    Mark a habit as done (1) for a given day.
    """
    if username not in users:
        print(f"User '{username}' does not exist.")
        return False
    if habit_name not in users[username]:
        print(f"Habit '{habit_name}' does not exist for {username}.")
        return False
    if day_index < 0 or day_index > 6:
        print("Invalid day index. Must be between 0 and 6.")
        return False
    users[username][habit_name][day_index] = 1
    print(f"Marked '{habit_name}' as done for {username} on {DAYS[day_index]}.")
    save_users()
    return True


def users_file_path():
    return os.path.join(os.path.dirname(__file__), "users.json")


def save_users():
    """Atomically save `users` to users.json in the same folder."""
    path = users_file_path()
    data = users
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dirpath)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except Exception:
            pass


def load_users():
    """Load users from users.json if present."""
    path = users_file_path()
    global users
    if not os.path.exists(path):
        users = {}
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = {}

def weekly_total(username, habit_name):
    """
    Return how many days the habit was completed for a user.
    """
    if username not in users or habit_name not in users[username]:
        return 0
    return sum(users[username][habit_name])

def show_user_summary(username):
    """
    Print a summary of all habits for a specific user.
    """
    if username not in users:
        print(f"User '{username}' does not exist.")
        return
    
    if not users[username]:
        print(f"{username} has no habits yet.")
        return
    
    print(f"\n--- {username}'s Habits ---")
    for habit, days in users[username].items():
        total = sum(days)
        print(f"  {habit}: {total}/7 days completed")

def show_all_users_summary():
    """
    Print a summary of all users and their habits.
    """
    if not users:
        print("No users in the tracker yet.")
        return
    
    print("\n" + "="*50)
    print("HABIT TRACKER SUMMARY - ALL USERS")
    print("="*50)
    for username in users:
        show_user_summary(username)
    print("="*50 + "\n")

def list_users():
    """
    List all registered users.
    """
    if not users:
        print("No users registered yet.")
        return
    print("\nRegistered users:")
    for i, username in enumerate(users.keys(), 1):
        habit_count = len(users[username])
        print(f"  {i}. {username} ({habit_count} habits)")

def main():
    """
    Interactive menu for the habit tracker.
    """
    print("Welcome to the Multi-User Habit Tracker!")
    load_users()
    
    current_user = None
    
    while True:
        if current_user:
            print(f"\n--- Logged in as: {current_user} ---")
            print("1. Add a new habit")
            print("2. Mark habit as done")
            print("3. Show my summary")
            print("4. Switch user")
            print("5. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                habit_name = input("Habit name: ")
                add_habit(current_user, habit_name)
            
            elif choice == "2":
                if not users[current_user]:
                    print("You have no habits yet. Add one first!")
                    continue
                print("Your habits:")
                for i, habit in enumerate(users[current_user].keys(), 1):
                    print(f"  {i}. {habit}")
                habit_name = input("Habit name: ")
                print("\nDays of the week:")
                for i, day in enumerate(DAYS):
                    print(f"  {i}: {day}")
                day_index = int(input("Day number (0-6): "))
                mark_done(current_user, habit_name, day_index)
            
            elif choice == "3":
                show_user_summary(current_user)
            
            elif choice == "4":
                current_user = None
            
            elif choice == "5":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Try again.")
        
        else:
            print("\n1. Create new user")
            print("2. Select existing user")
            print("3. View all users")
            print("4. View all summaries")
            print("5. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                username = input("Enter username: ")
                add_user(username)
            
            elif choice == "2":
                username = input("Enter username: ")
                if username in users:
                    current_user = username
                    print(f"Logged in as {username}.")
                else:
                    print(f"User '{username}' not found.")
            
            elif choice == "3":
                list_users()
            
            elif choice == "4":
                show_all_users_summary()
            
            elif choice == "5":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
