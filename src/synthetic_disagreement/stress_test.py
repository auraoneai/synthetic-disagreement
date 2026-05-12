def degradation_curve(items, raters, model_factory, levels):
    from iaa_kit import fleiss_kappa
    rows=[]
    for level in levels:
        generated = __import__('synthetic_disagreement.generators', fromlist=['generate']).generate(items, raters, model_factory(level), sorted({i['label'] for i in items}))
        matrix=[[generated[(item.get('item_id', idx), r)] for r in raters] for idx,item in enumerate(items)]
        rows.append({"noise": level, "agreement": fleiss_kappa(matrix)})
    return rows
