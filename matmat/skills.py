SKILL_TABLES = {
    'numbers_leq_10':
        [[str(c + r * 10) for c in range(1, 11)] for r in range(1)],
    'numbers_leq_20':
        [[str(c + r * 10) for c in range(1, 11)] for r in range(1, 2)],
    'addition_leq_10':
        [['%s+%s' % (r, c) for c in range(1, 10 - r + 1)] for r in range(1, 6)],
    'addition_leq_20':
        [['%s+%s' % (c, r - c) for c in range(1, 11) if r - c >= c] for r in range(11, 21)],
    'subtraction_leq_10':
        [['%s-%s' % (r, c) for c in range(1, r + 1)] for r in range(1, 11)],
    'multiplication_small':
        [['%sx%s' % (c, r) for c in range(1, 11)] for r in range(1, 11)],
    'multiplication_big':
        [['%sx%s' % (c, r) for c in range(1, 11)] for r in range(11, 21)],
    'division1':
        [['%s/%s' % (a * b, b) for a in range(1, 11)] for b in range(1, 11)],
}