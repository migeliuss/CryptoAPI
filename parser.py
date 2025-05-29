import requests
import csv
from typing import List, Dict, Optional
import locale
from datetime import datetime
import os

class Cryptocurrency:
    def __init__(self, name: str, symbol: str, price: float, market_cap: float, circulating_supply: float):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.market_cap = market_cap
        self.circulating_supply = circulating_supply
    
    def __str__(self):
        return (f"{self.name} ({self.symbol}): "
                f"Price: ${self.price:,.2f}, "
                f"Market Cap: ${self.market_cap:,.2f}, "
                f"Circulating Supply: {self.circulating_supply:,.2f}")

class CryptoDataProcessor:
    def __init__(self):
        self.cryptocurrencies: List[Cryptocurrency] = []
        self.api_key = None
    
    def set_api_key(self, api_key: str):
        self.api_key = api_key
    
    def fetch_from_api(self, limit: int = 100) -> bool:
        if not self.api_key:
            print("Ошибка: API ключ не установлен")
            return False
        
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            'start': '1',
            'limit': str(limit),
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        try:
            response = requests.get(url, headers=headers, params=parameters)
            data = response.json()
            
            if response.status_code == 200:
                for crypto_data in data['data']:
                    crypto = Cryptocurrency(
                        name=crypto_data['name'],
                        symbol=crypto_data['symbol'],
                        price=crypto_data['quote']['USD']['price'],
                        market_cap=crypto_data['quote']['USD']['market_cap'],
                        circulating_supply=crypto_data['circulating_supply']
                    )
                    self.cryptocurrencies.append(crypto)

                print(f"Успешно загружено {len(self.cryptocurrencies)} криптовалют с CoinMarketCap API")
                return True
            else:
                print(f"Ошибка API: {data['status']['error_message']}")
                return False
                
        except Exception as e:
            print(f"Ошибка при запросе к API: {e}")
            return False
    
    def add_crypto(self, crypto: Cryptocurrency) -> None:
        self.cryptocurrencies.append(crypto)
    
    def get_all_cryptos(self) -> List[Cryptocurrency]:
        return self.cryptocurrencies
    
    def get_all_cryptos_pages(self, page: int = 1, per_page: int = 15) -> List[Cryptocurrency]:
        start = (page - 1) * per_page
        end = start + per_page
        return self.cryptocurrencies[start:end]
    
    def get_crypto_by_name(self, name: str) -> Optional[Cryptocurrency]:
        for crypto in self.cryptocurrencies:
            if crypto.name.lower() == name.lower():
                return crypto
        return None
    
    def get_top_by_market_cap(self, n: int = 10) -> List[Cryptocurrency]:
        sorted_cryptos = sorted(self.cryptocurrencies, key=lambda x: x.market_cap, reverse=True)
        return sorted_cryptos[:n]
    
    def get_cryptos_in_price_range(self, min_price: float, max_price: float) -> List[Cryptocurrency]:
        return [crypto for crypto in self.cryptocurrencies if min_price <= crypto.price <= max_price]
    
    def calculate_total_market_cap(self) -> float:
        return sum(crypto.market_cap for crypto in self.cryptocurrencies)
    
    def save_to_csv(self, file_path: str) -> None:
        try:
            timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
            filename = f"{file_path}_{timestamp}.csv" if not file_path.endswith('.csv') else file_path
            
            with open(filename, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['data.name', 'data.symbol', 'ata.quote.USD.price', 'ata.quote.USD.market_cap', 'data.circulating_supply'])
                for crypto in self.cryptocurrencies:
                    writer.writerow([
                        crypto.name,
                        crypto.symbol,
                        crypto.price,
                        crypto.market_cap,
                        crypto.circulating_supply
                    ])
            print(f"Данные успешно сохранены в {filename}")
        except Exception as e:
            print(f"Произошла ошибка при сохранении файла: {e}")

def display_menu():
    print("\nМеню:")
    print("1. Установить API ключ CoinMarketCap")
    print("2. Загрузить данные с CoinMarketCap API")
    print("3. Показать все криптовалюты")
    print("4. Найти криптовалюту по имени")
    print("5. Показать топ-N по рыночной капитализации")
    print("6. Показать криптовалюты в диапазоне цен")
    print("7. Показать общую рыночную капитализацию")
    print("8. Добавить новую криптовалюту (вручную)")
    print("9. Сохранить данные в CSV")
    print("10. Выход")

