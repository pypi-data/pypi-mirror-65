from . import access, context
import agilicus


def query(ctx):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.issuers_query()


def add(ctx, issuer, **kwargs):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()
    apiclient = context.get_apiclient(ctx, token)
    issuer_model = agilicus.Issuer(issuer=issuer)
    return apiclient.issuers_api.issuers_post(issuer_model).to_dict()


def add_client(
    ctx, issuer_id, name, secret=None, application=None, org_id=None, **kwargs
):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()
    apiclient = context.get_apiclient(ctx, token)
    client_model = agilicus.IssuerClient(
        name=name, application=application, org_id=org_id, secret=secret
    )
    return apiclient.issuers_api.clients_post(issuer_id, client_model).to_dict()


def _get_client(issuer, client_name):
    for client in issuer.clients:
        if client.name == client_name:
            return client


def _get_redirect(client, redirect_url):
    for redirect in client.redirects:
        if redirect.redirect_url == redirect_url:
            return redirect


def add_redirect(ctx, issuer_id, client_name, redirect_url, **kwargs):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()
    apiclient = context.get_apiclient(ctx, token)

    issuer = apiclient.issuers_api.issuers_get(issuer_id)
    client = _get_client(issuer, client_name)
    if not client:
        print(f"Cannot find client {client_name}")
        return

    redirect_model = agilicus.IssuerClientRedirect(redirect_url=redirect_url)
    return apiclient.issuers_api.redirects_post(
        issuer_id, client.id, redirect_model
    ).to_dict()


def delete_redirect(ctx, issuer_id, client_name, redirect_url, **kwargs):
    token = context.get_token(ctx)
    if not token:
        access_token = access.get_access_token(ctx)
        token = access_token.get()
    apiclient = context.get_apiclient(ctx, token)

    issuer = apiclient.issuers_api.issuers_get(issuer_id)
    client = _get_client(issuer, client_name)
    if not client:
        print(f"Cannot find client {client_name}")
        return

    redirect = _get_redirect(client, redirect_url)
    if not redirect:
        print(f"Cannot find redirect {redirect_url}")
        return

    return apiclient.issuers_api.redirects_delete(issuer_id, client.id, redirect.id)
