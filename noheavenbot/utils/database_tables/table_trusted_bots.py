from noheavenbot.utils import Database
from datetime import datetime


class TrustedBot:

    @classmethod
    async def insert_bot(cls, added_by_id: str, added_by_name: str, bot_id: str, bot_name: str, is_admin: bool = False):
        conn = await Database.connect()
        await conn.execute('''
        INSERT INTO nh.trusted_bots 
            (added_by_id, added_by_name, bot_id, bot_name, date_arrival, is_admin) 
            VALUES ($1, $2, $3, $4, $5, $6)
        ''', added_by_id, added_by_name, bot_id, bot_name, datetime.today(), is_admin)

    @classmethod
    async def get_ids(cls):
        conn = await Database.connect()
        query = await conn.fetch('''
        SELECT bot_id FROM nh.trusted_bots
        
        ''')
        return [int(botid.get('bot_id')) for botid in query]