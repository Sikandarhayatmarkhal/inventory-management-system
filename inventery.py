# User class to define users
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # 'admin' or 'employee'

    def __str__(self):
        return f"User(username={self.username}, role={self.role})"


# Product class to define products
class Product:
    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category  # New field for category

    def __str__(self):
        return f"Product(id={self.product_id}, name={self.name}, price={self.price}, stock={self.stock}, category={self.category})"


# Inventory system class for managing users and products
class InventorySystem:
    def __init__(self):
        self.users = []
        self.products = []
        self.current_user = None
        self.low_stock_threshold = 5  # Products below this stock will trigger a restocking message

    def register_user(self, username, password, role):
        if role not in ['admin', 'employee']:
            print("Invalid role. Must be 'admin' or 'employee'.")
            return
        user = User(username, password, role)
        self.users.append(user)
        print(f"User {username} registered successfully as {role}.")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"Logged in as {username} ({user.role}).")
                return True
        print("Login failed. Incorrect username or password.")
        return False

    def logout(self):
        print(f"User {self.current_user.username} logged out.")
        self.current_user = None

    def create_product(self, name, price, stock, category):
        if self.current_user.role != 'admin':
            print("Only admins can create products.")
            return

        product_id = len(self.products) + 1
        product = Product(product_id, name, price, stock, category)
        self.products.append(product)
        print(f"Product '{name}' created successfully with ID {product_id}.")
        self._check_stock_levels(product)

    def update_product(self, product_id, name=None, price=None, stock=None):
        if self.current_user.role != 'admin':
            print("Only admins can update products.")
            return

        for product in self.products:
            if product.product_id == product_id:
                if name:
                    product.name = name
                if price:
                    product.price = price
                if stock:
                    product.stock = stock
                print(f"Product {product_id} updated successfully.")
                self._check_stock_levels(product)
                return
        print(f"Product with ID {product_id} not found.")

    def view_products(self):
        if not self.products:
            print("No products available.")
            return

        for product in self.products:
            print(product)

    def search_product(self, search_term):
        found_products = [product for product in self.products if search_term.lower() in product.name.lower()]
        if found_products:
            for product in found_products:
                print(product)
        else:
            print("No products found matching that search term.")

    def filter_by_category(self, category):
        found_products = [product for product in self.products if category.lower() == product.category.lower()]
        if found_products:
            for product in found_products:
                print(product)
        else:
            print(f"No products found in category '{category}'.")

    def filter_low_stock(self):
        low_stock_products = [product for product in self.products if product.stock <= self.low_stock_threshold]
        if low_stock_products:
            print("Products with low stock:")
            for product in low_stock_products:
                print(product)
        else:
            print("No products with low stock.")

    def adjust_stock(self, product_id, amount):
        for product in self.products:
            if product.product_id == product_id:
                product.stock += amount
                print(f"Stock adjusted for product {product_id}. New stock level: {product.stock}.")
                self._check_stock_levels(product)
                return
        print(f"Product with ID {product_id} not found.")

    def delete_product(self, product_id):
        if self.current_user.role != 'admin':
            print("Only admins can delete products.")
            return

        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                print(f"Product {product_id} deleted successfully.")
                return
        print(f"Product with ID {product_id} not found.")

    def _check_stock_levels(self, product):
        if product.stock <= self.low_stock_threshold:
            print(f"WARNING: Stock for product '{product.name}' (ID: {product.product_id}) is low! Consider restocking.")


# Main logic to interact with the user via console
def main():
    system = InventorySystem()

    # Create default admin
    system.register_user('admin', 'password', 'admin')

    while True:
        print("\nInventory Management System")
        print("1. Register")
        print("2. Login")
        print("3. View Products")
        print("4. Search Product by Name")
        print("5. Filter Products by Category")
        print("6. Filter Low Stock Products")
        if system.current_user and system.current_user.role == 'admin':
            print("7. Create Product")
            print("8. Update Product")
            print("9. Adjust Stock")
            print("10. Delete Product")
        print("11. Logout")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (admin/employee): ")
            system.register_user(username, password, role)

        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            system.login(username, password)

        elif choice == '3':
            system.view_products()

        elif choice == '4':
            search_term = input("Enter product name to search: ")
            system.search_product(search_term)

        elif choice == '5':
            category = input("Enter category to filter: ")
            system.filter_by_category(category)

        elif choice == '6':
            system.filter_low_stock()

        elif choice == '7' and system.current_user and system.current_user.role == 'admin':
            name = input("Product Name: ")
            price = float(input("Product Price: "))
            stock = int(input("Product Stock: "))
            category = input("Product Category: ")
            system.create_product(name, price, stock, category)

        elif choice == '8' and system.current_user and system.current_user.role == 'admin':
            product_id = int(input("Product ID: "))
            name = input("New Name (press Enter to skip): ")
            price = input("New Price (press Enter to skip): ")
            stock = input("New Stock (press Enter to skip): ")

            system.update_product(product_id, name=name if name else None,
                                  price=float(price) if price else None,
                                  stock=int(stock) if stock else None)

        elif choice == '9' and system.current_user and system.current_user.role == 'admin':
            product_id = int(input("Product ID to adjust stock: "))
            amount = int(input("Enter stock adjustment (positive for restocking, negative for sales): "))
            system.adjust_stock(product_id, amount)

        elif choice == '10' and system.current_user and system.current_user.role == 'admin':
            product_id = int(input("Product ID to delete: "))
            system.delete_product(product_id)

        elif choice == '11' and system.current_user:
            system.logout()

        elif choice == '12':
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice or insufficient permissions.")


# Run the program
if __name__ == "__main__":
    main()
