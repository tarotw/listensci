#!/usr/bin/env python3
"""Export a JSON mapping of episode titles to their MP3 URLs from soundon.xml."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def extract_title_url_map(xml_path: Path) -> dict[str, str]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    channel = root.find('channel')
    if channel is None:
        raise ValueError('XML does not contain a <channel> element')

    mapping: dict[str, str] = {}
    for item in channel.findall('item'):
        title_elem = item.find('title')
        enclosure_elem = item.find('enclosure')

        if title_elem is None or enclosure_elem is None:
            continue

        title_text = title_elem.text or ''
        enclosure_url = enclosure_elem.attrib.get('url')
        if not enclosure_url:
            continue

        mapping[title_text.strip()] = enclosure_url.strip()

    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('xml_path', type=Path, help='Path to soundon.xml file')
    parser.add_argument('output_path', type=Path, help='Destination JSON file')
    parser.add_argument('--indent', type=int, default=2, help='Indentation for JSON output')
    args = parser.parse_args()

    mapping = extract_title_url_map(args.xml_path)
    args.output_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=args.indent) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
