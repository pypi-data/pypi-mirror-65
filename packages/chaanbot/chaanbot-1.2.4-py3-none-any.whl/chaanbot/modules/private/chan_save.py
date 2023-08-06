""" The chan save module preserves 4chan media.

Available commands:
None, will trigger on 4chan links by users.

Usage example:
[user]: https://4chan.org/i/1231231.jpg

Would results in:
"Bot: Image saved at [website-url]"
"""
import logging
import re
import uuid
from typing import List

logger = logging.getLogger("chan_save")


class ChanSave:
    chan_regex_urls = ['4chan\\.org', 'i\\.4cdn\\.org']
    file_extensions_to_save = ["jpg", "png", "bmp", "gif", "jpeg", "webm", "pdf"]
    always_run = True

    def __init__(self, config, matrix, database, requests):
        self.matrix = matrix
        self.requests = requests
        save_location = config.get("chan_save", "save_location", fallback=None)
        url_for_saved_files = config.get("chan_save", "url_for_saved_files", fallback=None)

        if save_location:
            self.save_location = save_location if save_location.endswith("/") else save_location + "/"
        else:
            self.disabled = True
            logger.info("No location provided for chan_save, module disabled")
            return
        if url_for_saved_files:
            self.url_for_saved_files = url_for_saved_files if url_for_saved_files.endswith(
                "/") else url_for_saved_files + "/"

    def run(self, room, event, message) -> bool:
        links = self._get_links(message)
        for link in links:
            if link and self._should_run(link):
                logger.debug("Should run chan_save, checking if which (if any) file to save")
                file_extension = self._get_file_extension(link)
                if file_extension:
                    filepath, filename = self._save_media(room, event["sender"], link, file_extension)
                    if hasattr(self, "url_for_saved_files"):
                        room.send_text("File saved to {}{}.".format(self.url_for_saved_files, filename))

        return False  # ChanSave does not use commands and should not return that it has handled one

    def _get_links(self, message) -> List[str]:
        http_message = re.sub("www\\.", message, re.IGNORECASE) \
            if re.match("www\\.", message, re.IGNORECASE) and not (
                re.match("http:", message) or re.match("https:", message)) \
            else message

        links = re.findall("http[^(\\s)]+", http_message, re.IGNORECASE)  # Match from http to next space to get links
        return links

    def _should_run(self, link) -> bool:
        return not hasattr(self, "disabled") and [re.match(url, link, re.IGNORECASE) for url in self.chan_regex_urls]

    def _get_file_extension(self, link):
        for extension in self.file_extensions_to_save:
            if re.match("\\.{}".format(extension), link, re.IGNORECASE):
                return extension

    def _save_media(self, room, user_id, link, file_extension) -> (str, str):
        filename = "{}.{}".format(uuid.uuid1(), file_extension)
        filepath = "{}{}".format(self.save_location, filename)

        request = self.requests.get(link, allow_redirects=True)
        open(filepath, 'wb').write(request.content)
        return (filepath, filename)
