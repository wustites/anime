"""Illustrations for each causal beat of the complete fables."""


def render(b, project, shot):
    beat = shot['beat']
    g, p, e = b.group, b.path, b.ellipse
    art = b.scenery('mountain' if project == 'foolish-move-mountain' else 'meadow')
    if project == 'crow-water':
        if beat in ('thirst', 'search'):
            if beat == 'search':
                well = p('M0 45 V155 Q120 203 240 155 V45Z', '#af997c')
                well += e(120, 45, 120, 43, '#564b40', stroke=b.INK)
                well += p('M-5 40 V-200 H245 V40 M-35 -200 H280', 'none', stroke='#91704e', sw=18)
                well += p('M120 -200 V-80 M87 -80 H153 L145 -25 H96Z', '#bb916b', stroke='#806045', sw=6)
                well += p('M0 95 H240 M60 63 V95 M175 95 V160', 'none', stroke='#dac6a3', sw=5)
                art += g(well, 720, 660, cls='dry-well')
                art += b.bubble('这里也没有水……', 1120, 360, 420)
            art += g(b.crow(), 1190, 420 if beat == 'thirst' else 545, 1.1, 'hero bird')
            art += p('M850 895 L885 867 L912 892 L946 873 M1100 897 L1135 879 L1175 902', 'none', stroke='#b19876', sw=5)
        elif beat == 'moral':
            art += g(b.pot('ending', 99, stones=True), 1090, 500, .9, 'pot')
            art += g(b.crow(), 1390, 575, .95, 'hero bird') + b.sparkles(1520, 570)
        else:
            water = 100 if beat == 'drink' else 220 if beat == 'repeat' else 258
            art += g(b.pot(shot['id'], water, stones=beat in ('test', 'repeat', 'drink')), 800, 390, 1.28, 'pot')
            art += e(1330, 835, 170, 23, '#918769', 'landing-shadow')
            art += g(b.crow(), 1155, 355 if beat in ('test', 'repeat', 'drink') else 495, 1.4, 'hero bird')
            for i in range(4):
                art += b.stone(1270 + i * 48, 785 + (i % 2) * 18, f'falling-stone stone-{i}')
            if beat in ('test', 'repeat', 'drink'):
                for i in range(5):
                    art += g(p('M0 0 Q-6 -15 0 -24 Q6 -15 0 0Z', '#6aa6a5', stroke='none'), 975+i*22, 521, cls=f'splash splash-{i}')
                art += g(e(0, 0, 63, 9, 'none', 'ripple', '#77b6af', 5), 977, 512)
            words = {'discover':'真的有水！', 'reach':'还是够不到……', 'push':'怎么这么重？', 'idea':'试试小石子！', 'test':'水面升高了！', 'repeat':'再来一颗！'}
            if beat in words:
                art += b.bubble(words[beat], 1240, 230, 390)
            if beat == 'idea':
                bulb = e(0, 0, 35, 42, '#f5cd68', stroke='#ad8250') + p('M-14 38 H14 M-12 49 H12 M0 -64 V-82 M-54 -30 L-70 -39 M54 -30 L70 -39', 'none', stroke='#ad8250', sw=6)
                art += g(bulb, 1340, 430, cls='idea-light')
    elif project == 'turtle-rabbit':
        art += b.race_track()
        if beat in ('rivalry', 'challenge', 'start'):
            art += g(b.tortoise(), 785, 590, .85, 'hero tortoise') + g(b.rabbit(), 1210, 535, 1, 'hero rabbit')
            if beat == 'rivalry': art += b.bubble('你走得太慢啦！', 1210, 280, 410)
            if beat == 'challenge': art += b.bubble('我们比一比吧！', 680, 340, 410)
            if beat == 'start':
                art += g(p('M0 0 V280', 'none', stroke='#886c4f', sw=12) + p('M0 0 H140 L115 53 L140 105 H0Z', '#d76e50'), 710, 540, cls='flag')
                art += g(b.tree(0, 0, .65), 1590, 520, cls='destination-tree')
                art += g(p('M0 0 H160 V65 H0Z', '#fff4db', sw=3) + '<text x="80" y="44" text-anchor="middle" font-size="30" fill="#493b36">终点 →</text>', 1560, 770)
        elif beat == 'lead':
            art += g(b.rabbit(), 830, 525, 1.08, 'hero rabbit') + g(b.tortoise(), 140, 662, .48, 'hero tortoise')
            art += b.bubble('乌龟还那么远！', 1090, 290, 410)
        elif beat in ('sleep', 'overtake', 'wake'):
            art += g(b.tree(0, 0, 1.3, '#537861'), 1260, 200, cls='shade-tree')
            art += g(b.rabbit(), 1120, 535, 1.04, 'hero rabbit')
            if beat == 'overtake': art += g(b.tortoise(), 480, 606, .94, 'hero tortoise')
            if beat == 'wake': art += g(b.tortoise(), 1580, 667, .43, 'hero tortoise')
            art += '<g class="sleep"><text x="1490" y="350" font-size="68" fill="#493b36">Z</text><text x="1570" y="290" font-size="45" fill="#493b36">z</text></g>'
            art += b.bubble('先睡一觉吧～' if beat == 'sleep' else '糟糕，快追！' if beat == 'wake' else '一步一步向前。', 730, 300, 450)
        elif beat == 'steady':
            art += g(b.tortoise(), 665, 530, 1.28, 'hero tortoise')
            art += b.bubble('我会坚持走到终点。', 920, 300, 520)
            for i in range(6): art += e(440+i*55, 850, 12, 5, '#ac8768', 'footprint')
        elif beat == 'finish':
            art += b.finish() + b.spectators()
            art += g(b.tortoise(), 880, 592, .95, 'hero tortoise') + g(b.rabbit(), 120, 625, .85, 'hero rabbit')
            art += b.sparkles(1390, 540)
        else:
            art += b.finish() + g(b.tortoise(), 1090, 592, .95, 'hero tortoise') + g(b.rabbit(), 720, 650, .75, 'hero rabbit')
            art += b.sparkles(1370, 630)
    else:
        if beat == 'lift': art += p('M740 1080 Q670 842 980 634 Q1080 569 1140 500', 'none', 'open-road', stroke='#f7e6c0', sw=150)
        if beat not in ('carry', 'moral'): art += b.mountains()
        if beat in ('blocked', 'plan', 'question', 'moral'): art += b.house(190, 540, .9)
        def person(x, y, scale, cls, child=False, tool=False):
            return g(b.elder(child=child, tool=tool), x, y, scale, cls)
        if beat == 'blocked':
            art += person(265, 625, .72, 'hero elder')
            art += g(p('M0 0 H120 M12 -30 H105 M9 35 H111', 'none', stroke='#b89d72', sw=8), 395, 868, cls='blocked-road')
        elif beat in ('plan', 'question'):
            art += person(510, 585, .95, 'hero elder')
            for i in range(3): art += person(900+i*230, 650, .7 if i<2 else .5, f'family family-{i}', child=True)
            art += b.bubble('一起把山搬走！' if beat == 'plan' else '把土石运到渤海边。', 480, 330, 550)
            if beat == 'question': art += basket(b, 1290, 810)
        elif beat in ('dig', 'generations', 'seasons'):
            for i in range(3): art += person(500+i*370, 555+i%2*40, 1.02-i*.13, f'worker worker-{i}', child=i>0, tool=True)
            for i in range(7): art += b.stone(900+i*65, 863-i%3*15, f'chip chip-{i}')
            if beat == 'generations': art += b.bubble('子子孙孙，一代接一代。', 175, 285, 600)
            if beat == 'seasons':
                art += '<g class="winter">' + ''.join(e(200+i*125, 210+(i%4)*110, 7, 7, '#fff7e6', 'snow') for i in range(13)) + '</g>'
                art += '<g class="autumn">' + ''.join(g(p('M0 0 Q35 -30 40 10 Q18 33 0 0Z', '#d58b51', stroke='none'), 290+i*165, 270+i%3*95, cls='leaf') for i in range(9)) + '</g>'
        elif beat == 'carry':
            art += p('M0 890 Q800 660 1920 815', 'none', stroke='#efdaad', sw=115)
            art += p('M1350 660 Q1540 535 1920 665 V795 Q1540 695 1350 760Z', '#8abbb4', stroke='none')
            for i in range(3):
                art += person(410+i*360, 575+i%2*50, .9-i*.1, f'carrier carrier-{i}', child=i>0)
                art += basket(b, 565+i*350, 775+i%2*40, f'basket basket-{i}')
            art += b.bubble('一筐一筐，运到海边。', 1010, 350, 530)
        elif beat in ('doubt', 'answer'):
            art += person(650, 535, 1.1, 'hero elder')
            sage = b.elder(tool=False).replace('#b56b4e', '#668b95').replace('#f2e8d5', '#aeb8b2').replace('#fff2d9', '#ced5cf')
            art += g(sage, 1280, 565, 1, 'sage')
            art += b.bubble('这么大的山，搬得完吗？' if beat == 'doubt' else '我还有儿子，还有孙子。', 850 if beat=='doubt' else 330, 280, 600)
        elif beat in ('divine', 'lift'):
            art += g(strongman(b, '#678d91'), 700, 565, 1.1, 'god god-left')
            art += g(strongman(b, '#b87659'), 1190, 565, 1.1, 'god god-right')
            art += person(255, 710, .53, 'hero elder') + b.sparkles(1130, 310)
        else:
            art += p('M740 1080 Q670 842 980 634 Q1080 569 1140 500', 'none', 'open-road', stroke='#f7e6c0', sw=150)
            art += person(780, 650, .75, 'hero elder') + person(1010, 725, .48, 'hero child', child=True)
            art += b.sparkles(1260, 560)
    return art + b.foreground()


