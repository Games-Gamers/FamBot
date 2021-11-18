import json

rank_title = {
    1: 'Weak',
    2: 'Step Fam',
    3: 'FAM',
    4: 'True Fam',
    5: 'Elder Fam',
    6: 'Royal Fam',
    7: 'Super Fam',
    8: 'Ultra Fam',
    9: 'God Fam',
    10: 'OnlyFams'
}

def fam_by_rank(fam_rank):
    if isinstance(fam_rank, int):
        fam_rank = str(fam_rank)

    fam = []
    with open('structs/users.json', 'r') as f:
        users = json.load(f)

    for user_id in users:
        if any(fam_rank in rank for rank in users[user_id]["rank"]):
            fam.append(users[user_id]["name"])
    
    fam_str = "\n".join(fam)
    
    return fam_str
