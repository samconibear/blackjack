import pandas as pd

strat_hard_dict = {
    '2' : [1,1,2,2,1,0,0,0,0,0],
    '3' : [1,2,2,2,1,0,0,0,0,0],
    '4' : [1,2,2,2,0,0,0,0,0,0],
    '5' : [1,2,2,2,0,0,0,0,0,0],
    '6' : [1,2,2,2,0,0,0,0,0,0],
    '7' : [1,1,2,2,1,1,1,1,1,0],
    '8' : [1,1,2,2,1,1,1,1,1,0],
    '9' : [1,1,2,2,1,1,1,1,1,0],
    '10': [1,1,2,1,1,1,1,1,1,0],
    'A' : [1,1,1,1,1,1,1,1,1,0],
}
strat_hard_df = pd.DataFrame(strat_hard_dict, index =['5-8', '9', '10', '11','12','13','14','15','16','17'])

strat_soft_dict = {
    '2' : [1,1,1,1,1,0,0],
    '3' : [1,1,1,1,2,2,0],
    '4' : [1,1,2,2,2,2,0],
    '5' : [2,2,2,2,2,2,0],
    '6' : [2,2,2,2,2,2,0],
    '7' : [1,1,1,1,1,0,0],
    '8' : [1,1,1,1,1,0,0],
    '9' : [1,1,1,1,1,1,0],
    '10': [1,1,1,1,1,1,0],
    'A' : [1,1,1,1,1,1,0],
}
strat_soft_df = pd.DataFrame(strat_soft_dict, index =['13','14','15','16','17','18','19'])

strat_split_dict = {
    '2' : [4,4,1,2,4,4,4,4,0,4],
    '3' : [4,4,1,2,4,4,4,4,0,4],
    '4' : [4,4,1,2,4,4,4,4,0,4],
    '5' : [4,4,4,2,4,4,4,4,0,4],
    '6' : [4,4,4,2,4,4,4,4,0,4],
    '7' : [4,4,1,2,1,4,4,0,0,4],
    '8' : [1,1,1,2,1,1,4,4,0,4],
    '9' : [1,1,1,2,1,1,4,4,0,4],
    '10': [1,1,1,1,1,1,4,0,0,4],
    'A' : [1,1,1,1,1,1,4,0,0,4],
}
strat_split_df = pd.DataFrame(strat_split_dict, index =['4','6','8','10','12','14','16','18','20','AA'])

def Basic_Strategy(total, dealers_card, soft, can_split):

    total = int(total)

    if dealers_card == 'J':
        dealers_card = '10'
    if dealers_card == 'K':
        dealers_card = '10'
    if dealers_card == 'Q':
        dealers_card = '10'

    if total == 2:
        return 'sp'

    if soft:
        # Case for A-A

        if total >= 19:
            total = '19'
        output = strat_soft_df.loc[str(total), str(dealers_card)]

    elif can_split:
        output = strat_split_df.loc[str(total), str(dealers_card)]

    else:
        if total <= 9:
            total = '5-8'
        elif total >= 17:
            total = '17'
        output = strat_hard_df.loc[str(total), str(dealers_card)]

    if output == 0:
        return 's'
    if output == 1:
        return 'h'
    if output == 2:
        return 'd'
    if output == 4:
        return 'sp'