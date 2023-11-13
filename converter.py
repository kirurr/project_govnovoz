import downloader


def converter(lyrics):
    symbols_to_remove = ",&?.:/*%$#@=+-_\|!"
    for symbol in symbols_to_remove:
        lyrics = lyrics.replace(symbol, "")

    lyrics_array = lyrics.lower().split()

    count = 1
    i = 0
    lenght = len(lyrics_array)

    while i < lenght:
        lyrics_array[i] = f"{str(count)}_{lyrics_array[i]}"

        downloader.download(
            lyrics_array[i],
            limit=1,
            output_dir="images",
            adult_filter_off=True,
            force_replace=False,
            timeout=100,
            verbose=True,
        )

        i += 1
        count += 1
