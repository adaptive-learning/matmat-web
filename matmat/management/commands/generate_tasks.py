import os
import json
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Generate skills and tasks'
    data_dir = 'data'

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False)
        self.skills = {}
        self.contexts = {}

    def handle(self, *args, **options):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        skills = self.generate_skills()
        json.dump({'skills': skills}, open(os.path.join(self.data_dir, 'matmat-skills.json'), 'w'), indent=4)
        contexts = self.generate_contexts()
        json.dump({'contexts': contexts}, open(os.path.join(self.data_dir, 'matmat-contexts.json'), 'w'), indent=4)
        instances, tasks = self.generate_tasks()
        json.dump({'tasks': tasks, 'instances': instances}, open(os.path.join(self.data_dir, 'matmat-tasks.json'), 'w'), indent=4)

    def generate_skills(self):
        skills = []

        def add_skill(identifier, parent, name=None, active=True):
            skill = {
                'id': identifier,
                'names': {'cs': name if name is not None else identifier},
                'parents': [] if parent is None else [parent['id']],
            }
            if not active:
                skill['active'] = active
            skills.append(skill)
            self.skills[identifier] = skill
            return skill

        # Main math skill:
        # ----------------
        math = add_skill('math', None, 'Vše')

        # Numbers:
        # --------
        numbers = add_skill('numbers', math, 'Počítání')
        num10 = add_skill('numbers_leq_10', numbers, 'Počítání do 10')
        num20 = add_skill('numbers_leq_20', numbers, 'Počítání do 20')
        for n in range(1, 21):
            add_skill(str(n), num10 if n <= 10 else num20)

        # Addition:
        # ---------
        addition = add_skill('addition', math, u'Sčítání')
        a1 = add_skill('addition_leq_10', addition, u'Sčítání do 10')
        a2 = add_skill('addition_leq_20', addition, u'Sčítání do 20')
        add_skill('addition_leq_100', addition, u'Sčítání do 100')
        for a in range(20):
            for b in range(a, 21):
                if a + b <= 20:
                    add_skill('%s+%s' % (a, b), a1 if a + b <= 10 else a2, active=a > 0)

        # Subtraction:
        # ------------
        subtr = add_skill('subtraction', math, u'Odčítání')
        s1 = add_skill('subtraction_leq_10', subtr, u'Odčítání do 10')
        s2 = add_skill('subtraction_leq_20', subtr, u'Odčítání do 20')
        for a in range(1, 11):
            for b in range(1, a + 1):
                add_skill('%s-%s' % (a, b), s1)

        # Multiplication:
        # ---------------
        m0 = add_skill('multiplication', math, u'Násobení')
        m1 = add_skill('multiplication_small', m0, u'Malá násobilka')
        for b in range(1, 11):
            for a in range(1, b + 1):
                add_skill('%sx%s' % (a, b), m1, '%s&times;%s' % (a, b))
        m2 = add_skill('multiplication_big', m0, u'Velká násobilka')
        for a in range(1, 11):
            for b in range(11, 21):
                add_skill('%sx%s' % (a, b), m2, '%s&times;%s' % (a, b))

        # Division:
        # ---------
        d0 = add_skill('division', math, u'Dělení')
        d1 = add_skill('division1', d0, u'Dělení malých čísel')
        for a in range(1, 11):
            for b in range(1, 11):
                total = a * b
                add_skill('%s/%s' % (total, b), d1)

        return skills

    def generate_contexts(self):
        contexts= []

        def add_context(identifier, name, content=None, active=True):
            context = {
                'id': identifier,
                'names': {
                    'cs': name
                },
                'contents': {
                    'cs': content
                }
            }
            if not active:
                context['active'] = active
            contexts.append(context)
            self.contexts[identifier] = context
            return context

        add_context('written_question', 'Psaná otázka', {'directive': 'simple'})
        add_context('object_counting', 'Počítání předmětů', {'directive': 'object-counting', 'with_numbers': False})
        add_context('object_counting_with_numbers', 'Počítání předmětů s čísly', {'directive': 'object-counting', 'with_numbers': True})
        add_context('object_selection_answer', 'Výběr správného počtu předmětů', {'directive': 'object-selection'})
        add_context('number_line_answer', 'Výběr odpovědi na číselné ose', {'directive': 'number-line'})
        add_context('multiplication_visualization_field', 'Počítání předmětů v mřížce', {'directive': 'multiplication-field'})
        add_context('division_visualization_baskets', 'Vizualizace dělení', {'directive': 'division-baskets'})

        return contexts

    def generate_tasks(self):
        instances = []
        tasks = []
        task_map = {}
        instance_identifiers = []

        def add_task(identifier, skill, content, contexts, active=True):
            if identifier in task_map:
                task = task_map[identifier]
                if task['contents']['cs'] != content or task['skills'][0] != skill:
                    raise CommandError('Tasks do no not fit: {}'.format(task))
            else:
                task = {
                    'id': identifier,
                    'contents': {
                        'cs': content
                    },
                    'skills': [skill],
                }
                tasks.append(task)
                task_map[identifier] = task
            if not active:
                task['active'] = active

            contexts_dict = {c: None for c in contexts} if type(contexts) == list else contexts

            for context, description in contexts_dict.items():
                instance_identifier = '{}-{}'.format(identifier, context)
                i = 1
                while instance_identifier in instance_identifiers:
                    instance_identifier = '{}-{}-{}'.format(identifier, context, i)
                    i += 1
                instance_identifiers.append(instance_identifier)
                instance = {
                    'id': instance_identifier,
                    'task': identifier,
                    'context': context,
                    'descriptions': {
                        'cs': description,
                    }
                }
                if not active:
                    instance['active'] = active
                instances.append(instance)

        # Numbers:
        # --------
        for n in range(1, 21):
            value = str(n)
            # for numbers up to 7 ... choice up to 10
            # for numbers up to 17 ... choice up to 20
            # for numbers above .... choice up to a 100
            rows = 1 if n <= 7 else 2

            add_task(value, value, {'operands': [n], 'answer': n}, {
                'object_selection_answer': {'rows': rows},      # number -> select objects
                'object_counting': None,                        # objects -> number
                'number_line_answer': None,                     # number -> number-line
            })

        # Addition:
        # ---------
        for a in range(1, 21):
            for b in range(1, 21):
                total = a + b
                if total > 20:
                    continue
                x, y = (a, b) if a <= b else (b, a)
                identifier = '{}+{}'.format(a, b)
                skill = '{}+{}'.format(x, y)
                add_task(identifier, skill, {'operation': '+', 'operands': [a, b], 'answer': a + b}, ['written_question', 'object_counting_with_numbers'])
        skill = 'addition_leq_100'
        for a, b in RAND_ADD_1:
            identifier = '{}+{}'.format(a, b)
            add_task(identifier, skill, {'operation': '+', 'operands': [a, b], 'answer': a + b}, ['written_question'])

        for a, b in RAND_ADD_2:
            if a <= 20 and a + b <= 20:
                x, y = (a, b) if a <= b else (b, a)
                skill = '{}+{}'.format(x, y)
            else:
                skill = 'addition_leq_100'
            identifier = '{}+{}'.format(a, b)
            add_task(identifier, skill, {'operation': '+', 'operands': [a, b], 'answer': a + b}, ['object_counting_with_numbers'])

        # Subtraction:
        # ------------
        # up to 20
        for a in range(1, 21):
            for b in range(1, a + 1):
                skill = '{}-{}'.format(a, b) if a <= 10 else 'subtraction_leq_20'
                identifier = '{}-{}'.format(a, b)
                add_task(identifier, skill, {'operation': '-', 'operands': [a, b], 'answer': a - b}, ['written_question', 'object_counting_with_numbers'])
        # multiples of 5:
        for a in range(25, 101, 5):
            for b in range(10, a + 1, 5):
                add_task('{}-{}'.format(a, b), 'subtraction', {'operation': '-', 'operands': [a, b], 'answer': a - b}, ['written_question'])


        # Multiplication:
        # ---------------
        X = set([])
        for a in range(1, 11):
            for b in range(1, 21):
                X.add((a, b))
                X.add((b, a))
        for a, b in X:
            total = a * b
            skill = '{}x{}'.format(*((a, b) if a <= b else (b, a)))
            identifier = '{}x{}'.format(a, b)
            add_task(identifier, skill, {'operation': 'x', 'operands': [a, b], 'answer': a * b}, ['written_question'])
            if total and a <= 5 and b <= 5:
                add_task(identifier, skill, {'operation': 'x', 'operands': [a, b], 'answer': a * b}, ['object_counting_with_numbers'])

        for a, b, x in MULTI_2D:
            skill = '{}x{}'.format(*((a, b) if a <= b else (b, a)))
            identifier = '{}x{}'.format(a, b)
            add_task(identifier, skill, {'operation': 'x', 'operands': [a, b], 'answer': a * b}, {
                'multiplication_visualization_field': {"field": decode_field(x)}
            })

        # Division:
        # ---------------
        for a in range(1, 11):
            for b in range(1, 11):
                total = a * b
                skill = '{}/{}'.format(total, b)
                add_task(skill, skill, {'operation': '/', 'operands': [total, b], 'answer': a}, ['written_question'])
                if b <= 4 and a <= 6:
                    add_task(skill, skill, {'operation': '/', 'operands': [total, b], 'answer': a}, ['division_visualization_baskets'])

        return instances, tasks


