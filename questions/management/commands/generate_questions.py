# coding=utf-8
from collections import defaultdict
import json
import random
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        self.skills = self.skills()
        json.dump(self.skills, open("questions/migrations/skills.json", "w"), indent=4)
        data = self.questions()
        json.dump(data["questions"], open("questions/migrations/questions.json", "w"), indent=4)
        json.dump(data["simulators"], open("questions/migrations/simulators.json", "w"), indent=4)

    def skills(self):
        skills = []
        skill_level = {}

        def S(name, parent, note=None):
            level = 1 if parent is None else skill_level[parent["name"]] + 1
            skill_level[name] = level
            note = name if note is None else note
            s = {
                "name": name,
                "parent": None if parent is None else parent["name"],
                "note": note,
            }
            skills.append(s)
            return s

        # Main math skill:
        # ----------------
        math = S(name='math', parent=None, note='Všechno')

        # Numbers:
        # --------
        numbers = S(name='numbers', parent=math, note='Počítání')
        num10 = S(name='numbers <= 10', parent=numbers, note='Počítání do 10')
        num20 = S(name='numbers <= 20', parent=numbers, note='Počítání do 20')
        for n in range(1, 21):
            S(name=str(n), parent=num10 if n <= 10 else num20)

        # Addition:
        # ---------
        addition = S(name='addition', parent=math, note=u'Sčítání')
        a1 = S(name='addition <= 10', parent=addition, note=u'Sčítání do 10')
        a2 = S(name='addition <= 20', parent=addition, note=u'Sčítání do 20')
        S(name='addition <= 100', parent=addition, note=u'Sčítání do 100')
        for a in range(20):
            for b in range(a, 21):
                if a + b <= 20:
                    S(name='%s+%s' % (a, b), parent=a1 if a + b <= 10 else a2)

        # Subtraction:
        # ------------
        subtr = S(name='subtraction', parent=math, note=u'Odčítání')
        s1 = S(name='subtraction <= 10', parent=subtr, note=u'Odčítání do 10')
        s2 = S(name='subtraction <= 20', parent=subtr, note=u'Odčítání do 20')
        for a in range(1, 11):
            for b in range(1, a + 1):
                S(name='%s-%s' % (a, b), parent=s1)

        # Multiplication:
        # ---------------
        m0 = S(name='multiplication', parent=math, note=u'Násobení')
        m1 = S(name='multiplication1', parent=m0, note=u'Malá násobilka')
        for b in range(1, 11):
            for a in range(1, b + 1):
                S(name='%sx%s' % (a, b), parent=m1, note='%s&times;%s' % (a, b))
        m2 = S(name='multiplication2', parent=m0, note=u'Velká násobilka')
        for a in range(1, 11):
            for b in range(11, 21):
                S(name='%sx%s' % (a, b), parent=m2, note='%s&times;%s' % (a, b))

        # Division:
        # ---------
        d0 = S(name='division', parent=math, note=u'Dělení')
        d1 = S(name='division1', parent=d0, note=u'Dělení malých čísel')
        for a in range(1, 11):
            for b in range(1, 11):
                total = a * b
                S(name='%s/%s' % (total, b), parent=d1)

        return skills


    def questions(self):
        json_data = {
            "simulators": [],
            "questions": [],
        }

        KB_FULL = "full"
        KB_10 = range(1, 11)
        ids = defaultdict(lambda: 0)

        def get_skill(name):
            return self.skills[name]

        def Q(skill, player, data, type='c', value=None, active=True):
            data = json.dumps(data)
            q = {
                "type": type,
                "skill": skill,
                "player": player,
                "data": data,
                "value": value,
                "active": active,
                "id": "{}-{}-{}".format(skill, player, ids["{}-{}".format(skill, player)]),
            }
            ids["{}-{}".format(skill, player)] += 1
            json_data["questions"].append(q)
            return q

        def Sim(name, note):
            sim = {"name": name, "note": note}
            json_data["simulators"].append(sim)
            return name

        # Simulators:
        # -----------
        free_answer = Sim('free_answer', 'Volná odpověd')
        counting = Sim('counting', 'Počítání předmětů')
        selecting = Sim('selecting', 'Výběr správného počtu předmětů')
        numberline = Sim('numberline', 'Výběr odpovědi na číselné ose')
        fillin = Sim('fillin', 'Doplnění čísla')
        field = Sim('field', 'Počítání předmětů v mřížce')
        pairing = Sim('pairing', 'Matematické pexeso')

        # Numbers:
        # --------
        for n in range(1, 21):
            skill = str(n)
            # for numbers up to 7 ... choice up to 10
            # for numbers up to 17 ... choice up to 20
            # for numbers above .... choice up to a 100
            nr = 1 if n <= 7 else 2
            # number -> select objects
            Q(skill, selecting, {"question": n, "answer": n,
                                 "nrows": nr, "ncols": 10}, value=skill)
            # objects -> number
            Q(skill, counting, {"question": [n], "answer": str(n), "with_text": False,
                                "kb": KB_10 if n <= 10 else KB_FULL}, value=skill)
        for n in range(1, 21):
            # number -> number-line
            Q(str(n), numberline, {"question": str(n), "answer": n}, value=str(n))

        # Addition:
        # ---------
        for a in range(1, 21):
            for b in range(1, 21):
                total = a + b
                if total <= 20:
                    x, y = (a, b) if a <= b else (b, a)
                    skill = '%s+%s' % (x, y)
                    kb = KB_10 if total <= 10 else KB_FULL
                    Q(skill, free_answer,
                      {"question": "%s + %s" % (a, b), "answer": str(total),
                       "kb": kb}, value=skill)
                    Q(skill, counting,
                      {"question": [a, "+", b], "answer": str(total), "kb": kb, "with_text": True}, value=skill,)
        skill = 'addition <= 100'
        random.seed(150 - 2)
        X = set([])
        while len(X) < 100:
            a, b = random.randint(1, 100), random.randint(1, 100)
            if (a > 20 or b > 20) and a + b <= 100:
                X.add((a, b))
        for a, b in X:
            Q(skill, free_answer,
              {"question": "%s + %s" % (a, b), "answer": str(a + b),
               "kb": KB_FULL})

        X = set([])
        for a in range(1, 11):
            for b in range(1, 11):
                X.add((a, b))
        while len(X) < 150:
            a, b = random.randint(1, 50), random.randint(1, 50)
            X.add((a, b))
        for a, b in X:
            if a <= 20 and a + b <= 20:
                x, y = (a, b) if a <= b else (b, a)
                skill = '%s+%s' % (x, y)
                value = skill
            else:
                skill = "addition <= 100"
                value = None
            Q(skill, counting,
              {"question": [a, "+", b], "answer": str(a + b), "with_text": True,
               "kb": KB_FULL if a + b > 10 else KB_10}, value=value)
        # end random.seed(150 - 2)

        # pairings:
        random.seed(8)
        opts = range(2, 11)

        def shuffle(pairs):
            l = [(e, i) for i, p in enumerate(pairs) for e in p]
            random.shuffle(l)
            a = len(l) / 2
            return [l[:a], l[a:]]

        def gen0(k):
            ret = []
            for s in random.sample(opts, k):
                n = random.randint(1, s - 1)
                ret.append([str(s), "%s + %s" % (n, s - n)])
            return shuffle(ret)

        for k in [2, 3]:
            for _ in range(5):
                Q("addition <= 10", pairing, {"question": gen0(k), "answer": 1}, active=False)

        def gen(k):
            return shuffle(
                [["%s + %s" % (n, s - n) if n else str(s)
                  for n in random.sample(range(s), 2)]
                 for s in random.sample(opts, k)])

        for k in [2, 3]:
            for _ in range(10):
                Q("addition <= 10", pairing, {"question": gen(k), "answer": 1}, active=False)

        opts = range(2, 21)
        for _ in range(10):
            Q("addition <= 20", pairing, {"question": gen(3), "answer": 1}, active=False)
        # end random.seed(8)

        # Subtraction:
        # ------------
        # up to 20
        for a in range(1, 21):
            for b in range(1, a + 1):
                skill = '%s-%s' % (a, b) if a <= 10 else 'subtraction <= 20'
                value = str(a - b) if a <= 10 else None
                kb = [0] + KB_10 if a <= 10 else KB_FULL
                Q(skill, free_answer,
                  {"question": "%s - %s" % (a, b), "answer": str(a - b),
                   "kb": kb}, value=value)
                Q(skill, counting,
                  {"question": [a, "-", b], "answer": str(a - b),
                   "with_text": True,
                   "kb": KB_FULL if a > 10 else kb}, value=value)
                if a <= 10:
                    Q(skill, counting,
                      {"question": [a, "-", b], "answer": str(a - b), "kb": kb, "with_text": True}, value=value)
        # multiples of 5:
        for a in range(25, 101, 5):
            for b in range(10, a + 1, 5):
                Q('subtraction', free_answer,
                  {"question": "%s - %s" % (a, b), "answer": str(a - b),
                   "kb": KB_FULL})

        # pairings:
        random.seed(4.5)

        def gen0(k, a=1, b=10):
            ret = []
            for t in random.sample(range(a, b), k):
                x = random.randint(t + 1, b)
                y = x - t  # x - y == t
                ret.append([str(t), "%s - %s" % (x, y)])
            return shuffle(ret)

        for k in [2, 3]:
            for _ in range(5):
                Q("subtraction <= 10", pairing, {"question": gen0(k), "answer": 1}, active=False)

        def gen(k, a=1, b=10):
            return shuffle(
                [["%s - %s" % (x, x - t) if x != t else str(t)
                  for x in random.sample(range(t, b + 1), 2)]
                 for t in random.sample(range(a, b), k)])

        for k in [2, 3]:
            for _ in range(10):
                Q("subtraction <= 10", pairing, {"question": gen(k), "answer": 1}, active=False)

        for _ in range(10):
            Q("subtraction <= 20", pairing, {"question": gen(3, a=1, b=20), "answer": 1}, active=False)
        # end random.seed(4.5)

        # Multiplication:
        # ---------------
        # fillin removed for now
        X = set([])
        for a in range(1, 11):
            for b in range(1, 21):
                X.add((a, b))
                X.add((b, a))
        for a, b in X:
            total = a * b
            skill = '%sx%s' % ((a, b) if a <= b else (b, a))
            Q(skill, free_answer,
              {"question": "%s &times; %s" % (a, b), "answer": str(total),
               "kb": KB_FULL}, value=skill)
            if total and a <= 5 and b <= 5:
                Q(skill, counting,
                  {"question": [a, "&times;", b], "answer": str(total), "kb": KB_FULL, "with_text": False}, value=skill,
                  active=False)
                Q(skill, counting,
                  {"question": [a, "&times;", b], "answer": str(total), "kb": KB_FULL, "with_text": True}, value=skill)
        for a, b, x in MULTI_2D:
            skill = '%sx%s' % ((a, b) if a <= b else (b, a))
            Q(skill, field, {"field": decode_field(x), "answer": a * b, "text": "{}&times;{}".format(a, b), "kb": KB_FULL}, value=skill)

        # pairings:
        random.seed(300000)
        resmap = defaultdict(set)
        for a in range(2, 11):
            for b in range(a, 11):
                t = a * b
                resmap[t].add('%s x %s' % (a, b))

        def gen0(k):
            ret = []
            for t in random.sample(resmap.keys(), k):
                ret.append([t, random.choice(list(resmap[t]))])
            return shuffle(ret)

        for k in [2, 3]:
            for _ in range(5):
                Q("multiplication1", pairing, {"question": gen0(k), "answer": 1}, active=False)

        def gen(k):
            ret = []
            for t in random.sample(resmap.keys(), k):
                ret.append(random.sample([t] + list(resmap[t]), 2))
            return shuffle(ret)

        for k in [2, 3]:
            for _ in range(10):
                Q("multiplication1", pairing, {"question": gen(k), "answer": 1}, active=False)

        resmap2 = defaultdict(set)
        for a in range(2, 11):
            for b in range(11, 21):
                t = a * b
                resmap[t].add('%s x %s' % (a, b))
                resmap2[t].add('%s x %s' % (a, b))

        for _ in range(10):
            Q("multiplication", pairing, {"question": gen(3), "answer": 1}, active=False)

        resmap = resmap2
        for _ in range(10):
            Q("multiplication2", pairing, {"question": gen0(3), "answer": 1}, active=False)
        # end random.seed(300000)

        # Division:
        # ---------------
        for a in range(1, 11):
            for b in range(1, 11):
                total = a * b
                skill = '%s/%s' % (total, b)
                Q(skill, free_answer,
                  {"question": "%s &divide; %s" % (total, b),
                   "answer": str(a), "kb": KB_10 if total <= 10 else KB_FULL}, value=str(a))

        # pairings:
        random.seed(30)
        resmap = defaultdict(set)
        for r in range(1, 11):
            for b in range(2, 11):
                a = r * b
                resmap[r].add('%s &divide; %s' % (a, b))

        for k in [2, 3]:
            for _ in range(5):
                Q("division1", pairing, {"question": gen0(k), "answer": 1}, active=False)
            for _ in range(10):
                Q("division1", pairing, {"question": gen(k), "answer": 1}, active=False)

        return json_data

