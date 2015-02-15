#coding: utf-8

def has_equivalents(target_values, pattern_values):
    used = set()
    for pattern in pattern_values:
        found_equivalent = False
        for index, target in enumerate(target_values):
            if index not in used and target.sub_equivalent_pattern(pattern):
                found_equivalent = True
                break
        if not found_equivalent:
            return False
    return True
