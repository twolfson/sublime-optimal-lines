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
            start = line.begin() + starting_char.start(1)

            # Count 65 characters from the character
            # TODO: Figure out how to highlight past a character
            # TODO: This is a limitation of Sublime Text. It should extend beyond the region for proper effect.
            # TODO: Make this font-size and settings based
            # end = start + 65
            end = min(start + 65, line.end())

            # Add the region to be highlighted
            regions.append(sublime.Region(start, end))

        view.add_regions('optimize_lines_highlight',
                         regions,
                         'optimal-lines',
                         # sublime.HIDE_ON_MINIMAP +
                         # sublime.DRAW_OUTLINED)
                         sublime.HIDDEN)
