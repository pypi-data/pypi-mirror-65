from .gomanga_co import GoMangaCo


class JapScanCom(GoMangaCo):
    _name_re = r'\.(?:com|cc|co|to)/[^/]+/([^/]+)/'
    _content_str = '{}/manga/{}/'
    _chapters_selector = '#chapters_list .chapters_list a'

    def get_archive_name(self) -> str:
        idx = self.chapter_id, self.get_chapter_index()
        return self.normal_arc_name({'vol': idx})

    def manga_name(self) -> str:
        raise RuntimeError(
            'Provider not worked. See https://github.com/manga-py/manga-py/issues/262#issuecomment-609092313'
        )

    def get_chapter_index(self) -> str:
        selector = r'\.(?:com|cc|co|to)/[^/]+/[^/]+/(\d+)/'
        return self.re.search(selector, self.chapter).group(1)

    def get_files(self):
        n = self.http().normalize_uri
        parser = self.html_fromstring(self.chapter)

        base_url = self.base_url(parser)
        images = self._images_helper(parser, '#pages option', 'data-img')

        return [n(base_url+i) for i in images]

    def base_url(self, parser):
        base_url = parser.cssselect('#image')[0].get('data-src')
        return self.re.search(r'(.+/)\w+\.\w{2,7}', base_url).group(1)


main = JapScanCom
