# fixit

## 1、XSS

markdown imgurl 正则修改

* 修改 `inlinepatterns.py`

```python
IMAGE_LINK_RE = r'\!' + BRK + r'\s*\(\s*(<.*?>|([^"\)\s]+\s*"[^"]*"|[^\)\s]*))\s*\)'
```

## 2、url 判断修改

```python
def sanitize_url(self, url):
	try:
            scheme, netloc, path, params, query, fragment = url = urlparse(url)
        except ValueError:  # pragma: no cover
            # Bad url - so bad it couldn't be parsed.
            return ''

        locless_schemes = ['', 'mailto', 'news']
        allowed_schemes = locless_schemes + ['http', 'https', 'ftp', 'ftps']
        if scheme not in allowed_schemes:
            # Not a known (allowed) scheme. Not safe.
            return ''

        if netloc == '' and scheme not in locless_schemes:  # pragma: no cover
            # This should not happen. Treat as suspect.
            return ''

        for part in url[2:]:
            if ":" in part:
                # A colon in "path", "parameters", "query"
                # or "fragment" is suspect.
                return ''

        # Url passes all tests. Return url as-is.
        return urlunparse(url)
```

## 3、实体化过滤

修改 `serializers.py`

* 增加过滤 `&` 、 `"`