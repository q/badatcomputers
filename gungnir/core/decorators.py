def order_fields(*field_list):
    def decorator(form):
        original_init = form.__init__
        def init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            for field in field_list[::-1]:
                self.fields.insert(0, field, self.fields.pop(field))
        form.__init__ = init
        return form
    return decorator