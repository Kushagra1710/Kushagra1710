"""Generate self-contained profile SVGs. Run from the repository root."""
import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
USER = 'Kushagra1710'
BG = '#0d1117'
FG = '#c9d1d9'
GREEN = '#7ee787'

def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Kushagra1710-profile-art', 'Accept': '*/*'})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()

def svg(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title, quote=True)}">
<title>{html.escape(title)}</title>
<style>text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;fill:{FG}}}.line{{animation:reveal .5s both}}@keyframes reveal{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}@media(prefers-reduced-motion:reduce){{.line{{animation:none!important}}}}</style>
<rect width="{width}" height="{height}" rx="14" fill="{BG}"/>
{body}</svg>'''

def text(x, y, value, size=14, color=FG):
    return f'<text x="{x}" y="{y}" font-size="{size}" style="fill:{color}">{html.escape(value)}</text>'

def info_card():
    rows = [
        ('role', 'Software developer'), ('study', 'ECE · IIIT Bhopal'),
        ('focus', 'Backend · Kotlin Multiplatform'), ('practice', 'Competitive programming · DSA'),
        ('languages', 'C++ · Swift · Kotlin · Python'),
        ('build', 'SwiftUI · Compose · Firebase'),
        ('previous', 'SDE Intern · Xelron'), ('projects', 'CryptoVision · FreshCart · StaffSync'),
    ]
    body = text(26, 38, 'kushagra@github:~', 19, GREEN)
    body += text(26, 65, '────────────────────────────────────', 14, '#30363d')
    for i, (key, value) in enumerate(rows):
        y = 102 + i * 31
        body += f'<g class="line" style="animation-delay:{i*.12}s">' + text(26,y,key,12,GREEN) + text(125,y,value,12) + '</g>'
    body += text(26, 370, '$ build · learn · iterate', 13, '#8b949e')
    (ASSETS/'info-card.svg').write_text(svg(490,400,'Kushagra Sharma — developer profile',body))

def portrait(source=None):
    from PIL import Image, ImageOps, ImageEnhance
    raw = Path(source).read_bytes() if source else fetch('https://avatars.githubusercontent.com/u/118935536?s=640&v=4')
    im = Image.open(io.BytesIO(raw)).convert('RGBA')
    bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im)
    im = ImageOps.fit(bg.convert('L'), (66, 43))
    im = ImageEnhance.Contrast(ImageOps.autocontrast(im)).enhance(1.35)
    ramp = ' .:-=+*#%@'
    body = text(22,32,'$ whoami',14,GREEN)
    for row in range(43):
        line = ''.join(ramp[min(9, (255-im.getpixel((col,row)))*10//256)] for col in range(66))
        body += f'<g class="line" style="animation-delay:{row*.035:.3f}s"><text x="22" y="{53+row*7.3:.1f}" font-size="7" xml:space="preserve">{html.escape(line)}</text></g>'
    body += text(22,382,'Kushagra Sharma',13,GREEN)
    (ASSETS/'portrait.svg').write_text(svg(370,400,'ASCII portrait of Kushagra Sharma',body))

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.days = []; self.tips = {}; self.tip = None
    def handle_starttag(self,tag,attrs):
        a = dict(attrs)
        if a.get('data-date') and 'data-level' in a:
            self.days.append({'date':a['data-date'], 'level':int(a['data-level']), 'id':a.get('id',''), 'count':a.get('data-count')})
        if tag == 'tool-tip': self.tip = a.get('for'); self.tips[self.tip] = ''
    def handle_data(self,data):
        if self.tip is not None: self.tips[self.tip] += data
    def handle_endtag(self,tag):
        if tag == 'tool-tip': self.tip = None

def parse_calendar(raw):
    parser = CalendarParser(); parser.feed(raw)
    today = dt.datetime.now(dt.timezone.utc).date()
    days = []
    for day in parser.days:
        date = dt.date.fromisoformat(day['date'])
        if date > today: continue
        description = parser.tips.get(day['id'],'').strip()
        match = re.search(r'([\d,]+) contribution', description, re.I)
        if day['count'] is not None: count = int(day['count'])
        elif match: count = int(match[1].replace(',',''))
        elif re.search(r'No contributions',description,re.I): count = 0
        else: raise ValueError(f'Missing contribution count for {date}; GitHub markup may have changed')
        if not 0 <= day['level'] <= 4 or count < 0: raise ValueError('Invalid calendar data')
        days.append({'date':str(date),'level':day['level'],'count':count})
    days.sort(key=lambda d:d['date'])
    if len(days) < 350 or len({d['date'] for d in days}) != len(days):
        raise ValueError('Incomplete or duplicate calendar data; refusing to replace graph')
    return days

def heatmap():
    days = parse_calendar(fetch(f'https://github.com/users/{USER}/contributions').decode())
    start = dt.date.fromisoformat(days[0]['date'])
    start -= dt.timedelta(days=(start.weekday()+1)%7)
    palette = ['#161b22','#0e4429','#006d32','#26a641','#39d353']
    body = text(26,35,'$ ./contributions.sh',17,GREEN)
    month = None
    for day in days:
        date = dt.date.fromisoformat(day['date']); delta = (date-start).days
        col, row = divmod(delta,7); x = 40+col*14.5; y = 80+row*15
        if date.month != month and row == 0:
            month = date.month; body += text(x,65,date.strftime('%b'),10,'#8b949e')
        label = f"{day['date']}: {day['count']} contributions"
        body += f'<rect class="line" style="animation-delay:{(col+row)*.018:.3f}s" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{palette[day["level"]]}"><title>{label}</title></rect>'
    total = sum(d['count'] for d in days)
    body += text(26,220,f'{total:,} contributions · {days[0]["date"]} → {days[-1]["date"]}',13)
    body += text(672,220,'Less',10,'#8b949e')
    for i,color in enumerate(palette): body += f'<rect x="{704+i*16}" y="210" width="11" height="11" rx="2" fill="{color}"/>'
    body += text(791,220,'More',10,'#8b949e')
    output = svg(860,245,'GitHub contribution calendar for '+USER,body)
    (ASSETS/'contrib-heatmap.svg').write_text(output)
    (ASSETS/'contributions.json').write_text(json.dumps(days,indent=2)+'\n')

def placeholders():
    # Honest initial states until the first successful GitHub Actions run.
    if not (ASSETS/'portrait.svg').exists():
        body = text(25,35,'$ whoami',14,GREEN)+text(65,225,'KS',110,GREEN)+text(25,375,'Portrait loads after first workflow run',12)
        (ASSETS/'portrait.svg').write_text(svg(370,400,'Kushagra Sharma monogram — portrait pending',body))
    if not (ASSETS/'contrib-heatmap.svg').exists():
        body = text(26,35,'$ ./contributions.sh',17,GREEN)+text(26,120,'Contribution calendar awaiting its first sync.',16)+text(26,155,'GitHub Actions generates this from your real activity.',13,'#8b949e')
        (ASSETS/'contrib-heatmap.svg').write_text(svg(860,245,'Contribution calendar pending first sync',body))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--offline',action='store_true'); ap.add_argument('--photo'); args = ap.parse_args()
    info_card()
    if args.offline: placeholders()
    else:
        heatmap()
        portrait(args.photo)
