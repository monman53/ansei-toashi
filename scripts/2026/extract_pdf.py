import json
import re
from pathlib import Path
import pdfplumber

HERE = Path(__file__).parent
PDF_PATH = HERE / 'program2026.pdf'
OUT_PATH = HERE.parent.parent / 'public' / 'data' / '2026' / 'participants.json'

TOGE_PAGES = range(21, 25)      # PDF pages 21-24 (峠コース)
SEKISHO_PAGES = range(25, 60)   # PDF pages 25-59 (関所・坂本宿コース)

HEADER_PATTERNS = [
    re.compile(r'^第\d+回安政遠足参加者名簿'),
    re.compile(r'^NO\s+氏名\s+性別'),
]

ROW_RE = re.compile(
    r'^(\d+)\s+(.+?)\s+(男性|女性)\s+(.+?[都道府県])\s+(仮装する|仮装しない)\s*(\d+)?\s*$'
)
ROW_RE_NO_COSTUME = re.compile(
    r'^(\d+)\s+(.+?)\s+(男性|女性)\s+(.+?[都道府県])\s+(\d+)?\s*$'
)


def is_header(line):
    return any(p.match(line) for p in HEADER_PATTERNS)


def parse_page(text, page_num, course):
    results = []
    for line in text.splitlines():
        line = line.strip()
        if not line or is_header(line):
            continue
        m = ROW_RE.match(line)
        if m:
            no, name, gender, pref, costume, times_str = m.groups()
            results.append({
                'no': int(no),
                'name': name.strip(),
                'name_kana': '',
                'gender': gender,
                'prefecture': pref,
                'costume': costume,
                'times': int(times_str) if times_str else None,
                'course': course,
                'source_page': page_num,
            })
        else:
            m2 = ROW_RE_NO_COSTUME.match(line)
            if m2:
                no, name, gender, pref, times_str = m2.groups()
                results.append({
                    'no': int(no),
                    'name': name.strip(),
                    'name_kana': '',
                    'gender': gender,
                    'prefecture': pref,
                    'costume': '',
                    'times': int(times_str) if times_str else None,
                    'course': course,
                    'source_page': page_num,
                })
                print(f'  [p{page_num}] missing costume: {line!r}')
            else:
                print(f'  [p{page_num}] unmatched: {line!r}')
    return results


def main():
    participants = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num in TOGE_PAGES:
            text = pdf.pages[page_num - 1].extract_text() or ''
            participants.extend(parse_page(text, page_num, '峠コース'))

        for page_num in SEKISHO_PAGES:
            text = pdf.pages[page_num - 1].extract_text() or ''
            participants.extend(parse_page(text, page_num, '関所・坂本宿コース'))

    # Deduplicate by (course, no) — keep last in case of page-boundary duplicates
    seen = {}
    for p in participants:
        seen[(p['course'], p['no'])] = p
    participants = sorted(seen.values(), key=lambda p: (p['course'], p['no']))

    OUT_PATH.write_text(json.dumps(participants, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'\nTotal: {len(participants)} participants')
    toge = sum(1 for p in participants if p['course'] == '峠コース')
    sekisho = sum(1 for p in participants if p['course'] == '関所・坂本宿コース')
    print(f'  峠コース:    {toge}')
    print(f'  関所コース: {sekisho}')
    missing_times = sum(1 for p in participants if p['times'] is None)
    print(f'  参加回数なし: {missing_times}')
    print(f'\n出力: {OUT_PATH}')


if __name__ == '__main__':
    main()
