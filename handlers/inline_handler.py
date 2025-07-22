from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from config_data.config import Config, load_config

config: Config = load_config()

router = Router()


@router.inline_query()
async def inline_get_photo(query: types.InlineQuery):
    text = query.query
    # какая-то бизнес-логика, генерирующая result

    #   <-| ----------------- -<phasalo>- ------------------ |->
    #                                                          |
    #   какая-то бизнес-логика, генерирующая result            | <=| PHASALO<|||
    #                                                          |
    #   <-| ----------------- -<phasalo>- ------------------ |->
    await query.answer(result, cache_time=1, is_personal=True)