def basket(b, x, y, cls='basket'):
    art = b.path('M-65 0 H65 L49 94 H-46Z', '#b99363', stroke='#7e6045', sw=4)
    art += b.path('M-59 20 H59 M-54 42 H54 M-49 65 H49 M-30 0 V88 M0 0 V90 M30 0 V90', 'none', stroke='#e0bd83', sw=5)
    art += b.path('M-55 -6 Q-15 -52 12 -25 Q55 -53 59 -6Z', '#99957f', sw=3)
    return b.group(art, x, y, .75, cls)


def strongman(b, color):
    art = b.ellipse(110, 270, 180, 24, '#fff1d4', 'divine-cloud')
    art += b.path('M30 155 L16 257 H87 L98 169 M133 168 L148 257 H207 L188 150', color)
    art += b.path('M26 61 Q110 24 195 65 L190 168 Q111 201 28 168Z', color, 'torso')
    art += b.path('M30 80 L-45 48 L-62 -84 L-34 -95 L-8 9 L55 28 M181 77 L252 50 L272 -78 L243 -93 L220 8 L164 28', '#deb285', 'arms')
    art += b.path('M31 139 H190', 'none', stroke='#efcf82', sw=18)
    art += b.ellipse(112, 7, 46, 53, '#e5b88e', 'head', b.INK)
    art += b.path('M66 -12 Q59 -70 111 -55 Q173 -69 161 -10 L145 -28 H82Z', '#493b36')
    art += b.ellipse(112, -72, 20, 16, '#493b36')
    art += b.path('M85 0 H97 M127 0 H139 M96 28 Q113 40 132 26', 'none', stroke=b.INK, sw=5)
    art += b.ellipse(111, -13, 77, 80, 'none', 'halo', '#ecc76a', 5)
    return art
