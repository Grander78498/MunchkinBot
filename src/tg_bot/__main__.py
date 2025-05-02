# pylint: skip-file
import os
import sys
import asyncio
from pathlib import Path

working_dir = Path().absolute().parent

for name in os.listdir(working_dir):
    if os.path.isdir(working_dir.joinpath(name)):
        sys.path.insert(0, working_dir.joinpath(name))

from tg_bot.main import main

if __name__ == "__main__":
    asyncio.run(main())
