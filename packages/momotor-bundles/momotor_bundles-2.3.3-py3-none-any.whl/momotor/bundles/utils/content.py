from pyxb.binding.basis import NonElementContent

from momotor.bundles.utils.encoding import decode_data, encode_data

__all__ = ['decode_content', 'encode_content']


def decode_content(node, encoding):
    content = ''.join(
        element.value
        for element in node.orderedContent()
        if isinstance(element, NonElementContent)
    )

    if content:
        if encoding:
            return decode_data(content, encoding)

        return content


def encode_content(content):
    if content:
        encoded, encoding = encode_data(content)
    else:
        encoded, encoding = None, None

    return encoded, encoding
