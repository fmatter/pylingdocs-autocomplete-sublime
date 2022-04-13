import sublime
import sublime_plugin
import logging
import json
import os

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class GRAMRAutocomplete(sublime_plugin.EventListener):

    data = None

    def on_post_save(self, view):
        window = view.window()
        current_dir = os.path.dirname(view.file_name())
        path = os.path.join(current_dir, ".autocomplete_data.json")
        if os.path.isfile(path):
            self.data = json.load(open(path, "r"))
        else:
            self.data = [("mp:", "[mp]()")]

    def on_query_completions(self, view, prefix, locations):
        logging.debug(str(view) + str(prefix) + str(locations))
        logging.debug(self.data)
        return self.data