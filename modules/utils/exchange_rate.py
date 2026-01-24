import requests


def get_exchange_rate(from_currency: str, to_currency: str):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            rate = data["rates"][to_currency]
            return rate
        else:
            raise ValueError(
                f"Failed to get exchange rate for {from_currency} to {to_currency}"
            )
    except Exception as e:
        raise ValueError(
            f"Failed to get exchange rate for {from_currency} to {to_currency}: {e}"
        )
