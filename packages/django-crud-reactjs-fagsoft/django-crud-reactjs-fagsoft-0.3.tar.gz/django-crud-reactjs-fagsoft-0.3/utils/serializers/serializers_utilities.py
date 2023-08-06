class CustomSerializerMixin(object):
    def __init__(self, instance=None, *args, **kwargs):
        context = kwargs.get('context', None)
        if context:
            fields_to_removel = context.get('remove_fields', None)
            if fields_to_removel:
                existing = set(self.fields.keys())
                for field_name in fields_to_removel:
                    if field_name in existing:
                        self.fields.pop(field_name)
        super().__init__(instance, *args, **kwargs)
