import asyncio
import logging

from jev_try.run import JEV

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    j = JEV('cpp_llama_runs.jsonl','cpp')


    async def main():
        await j.call('abc394c')


    asyncio.get_event_loop().run_until_complete(main())
