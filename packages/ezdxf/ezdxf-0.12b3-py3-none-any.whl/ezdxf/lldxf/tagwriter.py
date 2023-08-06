# Created: 13.01.2018
# Copyright (c) 2018-2020, Manfred Moitzi
# License: MIT License
from typing import Any, TextIO, TYPE_CHECKING, Union, List, Iterable, BinaryIO
from .types import TAG_STRING_FORMAT, cast_tag_value, DXFVertex
from .types import BYTES, INT16, INT32, INT64, DOUBLE, BINARY_CHUNK
from .tags import DXFTag, Tags
from .const import LATEST_DXF_VERSION
from ezdxf.tools import take2
import struct

if TYPE_CHECKING:
    from ezdxf.eztypes import ExtendedTags, DXFEntity

__all__ = ['TagWriter', 'BinaryTagWriter', 'TagCollector', 'basic_tags_from_text']


class TagWriter:
    """
    Writes DXF tags into a stream.

    Args:
        stream: text stream
        write_handles: if False don't write handles (5, 105), use only for DXF R12 format

    """

    def __init__(self, stream: TextIO, dxfversion=LATEST_DXF_VERSION, write_handles: bool = True):
        self._stream = stream
        # this are just options for export functions
        self.dxfversion = dxfversion
        self.write_handles = write_handles  # flag is needed for new new entity structure!
        # force writing optional values if equal to default value when set
        # True is only used for testing
        self.force_optional = False

    def write_tags(self, tags: Union['Tags', 'ExtendedTags']) -> None:
        for tag in tags:
            self.write_tag(tag)

    def write_tag(self, tag: DXFTag) -> None:
        self._stream.write(tag.dxfstr())

    def write_tag2(self, code: int, value: Any) -> None:
        self._stream.write(TAG_STRING_FORMAT % (code, value))

    def write_vertex(self, code: int, vertex: Iterable[float]) -> None:
        for index, value in enumerate(vertex):
            self.write_tag2(code + index * 10, value)

    def write_str(self, s: str) -> None:
        self._stream.write(s)


class BinaryTagWriter(TagWriter):
    """
    Writes binary encoded DXF tags into a binary stream.

    Args:
        stream: binary IO stream
        write_handles: if ``False`` don't write handles (5, 105), use only for DXF R12 format

    """

    def __init__(self, stream: BinaryIO, dxfversion=LATEST_DXF_VERSION, write_handles: bool = True, encoding='utf8'):
        super().__init__(None, dxfversion, write_handles)
        self._stream = stream
        self._encoding = encoding  # output encoding
        self._r12 = self.dxfversion <= 'AC1009'

    def write_signature(self) -> None:
        self._stream.write(b'AutoCAD Binary DXF\r\n\x1a\x00')

    def write_tags(self, tags: Union['Tags', 'ExtendedTags']) -> None:
        for tag in tags:
            self.write_tag2(tag.code, tag.value)

    def write_tag(self, tag: DXFTag) -> None:
        if isinstance(tag, DXFVertex):
            for code, value in tag.dxftags():
                self.write_tag2(code, value)
        else:
            self.write_tag2(tag.code, tag.value)

    def write_str(self, s: str) -> None:
        data = s.split('\n')
        for code, value in take2(data):
            self.write_tag2(int(code), value)

    def write_tag2(self, code: int, value: Any) -> None:
        # Binary DXF files do not support comments!
        assert code != 999
        if code in BINARY_CHUNK:
            self._write_binary_chunks(code, value)
        stream = self._stream

        # write group code
        if self._r12:
            # Special group code handling if DXF R12 and older
            if code >= 1000:  # extended data
                stream.write(b'\xff')
                # always 2-byte group code for extended data
                stream.write(code.to_bytes(2, 'little'))
            else:
                stream.write(code.to_bytes(1, 'little'))
        else:  # for R2000+ do not need a leading 0xff in front of extended data
            stream.write(code.to_bytes(2, 'little'))
        # write tag content
        if code in BYTES:
            stream.write(int(value).to_bytes(1, 'little'))
        elif code in INT16:
            stream.write(int(value).to_bytes(2, 'little', signed=True))
        elif code in INT32:
            stream.write(int(value).to_bytes(4, 'little', signed=True))
        elif code in INT64:
            stream.write(int(value).to_bytes(8, 'little', signed=True))
        elif code in DOUBLE:
            stream.write(struct.pack('<d', float(value)))
        else:  # write zero terminated string
            stream.write(str(value).encode(self._encoding, errors='dxfreplace'))
            stream.write(b'\x00')

    def _write_binary_chunks(self, code: int, data: bytes) -> None:
        # Split binary data into small chunks, 127 bytes is the
        # regular size of binary data in ASCII DXF files.
        CHUNK_SIZE = 127
        index = 0
        size = len(data)
        stream = self._stream

        while index < size:
            # write group code
            if self._r12 and code >= 1000:  # extended data, just 1004?
                stream.write(b'\xff')  # extended data marker
            # binary data does not exist in regular R12 entities,
            # only 2-byte group codes required
            stream.write(code.to_bytes(2, 'little'))

            # write max CHUNK_SIZE bytes of binary data in one tag
            chunk = data[index: index + CHUNK_SIZE]
            # write actual chunk size
            stream.write(len(chunk).to_bytes(1, 'little'))
            stream.write(chunk)
            index += CHUNK_SIZE


class TagCollector:
    """
    Collects DXF tags as DXFTag() entities for testing.

    """

    def __init__(self, dxfversion=LATEST_DXF_VERSION, write_handles: bool = True, optional: bool = True):
        self.tags = []
        self.dxfversion = dxfversion
        self.write_handles = write_handles  # flag is needed for new new entity structure!
        # force writing optional values if equal to default value when set
        # True is only used for testing
        self.force_optional = optional

    def write_tags(self, tags: Union['Tags', 'ExtendedTags']) -> None:
        for tag in tags:
            self.write_tag(tag)

    def write_tag(self, tag: DXFTag) -> None:
        if hasattr(tag, 'dxftags'):
            self.tags.extend(tag.dxftags())
        else:
            self.tags.append(tag)

    def write_tag2(self, code: int, value: Any) -> None:
        self.tags.append(DXFTag(code, cast_tag_value(int(code), value)))

    def write_vertex(self, code: int, vertex: Iterable[float]) -> None:
        for index, value in enumerate(vertex):
            self.write_tag2(code + index * 10, value)

    def write_str(self, s: str) -> None:
        self.write_tags(Tags.from_text(s))

    def has_all_tags(self, other: 'TagCollector'):
        return all(tag in self.tags for tag in other.tags)

    def reset(self):
        self.tags = []

    @classmethod
    def dxftags(cls, entity: 'DXFEntity', dxfversion=LATEST_DXF_VERSION):
        collector = cls(dxfversion=dxfversion)
        entity.export_dxf(collector)
        return Tags(collector.tags)


def basic_tags_from_text(text: str) -> List[DXFTag]:
    """
    Returns all tags from `text` as basic DXFTags(). All complex tags are resolved into basic (code, value) tags
    (e.g. DXFVertex(10, (1, 2, 3)) -> DXFTag(10, 1), DXFTag(20, 2), DXFTag(30, 3).

    Args:
        text: DXF data as string

    Returns: List of basic DXF tags (code, value)

    """
    collector = TagCollector()
    collector.write_tags(Tags.from_text(text))
    return collector.tags
