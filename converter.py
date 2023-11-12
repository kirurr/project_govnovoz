from bing_image_downloader import downloader


def converter(lyrics):
    symbols_to_remove = ",&?.:/*%$#@=+-_\|!"
    for symbol in symbols_to_remove:
        lyrics = lyrics.replace(symbol, "")

    lyrics_array = lyrics.lower().split()

    for item in lyrics_array:
        downloader.download(
            item,
            limit=1,
            output_dir="images",
            adult_filter_off=True,
            force_replace=True,
            timeout=100,
            verbose=True,
        )
