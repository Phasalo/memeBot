import aiohttp

__URL = 'https://ws3.morpher.ru/russian/declension'


async def decline_word(word: str, decline: str) -> str:

    headers = {'User-Agent': 'TG'}
    params = {'s': word, 'format': 'json'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url=__URL, params=params, headers=headers) as response:
            data = await response.json()

            if response.status == 200:
                return data.get(decline)
            elif response.status == 402:
                return word
            else:
                raise Exception(f'Ошибка при запросе склонения: {response.status}')
