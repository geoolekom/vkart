def group_name_from_url(url):
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]

def get_goods(url):
    owner_name = group_name_from_url(url)
    owner_id = api.groups.getById(group_id=owner_name)[0]['id']
    return api.market.get(owner_id=-owner_id)
