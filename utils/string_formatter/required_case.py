import aiohttp

url = 'https://ws3.morpher.ru/russian/declension'


async def word2case(town: str, case: str) -> str:

    headers = {'User-Agent': 'TG'}

    params = {
        's': town,
        'format': 'json',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, headers=headers) as response:
            data = await response.json()

            if response.status == 200:
                return data.get(case)
            elif response.status == 402:
                return town
            else:
                raise Exception(f'Ошибка при запросе склонения: {response.status}')
