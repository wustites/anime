"""Build self-contained, seekable SVG storybook compositions.

Run python3 storybook/build.py after editing the illustrations or choreography.
Each generated index.html remains independently previewable and renderable.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = '#493b36'


def group(content, x=0, y=0, scale=1, cls=''):
    # Separate authored placement from animated transforms.
    return f'<g transform="translate({x} {y}) scale({scale})"><g class="{cls}">{content}</g></g>'


def ellipse(x, y, rx, ry, fill, cls='', stroke='none', sw=4):
    return f'<ellipse class="{cls}" cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def path(d, fill, cls='', stroke=INK, sw=5):
    return f'<path class="{cls}" d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'


def cloud(x, y, scale=1):
    return group(path('M0 52 Q-12 14 32 18 Q48 -28 93 7 Q130 -10 155 24 Q201 13 212 52 Z', '#fff5df', stroke='none') + path('M27 52 H185', 'none', stroke='#f0c8a6', sw=3), x, y, scale, 'cloud')


def foliage(x, y, scale=1, color='#446e5b'):
    leaves = path('M0 170 Q28 75 20 0 M4 135 Q-50 106 -59 65 Q-10 69 8 112 M12 97 Q62 69 79 24 Q26 24 18 68 M18 52 Q-8 31 -9 1', 'none', stroke=color, sw=8)
    leaves += path('M3 135 Q-57 132 -69 77 Q-13 86 3 135 M11 97 Q68 97 91 31 Q41 37 11 97 M18 55 Q-20 43 -22 -8 Q10 3 18 55', color, stroke='none')
    return group(leaves, x, y, scale, 'plant')


def tree(x, y, scale=1, color='#648c6b'):
    art = path('M100 390 L110 205 M107 286 L47 224 M110 265 L164 205', 'none', stroke='#8e6d51', sw=21)
    art += path('M20 230 Q-30 174 24 122 Q1 60 68 59 Q85 1 147 23 Q193 17 199 75 Q252 90 222 148 Q267 216 204 245 Q140 277 100 237 Q52 267 20 230Z', color, stroke='none')
    art += path('M49 126 Q78 104 102 119 M145 79 Q173 89 166 111 M157 193 Q189 202 201 184', 'none', stroke='#abc28a', sw=7)
    return group(art, x, y, scale, 'tree')


def flower(x, y, scale=1):
    art = path('M0 30 L-2 -12 M0 17 Q22 4 20 -4 M0 24 Q-24 12 -20 3', 'none', stroke='#67845d', sw=5)
    for dx, dy in ((-12, -18), (0, -29), (12, -18), (7, -6), (-7, -6)):
        art += ellipse(dx, dy, 9, 10, '#e99673')
    art += ellipse(0, -17, 7, 7, '#f8ce63')
    return group(art, x, y, scale, 'flower')


def scenery(kind='meadow'):
    sky = '#f8dfb9' if kind == 'mountain' else '#f4e5cb'
    art = f'<rect width="1920" height="1080" fill="{sky}"/>'
    art += ellipse(1490, 225, 115, 115, '#edb861', 'sun')
    art += ellipse(1490, 225, 155, 155, 'none', stroke='#f1cd8e', sw=25)
    art += cloud(220, 175, 1.5) + cloud(1140, 130, .9) + cloud(1650, 350, .75)
    if kind == 'mountain':
        art += path('M0 750 L165 370 L370 585 L670 250 L940 655 L1190 350 L1520 680 L1790 320 L1920 650 V1080 H0Z', '#88a69a', 'distant', stroke='none')
        art += path('M0 810 L340 510 L520 750 L820 440 L1080 740 L1430 490 L1750 740 L1920 600 V1080 H0Z', '#b4b69a', stroke='none')
    else:
        art += path('M0 640 Q240 435 610 625 Q1030 340 1390 605 Q1720 420 1920 615 V1080 H0Z', '#9eb6a0', 'distant', stroke='none')
        art += path('M0 770 Q310 561 705 732 Q1130 526 1520 720 Q1770 614 1920 737 V1080 H0Z', '#6f927a', stroke='none')
        for x, y, s in ((-50, 340, 1.1), (260, 370, .75), (1450, 400, .9), (1720, 315, 1.15)):
            art += tree(x, y, s)
    art += path('M0 850 Q540 702 1050 820 Q1540 705 1920 815 V1080 H0Z', '#d8c397', stroke='none')
    art += path('M0 938 Q750 825 1920 911', 'none', stroke='#ead6ad', sw=95)
    for x, y, s in ((70, 875, .65), (320, 940, .85), (1610, 887, .7), (1800, 970, .95), (1380, 928, .45)):
        art += flower(x, y, s)
    art += group(ellipse(0, 0, 40, 12, '#9eae82') + ellipse(65, 12, 28, 9, '#bac596'), 640, 900)
    return art


def foreground():
    art = foliage(75, 1100, 1.4) + foliage(1860, 1090, 1.7, '#345d51')
    art += path('M0 1044 Q180 1010 340 1080 H0Z', '#587f60', stroke='none')
    art += path('M1520 1080 Q1760 979 1920 1042 V1080Z', '#446e5b', stroke='none')
    return art


def crow():
    art = ''
    art += path('M222 175 L309 181 L261 211 L308 219 L224 234Z', '#343f47', 'tail')
    art += group(path('M0 0 L-5 47 L-26 53 M-5 47 L17 55', 'none', stroke='#b47743', sw=9), 134, 210, cls='leg leg-a')
    art += group(path('M0 0 L2 47 L-16 57 M2 47 L25 52', 'none', stroke='#b47743', sw=9), 204, 210, cls='leg leg-b')
    art += path('M74 113 Q131 69 219 116 Q269 164 230 215 Q164 258 84 202 Q38 170 74 113Z', '#35424e', 'torso')
    art += group(path('M97 139 Q147 101 216 153 Q210 204 151 211 Q88 200 97 139Z', '#526271')
                 + path('M113 168 Q163 153 201 167 M120 187 Q156 177 184 188', 'none', stroke='#758694', sw=4), cls='wing')
    head = path('M39 47 Q54 -4 105 26 L123 9 L124 35 Q167 75 126 119 Q73 141 34 98Z', '#35424e')
    head += path('M42 72 L-15 90 L43 106Z', '#d8a94f')
    head += path('M-6 92 L40 91', 'none', stroke='#937149', sw=3)
    head += ellipse(74, 65, 23, 25, '#fffaeb', 'eye') + ellipse(66, 68, 10, 12, '#28313a', 'pupil') + ellipse(63, 64, 3.5, 4, '#fff')
    head += ellipse(53, 106, 12, 5, '#cb876b')
    head += path('M62 33 Q76 25 89 34', 'none', 'brow', stroke='#81909c', sw=5)
    art += group(head, 0, 0, cls='head')
    return art


def tortoise():
    art = ellipse(160, 250, 162, 18, '#6b7453', 'shadow')
    for x, cls in ((83, 'leg-a'), (211, 'leg-b')):
        art += group(path('M0 0 Q32 -13 45 21 L50 51 Q19 73 -13 48Z', '#b7bd7b'), x, 185, cls=f'leg {cls}')
    art += path('M57 171 L-6 189 L44 209Z', '#a1b37c', 'tail')
    art += path('M51 188 Q28 38 157 39 Q290 42 289 186 Q190 227 51 188Z', '#587d59', 'shell')
    art += path('M58 186 Q169 204 287 185', 'none', stroke='#d1ca8e', sw=12)
    art += path('M157 48 L115 94 L133 149 L188 158 L222 109 L192 58Z M115 94 L56 115 M133 149 L104 195 M188 158 L207 198 M222 109 L271 124 M157 48 L160 82', 'none', stroke='#a6bd7e', sw=6)
    head = path('M5 41 Q23 -12 67 2 Q112 6 111 43 Q109 79 63 84 L14 72Z', '#bdc987')
    head += ellipse(71, 24, 15, 17, '#fffae8', 'eye') + ellipse(77, 25, 6, 8, INK)
    head += ellipse(99, 43, 3, 3, INK) + ellipse(70, 53, 10, 5, '#dcad86')
    head += path('M79 63 Q94 73 103 60', 'none', stroke=INK, sw=3)
    art += group(head, 241, 126, cls='head')
    art += path('M293 210 Q274 246 289 258 L326 257', 'none', 'scarf', stroke='#d76e50', sw=16)
    return art


def rabbit():
    art = ellipse(147, 279, 145, 19, '#776d56', 'shadow')
    art += ellipse(65, 161, 30, 31, '#fff7e4', 'tail', INK)
    for x, cls in ((89, 'leg-a'), (189, 'leg-b')):
        art += group(path('M0 0 Q36 -19 47 13 L59 61 Q27 83 -6 58Z', '#faf0da'), x, 191, cls=f'leg {cls}')
    art += path('M66 172 Q77 107 152 104 Q227 118 239 187 Q237 232 174 241 Q109 250 67 218Z', '#f5e9d0', 'torso')
    art += path('M103 151 Q146 127 196 153 L195 215 Q149 239 109 211Z', '#d87652', 'vest')
    art += ellipse(151, 168, 5, 5, '#f7d577') + ellipse(153, 194, 5, 5, '#f7d577')
    art += group(path('M0 0 Q39 -10 40 28 Q17 50 -9 31Z', '#fff6df'), 192, 164, cls='arm')
    head = group(path('M0 0 Q-30 -83 2 -112 Q35 -107 29 -15Z', '#fff5df') + path('M8 -22 Q-7 -86 7 -96', 'none', stroke='#e7b1a0', sw=12), 139, 46, cls='ear ear-a')
    head += group(path('M0 0 Q9 -117 44 -116 Q68 -82 31 11Z', '#fff5df') + path('M20 -12 Q42 -83 41 -96', 'none', stroke='#e7b1a0', sw=12), 178, 45, cls='ear ear-b')
    head += path('M110 73 Q115 16 178 31 Q229 35 237 87 Q270 115 224 139 Q160 169 114 133Z', '#fff5df')
    head += ellipse(202, 74, 15, 19, '#fff', 'eye') + ellipse(208, 77, 7, 10, INK, 'pupil')
    head += path('M190 45 L216 48', 'none', 'brow', stroke=INK, sw=5)
    head += ellipse(239, 108, 8, 6, '#a9695c') + ellipse(204, 118, 15, 8, '#e7b1a0')
    head += path('M228 123 Q237 139 246 126 M235 102 L268 93 M238 112 L274 116', 'none', stroke=INK, sw=3)
    art += group(head, 0, 0, cls='head')
    return art


def elder(child=False):
    art = ellipse(95, 296, 90, 15, '#76664a', 'shadow')
    for x, cls in ((62, 'leg-a'), (120, 'leg-b')):
        art += group(path('M0 0 L-5 61 L-34 67 Q-45 82 14 79 L19 9Z', '#544b47'), x, 210, cls=f'leg {cls}')
    art += path('M45 117 Q82 92 137 119 L160 232 Q100 255 34 226Z', '#b56b4e' if not child else '#698b79', 'torso')
    art += path('M67 120 L87 154 L130 120 M84 150 L94 228', 'none', stroke='#ecc294', sw=5)
    art += group(path('M0 0 Q-32 14 -54 51 L-41 72 Q-7 43 11 25Z', '#d1a477') + ellipse(-50, 67, 15, 14, '#e5b88e'), 49, 134, cls='arm-back')
    arm = path('M0 0 Q24 10 35 43 L79 24 L94 45 Q41 83 15 58 L-13 24Z', '#b56b4e' if not child else '#698b79')
    arm += ellipse(87, 37, 15, 14, '#e5b88e')
    arm += path('M94 -72 L80 124', 'none', stroke='#947249', sw=12)
    arm += path('M49 -75 Q92 -101 153 -75 L151 -51 Q104 -62 57 -49Z', '#7b8d8e')
    art += group(arm, 134, 132, cls='arm-tool')
    head = path('M40 40 Q44 0 85 4 Q124 7 129 52 Q152 68 128 79 Q110 119 64 103 Q29 89 40 40Z', '#e5b88e')
    if not child:
        head += path('M41 36 Q19 8 52 -7 Q102 -23 127 15 L121 42 Q85 14 41 36Z', '#f2e8d5')
        head += path('M51 76 Q76 100 108 75 Q129 112 97 146 L80 127 L64 141 Q42 111 51 76Z', '#fff2d9', 'beard')
    else:
        head += path('M40 37 Q26 5 62 -4 Q108 -19 128 19 L119 47 Q75 9 40 37Z', '#493b36')
    head += path('M55 56 L67 54 M99 55 L111 57', 'none', 'eye', stroke=INK, sw=5)
    head += ellipse(66, 77, 13, 6, '#cb9275') + path('M79 57 L76 77 L88 79', 'none', stroke=INK, sw=3)
    art += group(head, 12, 0, cls='head')
    return art


def pot(prefix, water=178, stones=False):
    outline = 'M74 66 L69 144 Q11 183 23 291 Q33 342 82 351 H192 Q240 341 250 291 Q265 183 207 144 L202 66Z'
    art = ellipse(139, 375, 159, 23, '#82735b')
    art += path(outline, '#c98661')
    art += path('M63 188 Q42 264 75 316', 'none', stroke='#ecc39a', sw=13)
    art += path('M220 187 Q244 277 214 321', 'none', stroke='#a85f47', sw=10)
    art += f'<defs><clipPath id="{prefix}-glass">{path(outline, "#fff", stroke="none")}</clipPath></defs>'
    art += f'<g clip-path="url(#{prefix}-glass)">'
    art += path('M87 66 V151 Q43 204 56 298 Q63 319 86 324 H189 Q211 319 217 296 Q231 204 192 151 V66Z', '#f2d9b0', stroke='#ad7154', sw=3)
    art += group(f'<rect x="52" y="0" width="173" height="300" fill="#73b7b2"/>' + ellipse(137, 0, 86, 12, '#c4e6d6', stroke='#3f8783', sw=3), 0, water, cls='water')
    for i in range(4 if stones else 0):
        art += group(ellipse(0, 0, 23, 15, '#9b9984', 'settled-stone', INK, 3), 82 + i * 36, 309 - (i % 2) * 15, cls=f'settled settled-{i}')
    art += '</g>'
    art += ellipse(138, 65, 77, 17, '#9b6046', stroke=INK, sw=5) + ellipse(138, 60, 66, 10, '#efd1a4', stroke='#be805b', sw=5)
    art += path('M83 141 H193', 'none', stroke='#dfad78', sw=9)
    return art


def bubble(text, x, y, width=350):
    art = path(f'M30 0 H{width-30} Q{width} 0 {width} 30 V90 Q{width} 120 {width-30} 120 H90 L45 155 L54 120 H30 Q0 120 0 90 V30 Q0 0 30 0Z', '#fff8e8', stroke='#c29a76', sw=3)
    art += f'<text x="{width/2}" y="73" text-anchor="middle" fill="{INK}" font-size="38" font-weight="700">{escape(text)}</text>'
    return group(art, x, y, cls='bubble')


def sparkles(x, y):
    art = ''
    for i, (dx, dy) in enumerate(((0, 0), (110, 20), (-90, 55), (75, -80), (-85, -65))):
        art += group(path('M0 -20 L6 -6 L20 0 L6 6 L0 20 L-6 6 L-20 0 L-6 -6Z', '#f2c465', stroke='none'), dx, dy, cls=f'spark spark-{i}')
    return group(art, x, y, cls='sparkles')


def stone(x, y, cls='stone'):
    return group(path('M-22 2 Q-21 -16 1 -18 Q23 -20 27 3 Q19 22 -3 18 Q-24 18 -22 2Z', '#9b9984', stroke=INK, sw=3), x, y, cls=cls)


def house(x, y, scale=1):
    art = path('M20 86 H194 V237 H20Z', '#efcf9d', stroke='#946d4f', sw=4)
    art += path('M-10 91 L98 -4 L226 91Z', '#976448', stroke='#78523f', sw=4)
    art += path('M79 237 V136 H139 V237', '#715a46', stroke='#946d4f', sw=4)
    art += path('M43 115 H65 V151 H43Z M159 115 H181 V151 H159Z', '#698675', stroke='#946d4f', sw=4)
    art += path('M10 252 H203', 'none', stroke='#ba9a75', sw=8)
    return group(art, x, y, scale, 'house')


def mountains():
    left = path('M-80 805 Q-5 581 175 180 Q244 66 320 112 Q424 352 535 795Z', '#a57558', stroke='#805e47', sw=7)
    left += path('M172 195 L244 257 L289 169 L345 253 L321 111 Q244 66 172 195Z', '#d9b68b', stroke='none')
    left += path('M244 259 L193 423 L257 507 L213 686 M348 332 L383 530 L322 645', 'none', stroke='#bd916d', sw=10)
    left += group(foliage(0, 0, .4), 330, 600)
    right = path('M-30 806 Q82 500 167 308 L270 114 Q325 42 384 95 Q488 365 670 803Z', '#b78a60', stroke='#805e47', sw=7)
    right += path('M225 194 L285 241 L333 173 L391 227 L384 95 Q325 42 270 114Z', '#e0c395', stroke='none')
    right += path('M280 244 L218 429 L289 507 L240 698 M413 316 L472 520 L419 622', 'none', stroke='#ccaa7c', sw=11)
    return group(left, 470, 35, cls='mountain-left') + group(right, 960, 35, cls='mountain-right')


def race_track():
    art = path('M-30 861 Q960 712 1950 836', 'none', stroke='#ce8c6b', sw=172)
    art += path('M-30 799 Q960 662 1950 776 M-30 922 Q960 783 1950 897', 'none', stroke='#f7e1b4', sw=5)
    art += path('M0 859 Q960 708 1920 835', 'none', stroke='#edcaa0', sw=4)
    return art


def finish():
    art = path('M0 0 V550 M350 0 V550', 'none', stroke='#815e45', sw=16)
    art += path('M-20 0 H370 V110 H-20Z', '#f9e5bb', stroke='#815e45', sw=5)
    for row in range(2):
        for col in range(8):
            if (row + col) % 2 == 0:
                art += f'<rect x="{col*48-20}" y="{row*55}" width="48" height="55" fill="#85684e"/>'
    art += path('M0 363 Q175 393 350 363', 'none', 'ribbon', stroke='#d96950', sw=19)
    return group(art, 1320, 340, cls='finish')


def spectators():
    art = ''
    for i, x in enumerate((800, 950, 1100, 1240)):
        creature = ellipse(0, 0, 40, 45, '#a98160' if i % 2 == 0 else '#d5ad7a', stroke=INK, sw=3)
        creature += ellipse(-24, -40, 15, 19, '#a98160', stroke=INK, sw=3) + ellipse(24, -40, 15, 19, '#a98160', stroke=INK, sw=3)
        creature += ellipse(-13, -7, 4, 5, INK) + ellipse(13, -7, 4, 5, INK) + ellipse(0, 10, 13, 9, '#f3dfb7')
        creature += path('M-25 39 L-41 84 L39 84 L25 39Z', '#b8654c' if i % 2 == 0 else '#728e76', sw=3)
        creature += path('M-26 48 L-55 15 M26 48 L55 15', 'none', stroke='#b28e69', sw=12)
        art += group(creature, x, 694, .85, 'spectator')
    return art


def scene(project, index, start, end, art, title, subtitle, label, extra=''):
    svg = f'<svg class="world" data-layout-allow-overflow viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg" aria-label="{escape(label)}" role="img">{art}</svg>'
    title_html = f'<h1>{escape(title)}</h1>' if title else ''
    subtitle_html = f'<p class="subtitle">{escape(subtitle)}</p>' if subtitle else ''
    return f'''<section id="s{index}" class="scene clip" data-start="{start}" data-duration="{end-start:.2f}" data-track-index="{index}">
      <figure class="shot">{svg}</figure>
      <p class="chapter"><span class="chapter-number">0{index}</span><span>{escape(label)}</span></p>
      <header class="copy">{title_html}{subtitle_html}</header>{extra}
    </section>'''


def crow_scenes():
    a = scenery() + group(pot('opening', 258), 985, 500, .85, 'pot')
    a += ellipse(1430, 835, 150, 22, '#918769', 'landing-shadow')
    a += group(crow(), 1260, 565, 1.05, 'hero bird') + foreground()
    b = scenery() + group(pot('problem', 258), 810, 358, 1.38, 'pot')
    b += ellipse(1430, 825, 155, 24, '#918769', 'landing-shadow')
    b += group(crow(), 1215, 495, 1.25, 'hero bird') + bubble('就差一点点……', 1210, 240, 400)
    for i in range(5):
        b += stone(1410 + i * 49, 820 - (i % 2) * 20, 'ground-stone')
    b += foreground()
    c = scenery() + group(pot('solution', 258, stones=True), 800, 390, 1.28, 'pot')
    c += ellipse(1330, 835, 170, 23, '#918769', 'landing-shadow')
    c += group(crow(), 1155, 355, 1.4, 'hero bird') + bubble('有办法了！', 1220, 205, 350)
    for i in range(4):
        c += stone(1270 + i * 48, 785 + (i % 2) * 18, f'falling-stone stone-{i}')
    for i in range(5):
        c += group(path('M0 0 Q-6 -15 0 -24 Q6 -15 0 0Z', '#6aa6a5', stroke='none'), 975 + i * 22, 521, cls=f'splash splash-{i}')
    c += group(ellipse(0, 0, 63, 9, 'none', 'ripple', '#77b6af', 5), 977, 512)
    c += sparkles(1140, 465) + foreground()
    d = scenery() + group(pot('ending', 99, stones=True), 1090, 500, .9, 'pot')
    d += ellipse(1560, 827, 135, 20, '#918769', 'landing-shadow')
    d += group(crow(), 1390, 575, .95, 'hero bird') + sparkles(1520, 570) + foreground()
    return [scene('crow-water', 1, 0, 2, a, '乌鸦喝水', '一只口渴的小乌鸦，发现了一个陶罐。', '中国寓言 · 聪明的小办法'),
            scene('crow-water', 2, 2, 6.2, b, '', '', '遇到难题 · 水太浅了'),
            scene('crow-water', 3, 6.2, 13, c, '', '', '试试这个 · 小石子的大作用'),
            scene('crow-water', 4, 13, 18, d, '肯动脑筋\n办法总比困难多', '小小的石子，也能一步一步改变眼前的难题。', '故事里的智慧', '<aside class="seal">智</aside>')]


def turtle_scenes():
    a = scenery() + race_track() + group(tortoise(), 980, 554, .9, 'hero tortoise') + group(rabbit(), 1330, 570, .9, 'hero rabbit')
    a += group(path('M0 0 V280', 'none', stroke='#886c4f', sw=12) + path('M0 0 H140 L115 53 L140 105 H0Z', '#d76e50'), 830, 575, cls='flag') + foreground()
    b = scenery() + race_track() + group(rabbit(), 1030, 505, 1.12, 'hero rabbit') + group(tortoise(), 125, 655, .66, 'hero tortoise')
    b += group(tree(0, 0, 1.3, '#537861'), 1340, 200, cls='shade-tree')
    b += bubble('先睡一觉吧～', 1170, 315, 350)
    b += '<g class="sleep"><text x="1560" y="300" font-size="68" fill="#493b36">Z</text><text x="1630" y="245" font-size="45" fill="#493b36">z</text><text x="1680" y="198" font-size="30" fill="#493b36">z</text></g>'
    b += foreground()
    c = scenery() + race_track() + finish() + group(tortoise(), 325, 557, 1.04, 'hero tortoise') + group(rabbit(), 90, 640, .77, 'hero rabbit')
    c += bubble('一步一步，坚持向前。', 380, 340, 520) + foreground()
    d = scenery() + race_track() + spectators() + finish()
    d += group(tortoise(), 1000, 592, .95, 'hero tortoise') + group(rabbit(), 620, 650, .75, 'hero rabbit')
    d += sparkles(1310, 635) + foreground()
    return [scene('turtle-rabbit', 1, 0, 3.8, a, '龟兔赛跑', '跑得快，还是走得稳？森林里的比赛开始了。', '森林寓言 · 一场意外的比赛'),
            scene('turtle-rabbit', 2, 3.8, 10.2, b, '', '', '遥遥领先 · 兔子的午睡'),
            scene('turtle-rabbit', 3, 10.2, 17.5, c, '', '', '从不停步 · 乌龟的坚持'),
            scene('turtle-rabbit', 4, 17.5, 23, d, '持之以恒\n一步一步，也能到达', '骄兵必败。坚持到最后的人，才是真正的赢家。', '故事里的智慧')]


def foolish_scenes():
    a = scenery('mountain') + house(190, 540, .9) + mountains() + group(elder(), 260, 625, .72, 'hero elder')
    a += group(path('M0 0 H120 M12 -30 H105 M9 35 H111', 'none', stroke='#b89d72', sw=8), 395, 868, cls='blocked-road') + foreground()
    b = scenery('mountain') + mountains() + group(elder(), 760, 465, 1.25, 'hero elder')
    for i in range(7):
        b += stone(1130 + i * 44, 829 - (i % 3) * 16, f'chip chip-{i}')
    b += bubble('今天，也要再挖一点。', 195, 335, 500) + foreground()
    c = scenery('mountain') + mountains() + house(200, 545, .9)
    for i in range(4):
        c += group(elder(child=i > 0), 525 + i * 250, 600 + (i % 2) * 40, .78 - i * .055, f'worker worker-{i}')
    for i in range(8):
        c += stone(900 + i * 49, 884 - (i % 3) * 12, 'rock-pile')
    c += foreground()
    d = scenery('mountain')
    d += path('M740 1080 Q670 842 980 634 Q1080 569 1140 500', 'none', 'open-road', stroke='#f7e6c0', sw=150)
    d += house(155, 545, .8) + mountains() + group(elder(), 560, 650, .75, 'hero elder')
    d += group(elder(child=True), 765, 725, .48, 'hero child') + sparkles(960, 535) + foreground()
    return [scene('foolish-move-mountain', 1, 0, 7.8, a, '愚公移山', '家门前的两座大山，挡住了通往远方的路。', '中国寓言 · 山外有远方'),
            scene('foolish-move-mountain', 2, 7.8, 11.1, b, '', '', '第一锄 · 从今天开始'),
            scene('foolish-move-mountain', 3, 11.1, 18.1, c, '', '', '一代又一代 · 把坚持传下去'),
            scene('foolish-move-mountain', 4, 18.1, 25, d, '只要坚持\n终会打开一条路', '今天的一小步，会成为明天走向远方的路。', '故事里的智慧')]


CSS = '''
@font-face {font-family: Story; src: url("assets/story.woff2") format("woff2"); font-weight: 700 900; font-display: block;}
@font-face {font-family: Story; src: url("assets/story-regular.woff2") format("woff2"); font-weight: 100 600; font-display: block;}
* {box-sizing: border-box} html, body {margin:0;width:100%;height:100%;overflow:hidden;background:#f4e5cb}
body {font-family:Story,serif;color:#493b36} #book {width:100%;height:100%;position:relative;overflow:hidden}
.scene,.shot {position:absolute;inset:0;overflow:hidden;margin:0} .scene {background:#f4e5cb}
.world {display:block;width:100%;height:100%;overflow:visible;font-family:Story,serif}
.chapter {position:absolute;left:106px;top:74px;display:flex;align-items:center;gap:21px;font-size:25px;letter-spacing:3px;color:#635744;margin:0}
.chapter-number {font-size:22px;border:2px solid #a68b6d;width:48px;height:48px;border-radius:50%;display:grid;place-items:center}
.copy {position:absolute;left:106px;top:164px;max-width:1020px;pointer-events:none}
h1 {margin:0;font-size:112px;line-height:1.24;letter-spacing:6px;font-weight:900;white-space:pre-line;color:#493b36}
.subtitle {margin:24px 0 0;font-size:32px;line-height:1.7;max-width:780px;color:#493b36}
#s4 .copy {top:169px;max-width:1320px} #s4 h1 {font-size:87px;line-height:1.35} #s4 .subtitle {font-size:30px;max-width:1020px}
#s4 .chapter {color:#635744} .seal {position:absolute;left:107px;top:540px;width:93px;height:93px;border:4px solid #b85f45;border-radius:16px;color:#a7533d;background:#fff4db;display:grid;place-items:center;font-size:58px}
.caption {position:absolute;bottom:65px;left:50%;width:1580px;margin-left:-790px;text-align:center;font-size:36px;line-height:1.4;color:#493b36;pointer-events:none}
.caption span {display:inline-block;padding:13px 34px;background:#fff4db;border-radius:15px;box-shadow:0 3px 0 #d7b997}
.paper {position:absolute;inset:0;pointer-events:none;z-index:60;opacity:.17;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='grain'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23grain)' opacity='.2'/%3E%3C/svg%3E");mix-blend-mode:multiply}
.frame {position:absolute;inset:24px;border:2px solid #bca380;opacity:.5;pointer-events:none;z-index:70;border-radius:5px}
'''


def subset_fonts(regular, bold):
    """Optional font regeneration; default HTML builds need no third-party code."""
    from fontTools import subset
    import shutil
    import tempfile
    text = Path(__file__).read_text() + (ROOT / 'narration.json').read_text()
    with tempfile.TemporaryDirectory() as directory:
        for source, name in ((regular, 'story-regular.woff2'), (bold, 'story.woff2')):
            options = subset.Options()
            options.flavor = 'woff2'
            font = subset.load_font(str(source), options)
            worker = subset.Subsetter(options=options)
            worker.populate(text=text)
            worker.subset(font)
            output = Path(directory) / name
            subset.save_font(font, str(output), options)
            for project in ('crow-water', 'turtle-rabbit', 'foolish-move-mountain'):
                shutil.copyfile(output, ROOT / project / 'assets' / name)


def build():
    import json
    narration = json.loads((ROOT / 'narration.json').read_text())
    projects = [('crow-water', 18, crow_scenes()), ('turtle-rabbit', 23, turtle_scenes()), ('foolish-move-mountain', 25, foolish_scenes())]
    js = (ROOT / 'storybook' / 'motion.js').read_text()
    story_names = [name for name, _, _ in projects]
    boundaries = [js.index(f'if (STORY_ID === "{name}") {{') for name in story_names]
    script_end = js.index('window.__timelines[STORY_ID] = tl;')
    common = js[:boundaries[0]]
    for name, duration, scenes in projects:
        # Keep only this story's choreography in its standalone composition.
        index = story_names.index(name)
        common_script = common
        if name != 'foolish-move-mountain':
            dig_start = common_script.index('function dig(')
            dig_end = common_script.index('\nfor (const section', dig_start)
            common_script = common_script[:dig_start] + common_script[dig_end:]
        story_end = boundaries[index + 1] if index + 1 < len(boundaries) else script_end
        script = common_script + js[boundaries[index]:story_end]
        script += f'window.__timelines[{json.dumps(name)}] = tl;'
        captions = ''
        for i, cue in enumerate(narration[name]):
            end = narration[name][i+1]['start'] if i+1 < len(narration[name]) else duration - .3
            captions += f'<div id="caption-{i}" class="caption clip" data-start="{cue["start"]}" data-duration="{end-cue["start"]:.2f}" data-track-index="10"><span>{escape(cue["text"])}</span></div>'
        html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><title>{escape(narration[name][0]['text'])} · 动态绘本</title>
<script src="assets/gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="book" data-composition-id="{name}" data-start="0" data-width="1920" data-height="1080" data-duration="{duration}">
{''.join(scenes)}{captions}<div class="paper" data-layout-ignore></div><div class="frame" data-layout-ignore></div></div>
<script>const STORY_ID = {json.dumps(name)};\n{script}</script></body></html>\n'''
        (ROOT / name / 'index.html').write_text(html, encoding='utf-8')
        proof = {
            'duration': duration,
            'assertions': [
                {'kind': 'appearsBy', 'selector': '#s1 h1', 'bySec': 1.2},
                {'kind': 'appearsBy', 'selector': '#s4 h1',
                 'bySec': 22 if name == 'foolish-move-mountain' else duration - 3},
                *({'kind': 'staysInFrame', 'selector': f'#caption-{i}'}
                  for i in range(len(narration[name]))),
            ],
        }
        (ROOT / name / 'index.motion.json').write_text(json.dumps(proof, indent=2) + '\n')
        print(f'Built {name}: {len(html):,} bytes')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-regular', type=Path)
    parser.add_argument('--font-bold', type=Path)
    args = parser.parse_args()
    if bool(args.font_regular) != bool(args.font_bold):
        parser.error('Provide both --font-regular and --font-bold')
    if args.font_regular:
        subset_fonts(args.font_regular, args.font_bold)
    build()
