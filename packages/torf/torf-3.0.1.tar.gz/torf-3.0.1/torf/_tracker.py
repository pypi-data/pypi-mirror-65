# This file is part of torf.
#
# torf is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# torf is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with torf.  If not, see <https://www.gnu.org/licenses/>.

import urllib.parse
import binascii


def download_torrent(infohash, announce_urls):
    infohash_encoded = urllib.parse.quote_from_bytes(binascii.unhexlify(infohash))
    # I couldn't find any documentation for the "/file?..." GET request.
    # Found it here: https://stackoverflow.com/a/1019588
    url = f'http://torrent.ubuntu.com:6969/file?info_hash={infohash_encoded}'
    print(url)
