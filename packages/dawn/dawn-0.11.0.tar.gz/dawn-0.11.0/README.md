## dawn

A minimalist ePub parsing/writing library, that handle both ePub 2.0 and 3.0.


#### Basic usage:

```python
import dawn


def ser_toc_item(it):
	res = {'href': it.href, 'title': it.title}
	if it.children:
		res['children'] = [ser_toc_item(c) for c in it.children]
	return res
with open('input.epub', 'rb') as f, dawn.open(f) as epub:
	print({
		'uid': repr(epub.uid),
		'version': epub.version,
		'spine': [v.iid for v in epub.spine],
		'manifest': {k: [v.iid, v.href, v.mimetype] for k, v in epub.manifest.items()},
		'toc': [epub.toc.title, [ser_toc_item(it) for it in epub.toc]],
		'meta': {k: repr(v) for k, v in epub.meta.items()},
	})

with open('output.epub', 'wb') as f, dawn.open(f, mode='w', version='3.0') as epub:
	epub.meta['creators'] = [dawn.AS('Me', role='aut')]
	epub.meta['description'] = dawn.AS('Awesome book')
	epub.meta['title'].append(dawn.AS('My ePub', lang='en'))

	for href, path, title in [
		('README.md', 'README.html', 'README'),
		('dawn/__init__.py', 'dawn.htm', 'dawn'),
	]:
		with open(href, 'r') as f:
			html = ''.join((
				'<html xmlns="http://www.w3.org/1999/xhtml">',
					'<head><title></title></head>',
					'<body><pre id="someanchor">{}</pre></body>',
				'</html>',
			)).format(f.read())
			item = epub.writestr(path, html)
		epub.spine.append(item)
		epub.toc.append(path, title=title)

	epub.toc.append('README.html', 'main title', [
		('README.html', 'sub title'),
		('dawn.htm', 'sub title2', [
			('dawn.htm#someanchor', 'sub sub title'),
		]),
	])
```
