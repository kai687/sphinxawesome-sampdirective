# Sphinx awesome sampdirective

> **Warning**: **This project is in archive mode.** The ability to highlight placeholder variables in code blocks is much better addressed either by custom JavaScript or by post-processing the syntax-highlighted block. If you want to see an example of the latter, see the [Awesome Sphinx theme](https://github.com/kai687/sphinxawesome-theme).

The awesome `sampdirective` extension can be used to highlight placeholder variables in code blocks,
much like Sphinx's [`samp`](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-samp) interpreted text role.

## Install

Install the extension:

```console
pip install sphinxawesome-sampdirective
```

This Sphinx extension works with Python versions newer than 3.6 and recent Sphinx
releases.

## Configure

To enable this extension in Sphinx, add it to the list of extensions in the Sphinx
configuration file `conf.py`:

```python
extensions = ["sphinxawesome.sampdirective"]
```

## Use

Include the directive in your documents:

```
.. samp::

   $ echo {USERNAME}
```

`USERNAME` becomes an _emphasized_ node. In many outputs, it will be rendered as
_`USERNAME`_. For example, in HTML, the above example is rendered as:

```HTML
<pre>
  <span class="gp">$</span> echo <em class="var">USERNAME</em>
</pre>
```

You can then style the emphasized element with the `.var` class in CSS.
If the code block begins with a prompt character (`#`, `$`, or `~`), they are higlighted as well.

## Caveat

This extension does not provide full syntax highlighting. It is currently not possible
to have code blocks with both markup _and_ syntax highlighting. You have to choose
between the following:

- If you need to render markup, for example links, bold, or italic text, choose the
  `parsed-literal` directive.
- If you just want to highlight a placeholder variable, use the `samp` directive
  provided by this extension.
- If you need full syntax highlighting, use the `code-block` directive.
