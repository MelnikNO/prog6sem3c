import asyncio
import aiohttp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CROSSREF_API_URL = "https://api.crossref.org/works"

REQUEST_TIMEOUT = 10

ROWS_LIMIT = 15


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_sync():
    author = request.form.get('author', '').strip()
    title = request.form.get('title', '').strip()

    if not author and not title:
        return jsonify({'error': 'Заполните хотя бы одно поле: автор или название'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(async_search_publications(author, title))
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': f'Ошибка при выполнении поиска: {str(e)}'}), 500
    finally:
        loop.close()


async def async_search_publications(author: str, title: str):
    params = {
        'rows': ROWS_LIMIT,
    }

    if author:
        params['query.author'] = author
    if title:
        params['query.title'] = title

    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(CROSSREF_API_URL, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API вернул ошибку {response.status}: {error_text[:200]}")

                data = await response.json()

                items = data.get('message', {}).get('items', [])
                if not items:
                    return []

                tasks = [process_publication(item) for item in items]
                results = await asyncio.gather(*tasks)

                return results

        except asyncio.TimeoutError:
            raise Exception(f"Превышено время ожидания ответа от API ({REQUEST_TIMEOUT} сек)")
        except aiohttp.ClientError as e:
            raise Exception(f"Ошибка соединения с Crossref API: {str(e)}")
        except Exception as e:
            raise Exception(f"Неизвестная ошибка при запросе: {str(e)}")


async def process_publication(item: dict):
    title_list = item.get('title', [])
    title_text = title_list[0] if title_list else 'Без названия'

    authors = item.get('author', [])
    first_author_name = 'Не указан'
    affiliation_text = 'Не указано'

    if authors:
        first_author = authors[0]
        family = first_author.get('family', '')
        given = first_author.get('given', '')
        if family or given:
            first_author_name = f"{family} {given}".strip()
        else:
            first_author_name = 'Без имени'

        affiliations = first_author.get('affiliation', [])
        if affiliations and isinstance(affiliations, list) and len(affiliations) > 0:
            affiliation_text = affiliations[0].get('name', 'Не указано')

    container_title = item.get('container-title', [])
    journal_name = container_title[0] if container_title else 'Не указан'

    issued = item.get('issued', {})
    date_parts = issued.get('date-parts', [])
    if date_parts and len(date_parts) > 0 and len(date_parts[0]) > 0:
        year = date_parts[0][0]
    else:
        year = 'Не указан'

    if year == 'Не указан':
        published_online = item.get('published-online', {})
        online_date_parts = published_online.get('date-parts', [])
        if online_date_parts and len(online_date_parts) > 0 and len(online_date_parts[0]) > 0:
            year = online_date_parts[0][0]

    return {
        'title': title_text,
        'first_author': first_author_name,
        'journal': journal_name,
        'year': str(year),
        'affiliation': affiliation_text,
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)