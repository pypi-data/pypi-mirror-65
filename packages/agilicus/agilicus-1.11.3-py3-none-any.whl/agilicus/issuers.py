from . import context
import agilicus


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    query_results = apiclient.issuers_api.issuers_query(**kwargs)
    if query_results:
        return query_results.issuers
    return None


def show(ctx, issuer_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.issuers_get(issuer_id, **kwargs).to_dict()


def add(ctx, issuer, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer_model = agilicus.Issuer(issuer=issuer, org_id=org_id)
    return apiclient.issuers_api.issuers_root_post(issuer_model).to_dict()


def delete(ctx, issuer_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.issuers_root_delete(issuer_id, **kwargs)


def query_clients(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    query_results = apiclient.issuers_api.clients_query(**kwargs)
    if query_results:
        return query_results.clients
    return None


def show_client(ctx, client_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.clients_get(client_id, **kwargs).to_dict()


def add_client(
    ctx,
    issuer_id,
    name,
    secret=None,
    application=None,
    org_id=None,
    redirects=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    client_model = agilicus.IssuerClient(
        issuer_id=issuer_id,
        name=name,
        application=application,
        org_id=org_id,
        secret=secret,
        redirects=redirects,
    )
    return apiclient.issuers_api.clients_post(client_model).to_dict()


def delete_client(ctx, client_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.clients_delete(client_id, **kwargs)


def add_redirect(ctx, client_id, redirect_url, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    client = apiclient.issuers_api.clients_get(client_id, **kwargs)
    if not client:
        print(f"Cannot find client {client_id}")
        return

    client.redirects.append(redirect_url)
    return apiclient.issuers_api.clients_put(client.id, client).to_dict()


def delete_redirect(ctx, client_id, redirect_url, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    client = apiclient.issuers_api.clients_get(client_id, **kwargs)
    if not client:
        print(f"Cannot find client {client_id}")
        return

    client.redirects.remove(redirect_url)
    return apiclient.issuers_api.clients_put(client.id, client).to_dict()
