import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


LEVELS = '- .oOX'
CLASSES = ['rejected', 'done0', 'done1', 'done2', 'done3', 'done4']


class VimwikiExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'list_levels': [LEVELS,
                'valid checklist levels per ":h g:vimwiki_listsyms" '
                '(begin with g:vimwiki_listsym_rejected)'],
            'list_classes': [CLASSES,
                'CSS classes corresponding to each of the levels'],
            'tag_class': ['tag', 'CSS class for rendering tags'],
        }
        super(VimwikiExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        list_levels = self.getConfig('list_levels')
        list_classes = self.getConfig('list_classes')
        todo_postprocessor = VimwikiTodoPostprocessor(
            list_levels, list_classes, md)
        md.postprocessors.register(todo_postprocessor, 'vimwiki_todo', 20)

        tag_class = self.getConfig('tag_class')
        tags_postprocessor = VimwikiTagsPostprocessor(tag_class, md)
        md.postprocessors.register(tags_postprocessor, 'vimwiki_tags', 20)


class VimwikiTodoPostprocessor(Postprocessor):
    """
    adds checklist class to list element
    """

    def __init__(self, levels, classes, *args, **kwargs):
        self.levels = levels
        self.classes = classes
        self.item_pattern = re.compile(
            r'^<li>\[([' + self.levels + r'])\](.*)</li>$', re.MULTILINE)
        super(VimwikiTodoPostprocessor, self).__init__(*args, **kwargs)

    def run(self, html):
        return re.sub(self.item_pattern, self._convert_item, html)

    def _convert_item(self, match):
        level, caption = match.groups()
        return '<li class="{}">{}</li>'.format(
            self.classes[self.levels.index(level)], caption)


class VimwikiTagsPostprocessor(Postprocessor):
    """
    styles vim tags (:tag1:tag2: etc)

    Currently requires the tags to be on a line by themselves.
    """

    tags_pattern = re.compile(r'^<p>:(\w[\S:]+\w):</p>$', re.MULTILINE)

    def __init__(self, tag_class, *args, **kwargs):
        self.tag_class = tag_class
        super(VimwikiTagsPostprocessor, self).__init__(*args, **kwargs)

    def run(self, html):
        return re.sub(self.tags_pattern, self._convert_tags, html)

    def _convert_tags(self, match):
        tags = match.group(1).split(':')
        return '<p>{}</p>'.format(
            ' '.join(['<span class="{}">{}</span>'.format(self.tag_class, t)
                for t in tags]))


def makeExtension(**kwargs):
    return VimwikiExtension(**kwargs)
