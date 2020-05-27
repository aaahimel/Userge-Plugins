# Tesla's Project YTS
import asyncio, requests, json, os
from userge import userge, Message

@userge.on_cmd("yts", about={
    'header': "YTS Movie Search.",
    'description': "To Download .torrent file from YTS. It'll download first 10 matched torrents and default quality is 720p.",
    'usage': "{tr}yts [Movie name] [-quality]",
    'examples': "{tr}yts life of pi -1080p"})
async def yts(message: Message):
    max_limit = 10
    input_ = message.input_or_reply_str
    
    if input_.find('-') == -1:
        qual = None
    else:
        qual = input_[input_.find('-')+1:]
        input_ = input_[:input_.find('-')-1]
    
    if len(input_) == 0:
        await message.edit("No Input Found!, check .help yts", del_in=5)
        return
    else:
        URL = "https://yts.mx/api/v2/list_movies.json?query_term={0}"
        await message.edit("Fetching....")
        resp = requests.get(URL.format(input_))
        datas = resp.json()

    if datas['status'] != "ok":
        await message.edit("WRONG STATUS")
        return

    elif datas['data']['movie_count'] == 0:
        await message.edit(f"{input_} Not Found!")
        return
    
    else:
        await message.edit(f"{datas['data']['movie_count']} Matches Found!")
        _limit = 1
        for data in datas['data']['movies']:
            if _limit <= max_limit:
                _title = data['title_long']
                _rating = data['rating']
                _language = data['language']
                _torrents = data['torrents']
                def_quality = "720p"
                _qualities = []
                for i in _torrents:
                    _qualities.append(i['quality'])
                if qual in _qualities:
                    def_quality = qual
                capts = f'''
Title: {_title}
Rating: {_rating}
Language: {_language}
Size: {_torrents[_qualities.index(def_quality)]['size']}
Type: {_torrents[_qualities.index(def_quality)]['type']}
Seeds: {_torrents[_qualities.index(def_quality)]['seeds']}
Date Uploaded: {_torrents[_qualities.index(def_quality)]['date_uploaded']}
Available in: {_qualities}'''
                if def_quality in _qualities:
                    files = f"{_title}{_torrents[_qualities.index(def_quality)]['quality']}.torrent"
                    files = files.replace('/', '\\')
                    with open(files, 'wb') as f:
                        f.write(requests.get(_torrents[_qualities.index(def_quality)]['url']).content)
                    await userge.send_document(chat_id=message.chat.id,
                                        document=files,
                                        caption=capts,
                                        disable_notification=True)
                    os.remove(files)
                    _limit += 1
                else:
                    message.edit("NOT FOUND")
                    return
    return