def decode_field(x):
    f = []
    for _ in range(10):
        l = []
        for _ in range(10):
            l.append(x % 2)
            x /= 2
        f.append(l)
    return f


MULTI_2D = [(2, 3, 464378630459495837192945664L),
            (2, 3, 154969178502272764675620864L),
            (2, 3, 19399481727942022140002304L),
            (2, 3, 9250393634619130048L),
            (2, 4, 237846639445326993806761918464L),
            (2, 4, 522596296501679744700383232L),
            (2, 4, 1154050703082184704),
            (2, 4, 1210109869999860540899712L),
            (2, 5, 28398762501475955605504L),
            (2, 5, 56723756044357137858560L),
            (2, 5, 103197707267),
            (2, 5, 6762826379034624),
            (2, 6, 13524005906553863),
            (2, 6, 585591890901659839365888L),
            (2, 6, 237839390765114558718656118784L),
            (2, 6, 865536385542520832),
            (2, 7, 79363694432322696471365296128L),
            (2, 7, 18150415576909756659794304L),
            (2, 7, 59479188147825424126571446272L),
            (2, 7, 34691363653860296015247055873L),
            (2, 8, 56733024449089315406720L),
            (2, 8, 8674049894688032821547630592L),
            (2, 8, 987465131315188186071695360L),
            (2, 8, 147718558587690156032L),
            (2, 9, 304682363115028642499923972L),
            (2, 9, 3717450145393953000652800000L),
            (2, 9, 116170326411259308691959820L),
            (2, 9, 1172253701416500877864960L),
            (3, 3, 36947531355908046848L),
            (3, 3, 56686844967458573385728L),
            (3, 3, 309938357075969254948343808L),
            (3, 3, 928757260927972451006033920L),
            (3, 4, 4646808619143783718374604800L),
            (3, 4, 3462142213541468550),
            (3, 4, 8265294341421051936768L),
            (3, 4, 591304616683836040195L),
            (3, 5, 1021034858408497012277248L),
            (3, 5, 110813328328115356416L),
            (3, 5, 886452521854656780487L),
            (3, 5, 69382675075476798420709015552L),
            (3, 6, 1110277472734076420174643214350L),
            (3, 6, 28365863076177750523904L),
            (3, 6, 14439454636081689919488L),
            (3, 6, 3630322692470583673160128L),
            (3, 7, 77688898305312845124390092800L),
            (3, 7, 9460890615527114808321L),
            (3, 7, 1110123636939686138349900279820L),
            (3, 7, 16174678326082803714L),
            (3, 8, 148697875812599391790619028600L),
            (3, 8, 237955558470537786965218951168L),
            (3, 8, 29080397365116556410642432L),
            (3, 8, 1148655708563897843810400L),
            (3, 9, 37213154579451933607712623616L),
            (3, 9, 9529597067742907248672768L),
            (3, 9, 2425090119965366057760798L),
            (3, 9, 7434900890320627811238773216L),
            (4, 3, 2586075837127003865472L),
            (4, 3, 18546035474477096984L),
            (4, 3, 158692673272890295464306409472L),
            (4, 3, 3956979490425608131854729216L),
            (4, 4, 3716240331543867246739734528L),
            (4, 4, 952596677225177017088114429964L),
            (4, 4, 29739575162519877710670300000L),
            (4, 4, 116177305945846605171922950L),
            (4, 5, 7261819491800848501279842L),
            (4, 5, 69382821976627382039747952640L),
            (4, 5, 554834101537442777870031151120L),
            (4, 5, 38756461872547194141179936L),
            (4, 6, 555138736399351044355624143872L),
            (4, 6, 237916828001447363422181548440L),
            (4, 6, 37145455840499914054498785286L),
            (4, 6, 475862698529040163205745219584L),
            (4, 7, 29739603518627664503577131983L),
            (4, 7, 277887333493740473167445522460L),
            (4, 7, 34734856649201615118892678144L),
            (4, 7, 281306162543337430033841488096L),
            (4, 8, 7551072093673635286981017600L),
            (4, 8, 513008125343372103545263721475L),
            (4, 8, 594791503527368931051622085100L),
            (4, 8, 36338645525283320469600L),
            (4, 9, 297707658032167120305033543680L),
            (4, 9, 1200390146272375434120052736L),
            (4, 9, 1152022401078339277449854976L),
            (4, 9, 533170408860181543374L),
            (5, 3, 9918027424121098496110548996L),
            (5, 3, 14172576133636260302976L),
            (5, 3, 10034160753607357188307681280L),
            (5, 3, 10861594026327776763794441267L),
            (5, 4, 237923862880329115745668300800L),
            (5, 4, 951673722562841630721290803200L),
            (5, 4, 39933625710277159110606904L),
            (5, 4, 929361723828749583797455875L),
            (5, 5, 7444565326430069261486984193L),
            (5, 5, 67729807305564197290557496L),
            (5, 5, 35606341081893953254574809112L),
            (5, 5, 7900181541687806630524190944L),
            (5, 6, 55833858385178948508L),
            (5, 6, 951667376891870199085128942016L),
            (5, 6, 475833655951025656129802608519L),
            (5, 6, 556648963003825955287349262L),
            (5, 7, 969016606987217309266826443968L),
            (5, 7, 33457053954561209852973050899L),
            (5, 7, 619879964961195617002823023L),
            (5, 7, 18296790934171505512206568448L)]
