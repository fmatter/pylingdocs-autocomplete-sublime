import sublime
import sublime_plugin
import logging
import json
import os

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class PLDAutocomplete(sublime_plugin.EventListener):

    data = None 

    def on_post_save(self, view):
        current_dir = os.path.dirname(view.file_name())
        path = os.path.join(current_dir, ".pld_autocomplete.json")
        if os.path.isfile(path):
            self.data = json.load(open(path, "r"))
        else:
            self.data = []

    def on_query_completions(self, view, prefix, locations):
        return self.data
        