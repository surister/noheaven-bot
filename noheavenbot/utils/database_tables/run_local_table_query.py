"""Testing file for database_tables/*.py"""

import asyncio
from noheavenbot.utils.database_tables.table_users import Users


async def main():
    c = await Users.get_users_identifiers_list()

#
# asyncio.run(main())