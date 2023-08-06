import jaconv


vowel_map =\
    [
        ['ア', 'アカサタナハマヤラワガザダバパァャ'],
        ['イ', 'イキシチニヒミリギジヂビピィ'],
        ['ウ', 'ウクスツヌフムユルグズヅブプゥュ'],
        ['エ', 'エケセテネヘメレゲゼデベペェ'],
        ['オ', 'オコソトノホモヨロヲゴゾドボポォョ'],
    ]


def text2boin(text, cv='katakana'):
    ## -----*----- 母音に変換 -----*----- ##
    if not cv in ('katakana', 'hiragana'):
        raise ValueError("argument cv allows 'katakana' or 'hiragana'")

    ret = ''
    text = jaconv.hira2kata(text)

    # replace
    for i, c in enumerate(text):
        for pair in vowel_map:
            # match
            if c in pair[1]:
                ret += pair[0]
        # not match
        if len(ret) == i:
            ret += c

    if cv == 'hiragana':
        ret = jaconv.kata2hira(ret)

    return ret
