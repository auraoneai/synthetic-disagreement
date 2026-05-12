def generate(items, raters, noise_model, labels=None):
    labels = labels or sorted({item.get('label') for item in items})
    out={}
    for i,item in enumerate(items):
        for rater in raters:
            out[(item.get('item_id', i), rater)] = noise_model.corrupt(item.get('label'), labels, i)
    return out
