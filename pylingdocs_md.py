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
        


class PldChooseCommand(sublime_plugin.TextCommand):

    items = None
    values = None

    def __init__(self, view):
        super().__init__(view)
        current_dir = os.path.dirname(self.view.file_name())
        path = os.path.join(current_dir, ".pld_menudata.json")
        if os.path.isfile(path):
            items = list(json.load(open(path, "r")).keys())
            values = json.load(open(path, "r"))
        else:
            items = []
            values = []
        self.items = items
        self.values = values

    def on_done(self, result):
        self.view.run_command("pld_choose_entity", {"choices": self.values[self.items[result]]})
        
    def run(self, edit, **kwargs):
        window = sublime.active_window()
        window.show_quick_panel(self.items, self.on_done)
        


class PldChooseEntityCommand(sublime_plugin.TextCommand):

    data = None
        
    def on_done(self, text):
        self.view.run_command("pld_insert", {"value": text})
    
    def run(self, edit, choices, **kwargs):
        window = sublime.active_window()
        choice_str = [y["content"][0] for y in choices]
        window.show_quick_panel(choice_str, lambda x: self.on_done(choices[x]["content"][1]))

class PldInsertCommand(sublime_plugin.TextCommand):

    def run(self, edit, value, **kwargs):
        self.view.insert(edit, self.view.sel()[0].begin(), value)