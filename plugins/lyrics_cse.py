import os
from userge import userge, Message
try:
    from lyrics_extractor import Song_Lyrics
except:
    os.system("pip install lyrics-extractor")
from lyrics_extractor import Song_Lyrics
GCS_ENGINE_ID = os.environ.get("GCS_ENGINE_ID", None) 
GCS_API_KEY = os.environ.get("GCS_API_KEY", None)

@userge.on_cmd("glyrics", about={
    'header': "GCS Lyrics",
    'description': "Search lyrics of any song",
    'usage': "{tr}glyrics [Song Name]",
    'examples': "{tr}glyrics Higher Ground"})
async def glyrics(message: Message):
    if (GCS_ENGINE_ID and GCS_API_KEY) is None:
        await message.edit(
            "**Requirements Missing**\n\n"
            "Please Configure `GCS_ENGINE_ID` & `GCS_API_KEY`\n\n\n"
            "**More Info on How to Configure:**\n"
            "[NOTE: Read all Steps First, Coz No one's gonna help ya]\n"
            "1. Create your new Custom Search Engine here to get your Engine ID: https://cse.google.com/cse/create/new \n"
            "2. Add any of the following or all (adding all is recommended) websites as per your choice in your Custom Search Engine:\n\n"
            "   »`https://genius.com/` \n"
            "   »`http://www.lyricsted.com/` \n"
            "   »`http://www.lyricsbell.com/` \n"
            "   »`https://www.glamsham.com/` \n"
            "   »`http://www.lyricsoff.com/` \n"
            "   »`http://www.lyricsmint.com/` \n"
            "\n**NOTE:** Please **don't turn on** the '**Search the entire Web**' feature as it is currently not possible to scrape from any random"
            " sites appearing in the search results.\n"
            "3. Visit here to get your API key: https://developers.google.com/custom-search/v1/overview")
        return

    if not message.input_str:
        await message.edit("Give Song Name Sir")
        return

    song = message.input_str
    try:
        gcsl = Song_Lyrics(GCS_API_KEY, GCS_ENGINE_ID)
        song_title, song_lyrics = gcsl.get_lyrics(song)
        out = f"**{song_title}**\n\n**Lyrics:**\n\n__{song_lyrics}__"
        await message.edit(out)
    except Exception as e:
        await message.err(e)