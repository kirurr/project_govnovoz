from bing_image_downloader import downloader


def converter(lyrics):

    lyrics_array = lyrics.lower().split()

    for item in lyrics_array:
        downloader.download(
            item,
            limit=1,
            output_dir="images",
            adult_filter_off=True,
            force_replace=False,
            timeout=100,
            verbose=False,
        )
