MISMATCH_SCORE = -1
INDEL_SCORE = -1
MATCH_SCORE = 1


def print_dp_table(table, result, correct, R, C):

    for i in range(C+1):
        if i == 0:
            print('　'*7, end=' ')
        else:
            print(f"{correct[i-1]:3s}", end='　')
    print()

    for j in range(R+1):
        for i in range(C+1):
            if j == 0:
                if i == 0:
                    print(' '*4, end='　')
                print(f"{table[j][i]:4d}", end='　')
            elif i == 0 and j <= len(result):
                print(f"{result[j-1]:3s}", end='　')
                print(f"{table[j][i]:4d}", end='　')
            else:
                print(f"{table[j][i]:4d}", end='　')
        print()


def print_align_table(table, result, correct, R, C):

    for i in range(C+1):
        if i == 0:
            print('　'*5, end=' ')
        else:
            print(f"{correct[i-1]:3s}", end='　')
    print()

    for j in range(R+1):
        for i in range(C+1):
            if j == 0:
                if i == 0:
                    print(' '*4, end='　')
                print(f"{table[j][i]:4s}", end='　')
            elif i == 0 and j <= len(result):
                print(f"{result[j-1]:3s}", end='　')
                print(f"{table[j][i]:4s}", end='　')
            else:
                print(f"{table[j][i]:4s}", end='　')
        print()

def print_str_align(str_alignments):
    print(str_alignments['correct'])
    for i in range(len(str_alignments['correct'])):
        if str_alignments['correct'] == str_alignments['result']:
            print("｜", end='')
        else:
            print("　", end='')
    print()
    print(str_alignments['result'])


def make_dp_table(result, correct, R, C):

    value_table = [[0]*(C+1) for _ in range(R+1)]
    align_table = [[' ']*(C+1) for _ in range(R+1)]
    
    for j in range(C+1):
        value_table[0][j] = -j
    for i in range(R+1):
        value_table[i][0] = -i

    for i in range(1, R+1):  # rows
        for j in range(1, C+1): # columns
            if correct[j-1] == result[i-1]: # correct
                value_table[i][j] = value_table[i-1][j-1] + MATCH_SCORE
                align_table[i][j] = '\\'
            elif value_table[i][j-1] > value_table[i][j]: # indel from top
                value_table[i][j] = value_table[i][j-1] + INDEL_SCORE
                align_table[i][j] = '|'
            else: # table[i-1][j-1] > table[i][j-1]: # mismatch
                value_table[i][j] = value_table[i-1][j-1] + MISMATCH_SCORE
                align_table[i][j] = '\\'
    return {'value': value_table, 'alignment': align_table}


def determine_alignment(table, result, correct, i, j):

    res_align = ''
    cor_align = ''
    align_str = ''

    while i > 0 and j > 0:
        if i > 0 and j > 0 and result[i-1] == correct[j-1]:
            res_align = result[i-1] + res_align
            cor_align = correct[j-1] + cor_align
            align_str = "+" + align_str
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and table[i][j] == table[i-1][j-1] + MISMATCH_SCORE:
            res_align = result[i-1] + res_align
            cor_align = correct[j-1] + cor_align
            align_str = "-" + align_str
            i -= 1
            j -= 1
        else:
            res_align = '＿' + res_align
            cor_align = correct[j-1] + cor_align
            align_str = "-" + align_str
            j -= 1

    return {"result": list(res_align), "correct": list(cor_align), "align_str": list(align_str)}
