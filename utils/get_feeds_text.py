from db.repository import feeds_repository


async def get_feeds_text(feeds: dict):
    text = ""
    try:
        for key in feeds.keys():
            feed = await feeds_repository.select_feed_by_id(int(key))
            text += f"{feed.category_of_feed + ': ' + feed.kind_of_animal} - {feeds[key]} кг\n"
    finally:
        return text
