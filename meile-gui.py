import src.main.main as Meile
import asyncio
from threading import Thread

if __name__ == "__main__":
    meilethread = Thread(target=Meile.app.run())
    meilethread.start()