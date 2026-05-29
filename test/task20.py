import aiohttp
import asyncio

async def fetch_page(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print("Page loaded successfully")
                else:
                    print(f"Request failed with status: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Network error: {e}")
    except asyncio.TimeoutError:
        print("Request timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def main():
    url = "https://habr.com/ru"
    await fetch_page(url)

if __name__ == "__main__":
    asyncio.run(main())
