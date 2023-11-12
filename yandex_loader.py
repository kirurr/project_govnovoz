import requests


class Loader:
    def __init__(self, path_to_folder, path_to_archive):
        self.path_to_folder = path_to_folder
        self.path_to_archive = path_to_archive

        self.URL = "https://cloud-api.yandex.net/v1/disk/resources"
        self.TOKEN = "AQAAAAAz55vbAAc-fohhPDQSvU5kroy21-HguNA"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth y0_AgAAAABfCDvzAArN-gAAAADxyjijNYoyWaWMRxqra0axbdjaVbyFF2o",
        }

    def create_folder(self):
        requests.put(f"{self.URL}?path={self.path_to_folder}", headers=self.headers)

    # проверяем, есть ли папка на диске, если нет - создаем
    def check(self):
        res = requests.get(
            f"{self.URL}?path={self.path_to_folder}", headers=self.headers
        ).json()
        if "error" in res:
            self.create_folder()

    def upload_file(self, loadfile, savefile, replace=False):
        res = requests.get(
            f"{self.URL}/upload?path={savefile}&overwrite={replace}",
            headers=self.headers,
        ).json()
        with open(loadfile, "rb") as f:
            try:
                requests.put(res["href"], files={"file": f})
            except KeyError:
                print(res)

    def get_download_link(self):
        res = requests.get(
            f"{self.URL}/download?path={self.path_to_folder}/{self.path_to_archive}",
            headers=self.headers,
        ).json()
        link = res["href"]
        return link

    def load_to_yandex(self):
        self.check()
        self.upload_file(
            self.path_to_archive, self.path_to_folder + "/" + self.path_to_archive
        )