def show_all_cryptos_pages(processor):
    page = 1
    per_page = 15
    total_pages = (len(processor.cryptocurrencies) + per_page - 1) // per_page
    
    while True:
        cryptos = processor.get_all_cryptos_pages(page, per_page)
        print(f"\n=== Страница {page}/{total_pages} ===")
        for i, crypto in enumerate(cryptos, 1):
            print(f"{i}. {crypto.name} ({crypto.symbol}): ${crypto.price:,.2f}")
        
        print("\nДействия:")
        print("e - следующая страница")
        print("q - предыдущая страница")
        print("x - вернуться в меню")
        
        action = input("Выберите действие: ").lower()
        match action:
            case 'e':
                if page < total_pages:
                    page += 1
            case 'q':
                if page > 1:
                    page -= 1
            case 'x':
                if action == 'x':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
            case _:
                print("Некорректный ввод / конец списка")
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    processor = CryptoDataProcessor()
    
    while True:
        display_menu()
        while True:
            try:
                choice = int(input("Выберите действие (1-10): "))
                break
            except ValueError:
                print("Неверный выбор. Попробуйте снова.")

        match choice:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                api_key = input("Введите ваш API ключ CoinMarketCap: ").strip()
                processor.set_api_key(api_key)
                print("API ключ установлен")
        
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                if not processor.api_key:
                    print("Сначала установите API ключ (пункт меню 1)")
                    continue
                try:
                    limit = int(input("Кол-во загружаемых криптовалют(не вводить большое число, кредиты снимаются) ") or "100")
                    if processor.fetch_from_api(limit):
                        print("Данные успешно загружены")
                except ValueError:
                    print("Ошибка: введите целое число")
        
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                if not processor.cryptocurrencies:
                    print("Сначала загрузите данные (пункт 2)!")
                else:
                    show_all_cryptos_pages(processor)
        
            case 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                name = input("Введите название криптовалюты: ")
                crypto = processor.get_crypto_by_name(name)
                if crypto:
                    print(crypto)
                else:
                    print("Криптовалюта не найдена.")
        
            case 5:
                os.system('cls' if os.name == 'nt' else 'clear')
                try:
                    n = int(input("Введите количество криптовалют для отображения: "))
                    top_cryptos = processor.get_top_by_market_cap(n)
                    for i, crypto in enumerate(top_cryptos, 1):
                        print(f"{i}. {crypto.name} ({crypto.symbol}) - Капитализация: ${crypto.market_cap:,.2f}")
                except ValueError:
                    print("Ошибка: введите целое число.")
        
            case 6:
                os.system('cls' if os.name == 'nt' else 'clear')
                try:
                    min_p = float(input("Минимальная цена: "))
                    max_p = float(input("Максимальная цена: "))
                    cryptos = processor.get_cryptos_in_price_range(min_p, max_p)
                    for crypto in cryptos:
                        print(crypto)
                except ValueError:
                    print("Ошибка: введите числовые значения для цен.")
        
            case 7:
                os.system('cls' if os.name == 'nt' else 'clear')
                total = processor.calculate_total_market_cap()
                print(f"Общая рыночная капитализация: ${total:,.2f}")
        
            case 8:
                os.system('cls' if os.name == 'nt' else 'clear')
                try:
                    name = input("Название: ")
                    symbol = input("Символ: ")
                    price = float(input("Цена (USD): "))
                    market_cap = float(input("Рыночная капитализация: "))
                    supply = float(input("Объем токенов в обороте: "))
                
                    new_crypto = Cryptocurrency(name, symbol, price, market_cap, supply)
                    processor.add_crypto(new_crypto)
                    print("Криптовалюта добавлена.")
                except ValueError:
                    print("Ошибка: введите корректные числовые значения.")
        
            case 9:
                os.system('cls' if os.name == 'nt' else 'clear')
                file_path = input("Введите имя файла для сохранения (без расширения .csv): ")
                processor.save_to_csv('snapshots/'+file_path)
        
            case 10:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Выход из программы.")
                break
        
            case _:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    main()