def decode_field(x):
    f = []
    for _ in range(10):
        l = []
        for _ in range(10):
            l.append(x % 2)
            x //= 2
        f.append(l)
    return f

RAND_ADD_1 = [(2, 34), (3, 58), (4, 50), (4, 67), (4, 81), (6, 56), (7, 58), (8, 23), (8, 57), (8, 75), (9, 48), (10, 30), (10, 37), (10, 87), (11, 43), (12, 55), (16, 39), (17, 39), (17, 52), (17, 57), (17, 74), (20, 50), (20, 56), (21, 69), (22, 66), (23, 9), (24, 32), (24, 33), (25, 50), (25, 66), (27, 2), (28, 13), (28, 72), (29, 11), (29, 16), (29, 25), (29, 31), (29, 71), (30, 45), (30, 57), (31, 12), (31, 37), (31, 64), (32, 59), (34, 46), (34, 58), (35, 4), (35, 39), (35, 65), (37, 21), (37, 44), (38, 9), (38, 49), (39, 12), (39, 40), (40, 40), (40, 47), (41, 40), (42, 39), (42, 41), (42, 50), (45, 55), (46, 10), (46, 20), (47, 13), (47, 15), (47, 51), (48, 12), (48, 51), (49, 22), (50, 8), (50, 39), (50, 47), (51, 20), (51, 33), (52, 9), (52, 22), (53, 12), (55, 33), (56, 10), (56, 20), (57, 23), (61, 21), (61, 22), (61, 31), (61, 32), (64, 25), (65, 16), (65, 23), (65, 25), (67, 7), (69, 3), (71, 6), (71, 16), (73, 6), (75, 13), (77, 15), (78, 14), (82, 7), (86, 4)]
RAND_ADD_2 = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 15), (1, 30), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 40), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 25), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 13), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 19), (6, 48), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 32), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 24), (11, 47), (14, 2), (15, 6), (16, 15), (18, 27), (20, 28), (20, 33), (23, 8), (24, 33), (28, 6), (28, 24), (29, 4), (30, 20), (31, 25), (31, 47), (32, 41), (33, 39), (34, 31), (34, 35), (35, 5), (35, 10), (35, 26), (35, 41), (35, 45), (36, 24), (36, 43), (37, 48), (38, 7), (38, 36), (39, 47), (40, 25), (40, 37), (41, 44), (42, 15), (42, 40), (43, 42), (44, 4), (44, 33), (46, 9), (46, 40), (48, 47)]


