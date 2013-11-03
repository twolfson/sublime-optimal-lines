import re
import sublime
import sublime_plugin

FIND_IN_FILES_SYNTAX = 'Packages/Default/Find Results.hidden-tmLanguage'

class OptimalLinesListener(sublime_plugin.EventListener):
    # When a file is loaded, highlight it
    def on_load(self, view):
        self.highlight_lines(view)

    # When a file is modified, highlight it
    def on_modified(self, view):
        # TODO: It would be ideal to re-highlight only if the indentation has
            # changed or line has been added/deleted
        self.highlight_lines(view)

    def highlight_lines(self, view):
        # If we are in `Find in Files`, return
        view_settings = view.settings()
        if view_settings.get('syntax') == FIND_IN_FILES_SYNTAX:
            return

        # TODO: Don't highlight quick panel (see 173226f)
        # Collect the lines
        file_region = sublime.Region(0, view.size())
        lines = view.lines(file_region)

        # Create a collection var for regions
        regions = []

        # For each line
        for line in lines:
            # Find the starting character
            # DEV: Unfortunately, this plugin will not work with whitespace (the programming language)
            # TODO: It might be worthwhile to detect syntax of whitespace and use a different regexp
            text = view.substr(line)
            starting_char = re.match(r'\s*([^\s])', text)

            # If there is no starting character, skip the line
            if not starting_char:
                continue

            # Grab the start
            text_start = line.begin() + starting_char.start(1)

            # If we are over 65 characters, mark the violating characters
            # TODO: Make `text_limit` font-size and settings based
            # TODO: Although, that wouldn't be very cross-developer friendly
            text_end = line.end()
            text_limit = text_start + view_settings.get('optimal_line_limit', 75)
            if text_end > text_limit:
                regions.append(sublime.Region(text_limit, text_end))

        view.add_regions('optimize_lines_highlight',
                         regions,
                         'invalid.deprecated',  # Electric purple =3
                         sublime.HIDE_ON_MINIMAP |
                         sublime.DRAW_OUTLINED)
