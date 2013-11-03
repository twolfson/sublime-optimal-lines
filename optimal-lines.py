import re
import sublime
import sublime_plugin

FIND_IN_FILES_SYNTAX = 'Packages/Default/Find Results.hidden-tmLanguage'

class OptimalLinesListener(sublime_plugin.EventListener):
    # When a file is loaded, highlight it and introduce our rulers
    def on_load(self, view):
        self.highlight_lines(view)
        self.adjust_rulers(view)

    # When a file is modified, highlight it
    def on_modified(self, view):
        # TODO: It would be ideal to re-highlight only if the indentation has
            # changed or line has been added/deleted
        self.highlight_lines(view)
        self.adjust_rulers(view)

    # When a selection is modified, update the rulers
    def on_selection_modified(self, view):
        self.adjust_rulers(view)

    # When we lose focus, reset the rulers
    def on_deactivated(self, view):
        # TODO: Use a common function to set the rulers
        # TODO: Extend default cursors (save on_load)
            # but that won't adjust for syntax specific
        view.settings().set('rulers', [])

    def get_optimal_limit(self, view):
        """Fetch the optimal line limit."""
        return view.settings().get('optimal_line_limit', 75)

    def highlight_lines(self, view):
        """Mark every character after 75 characters as over the limit."""
        # If we are in `Find in Files`, return
        if view.settings().get('syntax') == FIND_IN_FILES_SYNTAX:
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
            # DEV: Unfortunately, this plugin will not work with whitespace (language)
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
            text_limit = text_start + self.get_optimal_limit(view)
            if text_end > text_limit:
                regions.append(sublime.Region(text_limit, text_end))

        view.add_regions('optimize_lines_highlight',
                         regions,
                         'invalid.deprecated',  # Electric purple =3
                         sublime.HIDE_ON_MINIMAP |
                         sublime.DRAW_OUTLINED)

    def adjust_rulers(self, view):
        """Display a cursor at the typographic limit after a threshold."""
        # Collect all lines in selection
        lines = set()
        for region in view.sel():
            for line in view.lines(region):
                lines.add(line)

        # TODO: Filter out lines which are not close to their limit

        # Find the common starting points of each line
        # TODO: This is copy/paste. Stop that.
        starting_points = set()
        for line in lines:
            text = view.substr(line)
            starting_char = re.match(r'\s*([^\s])', text)

            # DEV: This section is not copy/pate
            starting_pt = 0
            if starting_char:
                starting_pt(starting_char.start(1))
            starting_points.add(starting_pt)

        # Map the end points
        distance = self.get_optimal_limit(view)
        end_points = map(lambda pt: pt + distance, starting_points)

        # Draw the rulers
        view.settings().set('rulers', end_points)
