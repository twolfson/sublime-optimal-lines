import re
import sublime
import sublime_plugin


class OptimalLinesListener(sublime_plugin.EventListener):
    # When a file is loaded, highlight it
    def on_load(self, view):
        self.highlight_lines(view)

    # When a file is modified, highlight it
    def on_modified(self, view):
        # TODO: It would be ideal to re-highlight only if the indentation has changed or line has been added/deleted
        self.highlight_lines(view)

    def highlight_lines(self, view):
        # TODO: Don't highlight quick panel or Find in Files
        # Collect the lines
        file_region = sublime.Region(0, view.size())
        lines = view.lines(file_region)
        # print view.settings().get('syntax')
        print view.scope_name(0)

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
            text_limit = text_start + 65
            if text_end > text_limit:
                regions.append(sublime.Region(text_limit, text_end))

        view.add_regions('optimize_lines_highlight',
                         regions,
                         'invalid.deprecated',  # Electric purple =3
                         sublime.HIDE_ON_MINIMAP |
                         sublime.DRAW_OUTLINED)
