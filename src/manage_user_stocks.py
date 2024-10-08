import json
import pandas as pd

# File paths
users_file = 'users.json'
listeners_file = '../data/listeners_data.csv'

# Load JSON data
def load_users():
    try:
        with open(users_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save JSON data
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# Add user
def add_user(username):
    users = load_users()
    if username not in users:
        users[username] = {
            'Username': username,
            'Stocks': [],
            'FloatingMoney': 100,
            'PortfolioValue': 100
        }
        save_users(users)
        print(f"User {username} added successfully.")
    else:
        print(f"User {username} already exists.")

# Calculate Portfolio
def calculate_portfolio(username):
    users = load_users()
    if username in users:
        df = pd.read_csv(listeners_file)
        last_row = df.iloc[-1]
        portfolio_value = 0
        
        for stock in users[username]['Stocks']:
            artist_name = stock['ArtistName']
            current_gross = last_row[artist_name]
            stock['CurrentValue'] = (current_gross / stock['GrossAtPurchase']) * stock['AmountPurchased']
            portfolio_value += stock['CurrentValue']
        
        users[username]['PortfolioValue'] = portfolio_value
        save_users(users)
        print(f"Portfolio for {username} updated successfully.")
    else:
        print(f"User {username} not found.")

# Buy stock
def buy_stock(username, artist_name, amount_purchased):
    users = load_users()
    if username in users:
        df = pd.read_csv(listeners_file)
        last_row = df.iloc[-1]
        
        if users[username]['FloatingMoney'] >= amount_purchased:
            current_gross = last_row[artist_name]
            stock_exists = False
            
            for stock in users[username]['Stocks']:
                if stock['ArtistName'] == artist_name:
                    stock['AmountPurchased'] += amount_purchased
                    stock['GrossAtPurchase'] = current_gross
                    stock_exists = True
                    break
            
            if not stock_exists:
                new_stock = {
                    'ArtistName': artist_name,
                    'CurrentValue': amount_purchased,  # Will be updated in calculate_portfolio
                    'AmountPurchased': amount_purchased,
                    'GrossAtPurchase': int(current_gross)
                }
                users[username]['Stocks'].append(new_stock)
            
            users[username]['FloatingMoney'] -= amount_purchased
            calculate_portfolio(username)
            save_users(users)
            print(f"Stock {artist_name} purchased successfully for user {username}.")
        else:
            print("Insufficient funds.")
    else:
        print(f"User {username} not found.")


def sell_stock(username, artist_name, amount_to_sell):
    users = load_users()
    if username in users:
        user = users[username]
        stock_found = False

        for stock in user['Stocks']:
            if stock['ArtistName'] == artist_name:
                stock_found = True
                if stock['CurrentValue'] >= amount_to_sell:
                    # Deduct the sold amount from Stock current value
                    stock['CurrentValue'] -= amount_to_sell

                    # Add the sold amount to FloatingMoney
                    user['FloatingMoney'] += amount_to_sell

                    # Update AmountPurchased to the new CurrentValue
                    stock['AmountPurchased'] = stock['CurrentValue']

                    # Reset GrossAtPurchase with current listeners from listeners_data.csv
                    df = pd.read_csv(listeners_file)
                    last_row = df.iloc[-1]
                    stock['GrossAtPurchase'] = int(last_row[artist_name])

                    # Update portfolio value
                    calculate_portfolio(username)
                    save_users(users)
                    print(f"Stock {artist_name} sold successfully for user {username}.")
                else:
                    print(f"Insufficient stock value to sell {amount_to_sell}. Current value is {stock['CurrentValue']}.")
                break

        if not stock_found:
            print(f"Stock {artist_name} not found for user {username}.")
    else:
        print(f"User {username} not found.")