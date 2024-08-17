box.schema.space.create('kv_storege', {
    if_not_exists = true
})

box.space.kv_storege:format({
    {name = 'key', type = 'string'},
    {name = 'value', type = '*'}
})

box.space.kv_storege:create_index('primary', {
    parts = {'key'},
    if_not_exists = true
})