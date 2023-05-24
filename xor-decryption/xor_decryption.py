import itertools
import string


def read_file_in_chunks(file_name, chunk_size):
    with open(file_name, 'rb') as f:
        data = f.read().decode('utf-8')

    return [data[i:i+chunk_size]
            for i in range(0, len(data), chunk_size)]


def hamming_score(text1, text2):
    assert(len(text1) == len(text2))

    hamming_dist = sum(bin(ord(t1) ^ ord(t2)).count('1')
                       for t1, t2 in zip(text1, text2))

    # normalize hamming distance by bytes length
    return hamming_dist / (8 * len(text1))


def get_key_len(enc_file):
    hamming_scores = dict()

    # we know the key is between 5 and 9 characters
    for k_len in range(5, 10):
        chunks = read_file_in_chunks(enc_file, k_len)

        # compute scores for adjacent chunks
        scores = [hamming_score(chunks[i], chunks[i+1])
                  for i in range(len(chunks) - 2)]

        # compute the avarage score
        hamming_scores[k_len] = sum(scores) / len(scores)

    return min(hamming_scores, key=hamming_scores.get)


def frequency_score(text):
    most_freq = 'ETAOIN SHRDLU'  # most frequent letters in English
    return sum(ch.upper() in most_freq for ch in text)


def find_key_piece(text):
    scores = dict()

    # the key contains only lower and upper case letters
    for k in string.ascii_letters:
        xored = ''.join(chr(ord(t) ^ ord(k)) for t in text)

        scores[k] = frequency_score(xored)

    return max(scores, key=scores.get)


def find_key(enc_file, key_len):
    chunks = read_file_in_chunks(enc_file, key_len)

    # remove last chunk as it may be incomplete
    chunks = chunks[:-1]

    # transpose the chunks
    chunks = [[chunk[i] for chunk in chunks] for i in range(key_len)]

    return ''.join(find_key_piece(chunk) for chunk in chunks)


def decrypt_file(enc_file, dec_file, key):
    with open(enc_file, 'rb') as f:
        data = f.read().decode('utf-8')

    text = ''.join(chr(ord(data[i]) ^ ord(key[i % len(key)]))
                   for i in range(len(data)))

    with open(dec_file, 'w', encoding='utf-8') as f:
        f.write(text)


enc_file = ''
dec_file = ''

key_len = get_key_len(enc_file)
print(f'key_len = {key_len}')

key = find_key(enc_file, key_len)
print(f'key = {key}')

decrypt_file(enc_file, dec_file, key)
