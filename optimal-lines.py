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
        regions = [sublime.Region(0, 5)]
        view.add_regions('optimize_lines_highlight',
                         regions,
                         'markup.inserted',
                         sublime.HIDE_ON_MINIMAP)
