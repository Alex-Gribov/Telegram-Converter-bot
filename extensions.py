import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    currency_mapping = {
        "доллар": "USD",
        "евро": "EUR",
        "рубль": "RUB",
        # Добавьте другие валюты по мере необходимости
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        try:
            if amount <= 0:
                raise APIException("Количество валюты должно быть положительным числом.")

            base_code = CurrencyConverter.currency_mapping.get(base.lower())
            quote_code = CurrencyConverter.currency_mapping.get(quote.lower())

            if not base_code or not quote_code:
                raise APIException("Неизвестная валюта.")

            api_key = "283ce6ed95d5f0190248f298"  # Замените на ваш API-ключ!  Храните его в файле конфигурации, а не в коде!
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_code}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            if 'result' not in data or data['result'] != 'success':
                raise APIException(f"Ошибка API: {data.get('error-type', 'Unknown error')}")

            if quote_code not in data['conversion_rates']:
                raise APIException(f"Валюта {quote} не найдена.")

            rate = data['conversion_rates'][quote_code]

            if rate == 0:
                raise APIException("Ошибка получения курса валюты.")

            total = amount * rate
            return total

        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка API: {e}")
        except json.JSONDecodeError as e:
            raise APIException(f"Ошибка парсинга JSON: {e}")
        except KeyError as e:
            raise APIException(f"Ошибка: {e}")
        except APIException as e:
            raise e

