"""Testing file for database_tables/*.py"""

import asyncio
from noheavenbot.utils.database_tables.table_trusted_bots import TrustedBot


async def main():
    c = await TrustedBot.get_ids()
    print(c)

# asyncio.run(main())