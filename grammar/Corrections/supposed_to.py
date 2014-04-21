#!/usr/bin/env python

SET_3 = set(['he', 'she', 'it'])
SET_2 = set(['we', 'you', 'they'])  # 'i'


def do(self, cur):
    """Keyword: supposed
    Src: (<word> doesn't|I don't|<word> (?<!I )don't) _ to
    Dst: [isn't|I'm not|aren't] _ to

    NOTE: causes extension - don't -> [aren't]
    """
    if not self.sequence.next_has_continuous(1):
        return
    if self.sequence.next_word(1).word_lower != 'to':
        return
    if not self.sequence.prev_has_continuous(2):
        return
    person = 2  # note: 2nd person is the same as plural
    prev_word_1 = self.sequence.prev_word(1)
    prev_word_2 = self.sequence.prev_word(2)
    if prev_word_2.word_lower == "i":
        person = 1
    elif prev_word_1.word_lower == "don't":
        if prev_word_2.word_lower in SET_3:
            person = 3
        # else: person = 2
    elif prev_word_1.word_lower == "doesn't":
        # person = 2
        if not prev_word_2.word_lower in SET_2:
            person = 3
    else:
        return
    self.matched('supposed-to')
    cur.mark_common()
    self.sequence.next_word(1).mark_common()
    if person == 1:
        # special: [I'm not] supposed to
        prev_word_2.replace("I'm")
        prev_word_1.replace('not')
    elif person == 2:
        prev_word_1.replace("aren't")
        self.rerun.add(11)  # Rerun: your_are for "you aren't"
    else:  # person == 3
        prev_word_1.replace("isn't")
