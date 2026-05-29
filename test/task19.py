import aiohttp
import asyncio

async def fetch_data(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as response:
            status = response.status
            if status == 200:
                print("Request successful")
            else:
                print(f"Request failed with status: {status}")
    except aiohttp.ClientError as e:
        print(f"Network error: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        await fetch_data(session, "https://httpbin.org/get")
        await fetch_data(session, "https://httpbin.org/status/404")

if __name__ == "__main__":
    asyncio.run(main())
