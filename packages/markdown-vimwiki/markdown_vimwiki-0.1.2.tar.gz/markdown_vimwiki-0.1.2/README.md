markdown\_vimwiki
=================

Python Markdown extension for useful vimwiki additions

Todo lists
----------

The plugin supports the standard vimwiki style todo lists:

```markdown
* [ ] To do
* [.] 0-33% complete
* [o] 33-66% complete
* [O] 66-99% complete
* [X] 100% complete
* [-] rejected
```

leads to:

```html
<ul>
<li class="done0"> done0</li>
<li class="done1"> done1</li>
<li class="done2"> done2</li>
<li class="done3"> done3</li>
<li class="done4"> done4</li>
<li class="rejected"> rejected</li>
</ul>
```

By default, it uses all the same defaults as vimwiki's syntax. That is, it uses `.oOX` for `g:vimwiki_listsyms` and `-` for `g:vimwiki_listsym_rejected`, and applies the CSS classes used by the default HTML generation tool.

These are customizable. For the following markdown:

```markdown
* [i] yip
* [a] yap
* [o] yop
```

expecting:

```html
<ul>
<li class="yip"> yip</li>
<li class="yap"> yap</li>
<li class="yop"> yop</li>
</ul>
```

configure as follows:

```python
markdown(source, extensions=[VimwikiExtension(
    list_levels='iao',
    list_classes=['yip', 'yap', 'yop'])])
```

Tags
----

The plugin currently supports styling tags (but nothing else):

```markdown
:lorem:ipsum:
```

leads to:

```html
<p><span class="tag">lorem</span> <span class="tag">ipsum</span></p>
```

The class used is customizable with the `tag_class` config option.
