def cut_with_seprator(text, seprator, max_seq_len):
    result = []
    if len(text) == 0:
        return result
    if len(text) <= max_seq_len or seprator not in text or (text.count(seprator) == 1 and text[-1] == seprator):
        result.append(text)
        return result
    else:
        segments = text.split(seprator)
        for i in range(len(segments)):
            if i == len(segments) - 1:
                segment = segments[i]
                result.extend(cut_with_seprator(segment, seprator, max_seq_len))
            else:
                segment = segments[i] + seprator
                result.extend(cut_with_seprator(segment, seprator, max_seq_len))
        return result


def cut_with_specific_length(text, length):
    result = []
    times = (len(text) + length - 1) //  length
    for i in range(times):
        result.append(text[i*length:(i+1)*length])
    return result


def hard_split(texts, max_seq_len):
    for i in range(len(texts)):
        text = texts[i]
        if len(text) > max_seq_len:
            texts = texts[0:i] + cut_with_specific_length(text, max_seq_len) + texts[i+1:]
    return texts


def cut_with_seprator_list(texts, max_seq_len, seprators=['。', '？', '！', '，', ',']):
    for seprator in seprators:
        for i in range(len(texts)):
            text = texts[i]
            if len(text) > max_seq_len:
                texts = texts[0:i] + cut_with_seprator(text, seprator, max_seq_len) + texts[i+1:]

    result = hard_split(texts, max_seq_len)
    return result


if __name__ == '__main__':
    max_seq_len = 20
    text = 'jfdljfdkldjir，kdie。jfdl，jfdk，ldjir，kdie，jfdk，iega，woshe，haen。'
    results = cut_with_seprator_list([text], max_seq_len)
    print(results)
