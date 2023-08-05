
#  Copyright (c) 2020 Jean-François MARQUIS
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import re
import tempfile

from google.cloud.exceptions import NotFound
from google.cloud.storage import Client
from google.cloud.storage.blob import Blob


def download_content_from_file(url):
    blob = _get_blob(url)

    with tempfile.NamedTemporaryFile() as temp_file:
        temp_filename = temp_file.name
        blob.download_to_filename(temp_filename)
        with open(temp_filename, "r") as temp_file_reader:
            return temp_file_reader.read()


def _get_blob(url: str) -> Blob:
    """
    Get an existing blob object from a GCS URL.
    :param url: GCS blob URL
    :return: The blob object
    :raises: :class:`google.cloud.exceptions.NotFound`
    """
    bucket_name, bucket_path = split_url(url)
    bucket = Client().get_bucket(bucket_name)
    if not bucket:
        raise NotFound(f"Unable to get bucket (path: '{url}', bucket: '{bucket_name}')")

    blob = bucket.get_blob(bucket_path)
    if not blob:
        raise NotFound(f"Unable to get blob (path: '{url}', bucket: '{bucket_name}', blob: '{bucket_path}')")

    return blob


def split_url(url: str) -> (str, str):
    """
    Extract bucket name and blob path from a GCS URL.
    If path matches a root bucket path, returned blob path is an empty string.
    :param url: GCS URL
    :return: A tuple containing bucket name and blob path
    :raise ValueError when URL is invalid
    """
    match = re.match("^gs://([a-zA-Z0-9_-]+)/(.*)$", url)
    if not match:
        match_bucket = re.match("^gs://([a-zA-Z0-9_-]+)$", url)
        if not match_bucket:
            raise ValueError(f"URL is invalid: {url}")
        return match_bucket.group(1), ""

    bucket_name = match.group(1)
    bucket_path = match.group(2)

    return bucket_name, bucket_path
