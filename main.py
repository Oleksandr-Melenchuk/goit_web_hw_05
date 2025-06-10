from datetime import datetime, timedelta
import aiohttp
import asyncio


def user_input() -> int:
    while True:
        try:
            input_days = int(input("Введіть за скільки днів ви хочете дізнатись курс (1-10): "))
            if 1 <= input_days <= 10:
                return input_days
            else:
                print('Введіть число від 1 до 10')
        except ValueError:
            print("Введіть число")


def date_list(days: int) -> list:
    now = datetime.now()
    return [(now - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]


def extract_rate(currency_code, rates):
    r = next((item for item in rates if item.get("currency") == currency_code), None)
    if r:
        return {
            "sale": r.get("saleRate"),
            "purchase": r.get("purchaseRate")
        }
    return None


async def parse_data(session, url, date):
    async with session.get(url) as response:
        data = await response.json()
        rates = data.get('exchangeRate', [])
        
        if not rates:
                print(f"[{date}] Дані відсутні у відповіді")
                return {date: None}
        
        
        return {
            date: {
                "EUR": extract_rate("EUR", rates),
                "USD": extract_rate("USD", rates)
            }
        }


async def main():
    days = user_input()
    dates = date_list(days)
    base_url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    async with aiohttp.ClientSession() as session:
        tasks = [parse_data(session, f'{base_url}{day}', day) for day in dates]
        result = await asyncio.gather(*tasks)

        result_list = [result for result in results]
        print(result_list)


if __name__ == '__main__':
    asyncio.run(main())