MULTI_2D = [(2, 3, 464378630459495837192945664),
            (2, 3, 154969178502272764675620864),
            (2, 3, 19399481727942022140002304),
            (2, 3, 9250393634619130048),
            (2, 4, 237846639445326993806761918464),
            (2, 4, 522596296501679744700383232),
            (2, 4, 1154050703082184704),
            (2, 4, 1210109869999860540899712),
            (2, 5, 28398762501475955605504),
            (2, 5, 56723756044357137858560),
            (2, 5, 103197707267),
            (2, 5, 6762826379034624),
            (2, 6, 13524005906553863),
            (2, 6, 585591890901659839365888),
            (2, 6, 237839390765114558718656118784),
            (2, 6, 865536385542520832),
            (2, 7, 79363694432322696471365296128),
            (2, 7, 18150415576909756659794304),
            (2, 7, 59479188147825424126571446272),
            (2, 7, 34691363653860296015247055873),
            (2, 8, 56733024449089315406720),
            (2, 8, 8674049894688032821547630592),
            (2, 8, 987465131315188186071695360),
            (2, 8, 147718558587690156032),
            (2, 9, 304682363115028642499923972),
            (2, 9, 3717450145393953000652800000),
            (2, 9, 116170326411259308691959820),
            (2, 9, 1172253701416500877864960),
            (3, 3, 36947531355908046848),
            (3, 3, 56686844967458573385728),
            (3, 3, 309938357075969254948343808),
            (3, 3, 928757260927972451006033920),
            (3, 4, 4646808619143783718374604800),
            (3, 4, 3462142213541468550),
            (3, 4, 8265294341421051936768),
            (3, 4, 591304616683836040195),
            (3, 5, 1021034858408497012277248),
            (3, 5, 110813328328115356416),
            (3, 5, 886452521854656780487),
            (3, 5, 69382675075476798420709015552),
            (3, 6, 1110277472734076420174643214350),
            (3, 6, 28365863076177750523904),
            (3, 6, 14439454636081689919488),
            (3, 6, 3630322692470583673160128),
            (3, 7, 77688898305312845124390092800),
            (3, 7, 9460890615527114808321),
            (3, 7, 1110123636939686138349900279820),
            (3, 7, 16174678326082803714),
            (3, 8, 148697875812599391790619028600),
            (3, 8, 237955558470537786965218951168),
            (3, 8, 29080397365116556410642432),
            (3, 8, 1148655708563897843810400),
            (3, 9, 37213154579451933607712623616),
            (3, 9, 9529597067742907248672768),
            (3, 9, 2425090119965366057760798),
            (3, 9, 7434900890320627811238773216),
            (4, 3, 2586075837127003865472),
            (4, 3, 18546035474477096984),
            (4, 3, 158692673272890295464306409472),
            (4, 3, 3956979490425608131854729216),
            (4, 4, 3716240331543867246739734528),
            (4, 4, 952596677225177017088114429964),
            (4, 4, 29739575162519877710670300000),
            (4, 4, 116177305945846605171922950),
            (4, 5, 7261819491800848501279842),
            (4, 5, 69382821976627382039747952640),
            (4, 5, 554834101537442777870031151120),
            (4, 5, 38756461872547194141179936),
            (4, 6, 555138736399351044355624143872),
            (4, 6, 237916828001447363422181548440),
            (4, 6, 37145455840499914054498785286),
            (4, 6, 475862698529040163205745219584),
            (4, 7, 29739603518627664503577131983),
            (4, 7, 277887333493740473167445522460),
            (4, 7, 34734856649201615118892678144),
            (4, 7, 281306162543337430033841488096),
            (4, 8, 7551072093673635286981017600),
            (4, 8, 513008125343372103545263721475),
            (4, 8, 594791503527368931051622085100),
            (4, 8, 36338645525283320469600),
            (4, 9, 297707658032167120305033543680),
            (4, 9, 1200390146272375434120052736),
            (4, 9, 1152022401078339277449854976),
            (4, 9, 533170408860181543374),
            (5, 3, 9918027424121098496110548996),
            (5, 3, 14172576133636260302976),
            (5, 3, 10034160753607357188307681280),
            (5, 3, 10861594026327776763794441267),
            (5, 4, 237923862880329115745668300800),
            (5, 4, 951673722562841630721290803200),
            (5, 4, 39933625710277159110606904),
            (5, 4, 929361723828749583797455875),
            (5, 5, 7444565326430069261486984193),
            (5, 5, 67729807305564197290557496),
            (5, 5, 35606341081893953254574809112),
            (5, 5, 7900181541687806630524190944),
            (5, 6, 55833858385178948508),
            (5, 6, 951667376891870199085128942016),
            (5, 6, 475833655951025656129802608519),
            (5, 6, 556648963003825955287349262),
            (5, 7, 969016606987217309266826443968),
            (5, 7, 33457053954561209852973050899),
            (5, 7, 619879964961195617002823023),
            (5, 7, 18296790934171505512206568448)]