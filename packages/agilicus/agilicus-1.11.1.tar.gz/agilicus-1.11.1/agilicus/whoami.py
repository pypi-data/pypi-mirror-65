from . import access, context


def whoami(ctx, refresh, **kwargs):
    token = context.get_token(ctx)
    if not token:
        token = access.get_access_token(ctx, refresh).get()
    return token
