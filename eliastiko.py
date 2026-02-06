# Habit Tracker Starter Code
 
habits = {}  
# Example structure:
# {
#   "Exercise": [1, 0, 1, 1, 0, 1, 0],
#   "Read":     [1, 1, 1, 0, 0, 1, 1]
# }
 
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
 
def add_habit(name):
    """
    Add a new habit with 7 days initialized to 0.
    """
    if name in habits:
        print(f"Habit '{name}' already exists.")
        return
    habits[name] = [0] * 7

def mark_done(name, day_index):
    """
    Mark a habit as done (1) for a given day.
    """
    if name not in habits:
        print(f"Habit '{name}' does not exist.")
        return # always check if the habit exists
    if day_index < 0 or day_index > 6:
        print("Invalid day index. Must be between 0 and 6.")
        return #making sure the index is within bounds
    habits[name][day_index] = 1
   
    pass
 
 
def weekly_total(name):
    """
    Return how many days the habit was completed.
    """
    return sum(habits.get(name, []))

 
 
def show_summary():
    """
    Print a summary of all habits.
    """
    for habit, days in habits.items():
        total = sum(days)
 
        print(f"Habit: {habit}, Completed Days: {total}/7")
 
 
def main():
    while True:
        print("\n1. Add habit")
        print("2. Mark habit done")
        print("3. Show summary")
        print("4. Exit")
 
        choice = input("Choose an option: ")
 
        if choice == "1":
            name = input("Habit name: ")
            add_habit(name)
 
        elif choice == "2":
            name = input("Habit name: ")
            for i, d in enumerate(DAYS):
                print(i, d)
            day = int(input("Day number: "))
            mark_done(name, day)
 
        elif choice == "3":
            show_summary()
 
        elif choice == "4":
            print("Goodbye!")
            break
 
        else:
            print("Invalid choice")
 
 
main()