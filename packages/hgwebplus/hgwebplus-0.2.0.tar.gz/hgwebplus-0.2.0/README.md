# hgwebplus

hgwebplus is a [mercurial](https://mercurial-scm.org/) extension that enhances
the normal hgweb tooling so that theme authors can create more robust themes.

It's built as an extension mainly to try out new things before attempting to
get them upstreamed.  Also, due to the Bitbucket death clock, I couldn't wait
for an upstream release.

All screen shots are from my
[hgkeeper-theme](https://keep.imfreedom.org/grim/hgkeeper-theme).

# Features

hgwebplus was created during the development of
[hgkeeper-theme](https://keep.imfreedom.org/grim/hgkeeper-theme) as a way to
make the theme look more like current code hosting sites.

Everything has been built to be backwards compatible, to keep existing themes
working.  However, this code has only been tested on Python3 and Python2 is
considered unsupported right now.

## Readme Rendering

The most notable feature is that a new template keyword named `readme` has been
added.  Since this is a keyword, it can be used in any template.  This keyword
will look for files named `README.md`, `README.txt`, and `README` in a case
insensitive fashion, and return their contents rendered to HTML.

**Please note, that at this time, images do not yet work.**

The Markdown rendering uses [cmarkgfm](https://pypi.org/project/cmarkgfm/) to
support GitHub Flavored Markdown.  However, there is no styling associated with
this render.  To do that, I recommend you use [sindresorhus's
github-markdown-css](https://github.com/sindresorhus/github-markdown-css/) in
your theme and addjust it accordingly.

For plain text, the HTML rendering is just literally prefixing line endings
with a `<br/>`.

## Gravatar Support

This is a bit of a misnomer as there isn't actually a
[Gravatar](https://gravatar.com/) filter/keyword, but hgwebplus adds an `md5`
filter that allows you to create Gravatar links.

With the `md5` filter you can then display a Gravatar for an author with the
example below:

```
<img src="https://www.gravatar.com/avatar/{author|email|mailmap|strip|lower|md5}?s=36" decoding="async">
```

At some point, we'll probably build a proper function where you don't need to
know the specifics of the Gravatar API, but for now this works.

## Diff Rendering

The stock diff rendering in hgweb leaves a bit to be desired.  When rendering
the lines of the diffs, you don't have the correct line numbers, nor the file
names, nor the file revisions all of which make it impossible to link to the
original revision for further viewing.

Therefore, hgwebplus exposes all of these to the diffs templates and allows
you to create something similar to the screenshot below.

![diff screenshot](images/diff.png)

## Diffstat

The diffstat template has been modified to give you the number of lines added
and removed as well as a boolean telling you if the file is binary or not.

With these changes you can create something like the below screen shot:

![diffstat example](images/diffstat.png)

# Issues

If you have any issues with this extension, please file them at
[issues.imfreedom.org/hgwebplus](https://issues.imfreedom.org/hgwebplus).

# Installation

Release are done purely via [pypi](https://pypi.org/project/hgwebplus/) and
can be installed a few ways.

## Mercurial Installed via Package Manager

If your Mecurial is installed via your package manager, you may choose to
install hgwebplus to the system path, but this typically requires sudo access.
If you choose to go this route, you can use the following command to install
hgwebplus.

```
pip3 install hgwebplus
```

Once it's done installing, you can modify your `~/.hgrc` and add the make
sure your `[extensions]` section contains the following:

```
[extensions]
hgext3rd.hgwebplus =
```

If you would rather not install hgwebplus system wide, you can instead install
it to your user directory with the following command:

```
pip3 install --user hgwebplus
```

Once this is installed, you'll have to update your `~/.hgrc` to look something
like the following replacing the `?` with your version of Python:

```
[extensions]
hgext3rd.evolve = ~/.local/lib/python3.?/site-packages/hgext3rd/
```

## Mercurial Installed Via pip

If you've installed mercurial via `pip3 --user` then you can just install
hgwebplus in the same manner with

```
pip3 install --user hgwebplus
```

After installation you just need to tell Mercurial about it by making sure
that your `~/.hgrc` `[extensions]` section contains the following:

```
[extensions]
hgext3rd.hgwebplus =
```
