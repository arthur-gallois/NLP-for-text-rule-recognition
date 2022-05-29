import keyword_extract_rules as ker
import dataset_utility as du

A = du.getJson('Sport_rules').get_sentences()


def test_extract(data):
    result = [0,0]
    print('sont des règles')
    for i in range(len(data[0])):
        if ker.is_rule(data[0][i]):
            result[0] += 1
        else:
            print(data[0][i])
    print('ne sont pas des règles')
    for j in range(len(data[1])):
        if not ker.is_rule(data[1][j]):
            result[1] += 1
        else:
            print(data[1][j])
    if result[0] != 0:
        result[0] /= len(data[0])
    if result[1] != 0:
        result[1] /= len(data[1])
    return result

print(test_extract(A))

'''
Il faudra faire un argument till '','' pour le when
'''