from collections import OrderedDict
from goods.models import GoodsCategory, GoodsChannel


def get_categories():
    # 查询并展示商品分类
    categories = OrderedDict()
    # 查询所有的商品频道
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')

    for channel in channels:
        group_id = channel.group_id
        # print(group_id)
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        # print(categories)
        cat1 = channel.category

        categories[group_id]['channels'].append(
            {
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            }
        )
        # 查询二级和三级类别
        # 查询二级  parent_id = cat1.id
        # for cat2 in cat1.subs.all():
        for cat2 in GoodsCategory.objects.filter(parent_id=cat1.id).all():
            cat2.sub_cats = []
            categories[group_id]['sub_cats'].append(
                {
                    'id': cat2.id,
                    'name': cat2.name,
                    'sub_cats': cat2.sub_cats
                }
            )
            # for cat3 in cat2.subs.all()
            for cat3 in GoodsCategory.objects.filter(parent_id=cat2.id).all():
                cat2.sub_cats.append({
                    'id': cat3.id,
                    'name': cat3.name
                })

    return categories
