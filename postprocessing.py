import numpy as np

input = [23, 22, 21, 21] # 모델에서 나오는 class output을 네 개를 가져온다.
pred_score = [0.95, 0.89, 0.93, 0.97] #그 class output 각각에 대한 probability

upper_template = [18, 17, 16, 15, 14, 13 ,12, 11, 21, 22, 23, 24, 25, 26, 27, 28] #치아 upper 템플릿 순서 
upper_dentition = {
    'W' : [18, 28],
    'M' : [16, 17, 26, 27],
    'P' : [14, 15, 24, 25],
    'Ca' : [13, 23],
    'La' : [12, 22],
    'Ce' : [11, 21]
}
#치아 upper에 대한 category안의 치아 번호들

lower_template = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38] #치아 lower 템플릿 순서 
lower_dentition = {
    'W' : [38, 48],
    'M' : [36, 37, 46, 47],
    'P' : [34, 35, 44, 45],
    'Ca' : [33 ,43],
    'I' : [31, 32, 41, 42]
}
#치아 lower에 대한 category안의 치아 번호들
if input[0] in upper_template and input[1] in upper_template:
    mode = 'upper'
else:
    mode = 'lower'
#input안의 class output이 위에 속하면 mode는 upper가 되고, 아래면 lower가 된다.
input_category = []

if mode == 'upper':
    for num in input:
        if num in upper_dentition['W']:
            input_category.append('W')
        elif num in upper_dentition['M']:
            input_category.append('M')
        elif num in upper_dentition['P']:
            input_category.append('P')
        elif num in upper_dentition['Ca']:
            input_category.append('Ca')
        elif num in upper_dentition['La']:
            input_category.append('La')
        else:
            input_category.append('Ce')

else:
    for num in input:
        if num in lower_dentition['W']:
            input_category.append('W')
        elif num in lower_dentition['M']:
            input_category.append('M')
        elif num in lower_dentition['P']:
            input_category.append('P')
        elif num in lower_dentition['Ca']:
            input_category.append('Ca')
        else:
            input_category.append('I')
#output의 class 들을 category별로 정리한다.

upper_index = {'W' : 0, 'M' : 1,'P' : 2,'Ca' : 3,'La' : 4,'Ce' : 5}
lower_index = {'W' : 0, 'M' : 1,'P' : 2,'Ca' : 3, 'I' : 4}

upper_similarity_matrix = np.array([
    [0.9, 0.8, 0, 0, 0, 0],
    [0.8, 0.9, 0, 0, 0, 0],
    [0, 0, 0.9, 0.6, 0.4, 0.4],
    [0, 0, 0.6, 0.9, 0.6, 0.8],
    [0, 0, 0.4, 0.6, 0.9, 0.8],
    [0, 0, 0.4, 0.8, 0.8, 0.9]
])

lower_similarity_matrix = np.array([
    [0.9, 0.7, 0, 0, 0],
    [0.7, 0.9, 0, 0, 0],
    [0, 0, 0.9, 0.5, 0.3],
    [0, 0, 0.5, 0.9, 0.5],
    [0, 0, 0.3, 0.5, 0.9]
])
#논문에서 나온 table을 넘파이 배열로 정리

comparison_score = [] 
for i in range(len(upper_template) - len(input) + 1):
    #치아를 위 아래의 경우로 나누어 각각 슬라이딩 해가면서 comparison score를 저장한다.
    template_category = []
    if mode == 'upper':
        for j in range(i, len(input)+i):
            if upper_template[j] in upper_dentition['W']:
                template_category.append('W')
            elif upper_template[j] in upper_dentition['M']:
                template_category.append('M')
            elif upper_template[j] in upper_dentition['P']:
                template_category.append('P')
            elif upper_template[j] in upper_dentition['Ca']:
                template_category.append('Ca')
            elif upper_template[j] in upper_dentition['La']:
                template_category.append('La')
            else:
                template_category.append('Ce')
    else:
        for j in range(i, len(input)+i):
            if lower_template[j] in lower_dentition['W']:
                template_category.append('W')
            elif lower_template[j] in lower_dentition['M']:
                template_category.append('M')
            elif lower_template[j] in lower_dentition['P']:
                template_category.append('P')
            elif lower_template[j] in lower_dentition['Ca']:
                template_category.append('Ca')
            else:
                template_category.append('I')


    print(template_category)
    match_score = 0
    mismatch_score = 0
    
    for k in range(len(input)):
        if mode == 'upper':
            if input[k] == upper_template[k+i]:
                print('match로 계산')
                match_score += pred_score[k]*100
            else:
                print('mismatch')
                mismatch_score = mismatch_score + (pred_score[k]*100 * upper_similarity_matrix[upper_index[input_category[k]],upper_index[template_category[k]]])

        else:
            if input[k] == lower_template[k+i]:
                print('match로 계산')
                match_score += pred_score[k]*100
            else:
                print('mismatch')
                mismatch_score = mismatch_score + (pred_score[k]*100 * lower_similarity_matrix[lower_index[input_category[k]],lower_index[template_category[k]]])

    comparison_score.append(match_score + mismatch_score)
print(list(map(int, comparison_score)))

#input의 값을 정리해본다.
max = -1
for i, value in enumerate(comparison_score):
    if value > max:
        idx = i
        max = value
print('기존의 numbering : ', input)
if mode == 'upper':
    input = upper_template[idx:idx+len(input)]
else:
    input = lower_template[idx:idx+len(input)]

print('post processing으로 처리된 numbering : ',  input)