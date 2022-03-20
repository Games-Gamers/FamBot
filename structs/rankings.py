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

famDict = {
    "isfam": [
        "WikiWikiWasp",
        "Wirt.zirp",
        "bossanova",
        "Snail",
        "The Mongoose",
        "shaggyzero",
        "ToeUp"
    ],
    "jsquad": [
        "WikiWikiWasp",
        "Wirt.zirp",
        "shaggyzero",
    ]
}

def fam_by_rank(fam_rank, users):

    fam = []

    for user_id in users:
        if users[user_id]["rank"] == fam_rank:
            fam.append(users[user_id]["name"])

    if fam:
        fam_str = "\n".join(fam)
        return fam_str
    else:
        return "none"
