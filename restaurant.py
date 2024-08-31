menu = {
    "pizzas": {
        "pepperoni": 12.99,
        "margarita": 10.99,
        "chicken": 13.99,
        "4 cheese": 14.99,
        "cesar": 15.99
    },
    "drinks": {
        "coca cola": 1.99,
        "sprite": 1.99,
        "fanta": 1.99
    }
}


def display_menu(menu_type):
    print(f"\nAvailable {menu_type}:")
    for index, (item, price) in enumerate(menu[menu_type].items(), start=1):
        print(f"{index}. {item.title()} - ${price:.2f}")


def get_choice(menu_type):
    choices = menu[menu_type].keys()
    selected_items = {}

    while True:
        try:
            display_menu(menu_type)
            choice = (input(
                f"Please enter the number of the {menu_type[:-1]} you'd like to order (or type 'done' to finish): ")
                      .lower())

            if choice == 'done':
                break

            choice_index = int(choice) - 1
            if choice_index < 0 or choice_index >= len(choices):
                raise ValueError("Invalid choice. Please select a valid option.")

            selected_item = list(choices)[choice_index]
            quantity = int(input(f"How many {selected_item.title()} would you like to order? "))

            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")

            selected_items[selected_item] = selected_items.get(selected_item, 0) + quantity

        except ValueError as e:
            print(f"Error: {e}. Please try again.")

    return selected_items


def calculate_total_cost(orders, menu_type):
    total_cost = 0
    for item, quantity in orders.items():
        total_cost += menu[menu_type][item] * quantity
    return total_cost


def handle_payment(total):
    print(f"\nYour total is: ${total:.2f}")
    bills = [1, 5, 10, 20, 50, 100]
    payment = 0

    while payment < total:
        print("Available bills for payment: 1, 5, 10, 20, 50, 100")
        try:
            bill = int(input("Enter the bill denomination you are going to use for payment: "))
            if bill not in bills:
                raise ValueError("Invalid bill denomination. Please select from the available options.")
            amount = int(input(f"How many ${bill} bills do you want to use? "))
            if amount <= 0:
                raise ValueError("Amount must be a positive integer.")
            payment += bill * amount
            print(f"Total payment so far: ${payment:.2f}")
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

    if payment > total:
        print(f"Your change is: ${payment - total:.2f}")
    print("Payment successful! Thank you for your order.")


def main():
    print("Welcome to the Pizza Ordering App!")

    print("\nLet's start with pizzas.")
    pizza_orders = get_choice("pizzas")
    total_pizza_cost = calculate_total_cost(pizza_orders, "pizzas")

    print("\nNow, let's select some drinks.")
    drink_orders = get_choice("drinks")
    total_drink_cost = calculate_total_cost(drink_orders, "drinks")

    total_cost = total_pizza_cost + total_drink_cost
    print(f"\nYour order summary:")
    for pizza, quantity in pizza_orders.items():
        print(f"{quantity}x {pizza.title()} Pizza - ${menu['pizzas'][pizza] * quantity:.2f}")
    for drink, quantity in drink_orders.items():
        print(f"{quantity}x {drink.title()} - ${menu['drinks'][drink] * quantity:.2f}")
    print(f"Total cost: ${total_cost:.2f}")

    handle_payment(total_cost)


if __name__ == "__main__":
    main()
