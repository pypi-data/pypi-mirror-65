import os
import tempfile
import agilicus
import yaml

from . import apps, context, files


def add(
    ctx,
    application,
    env_name,
    org_id=None,
    config_type=None,
    mount_src_path=None,
    username=None,
    password=None,
    share=None,
    domain=None,
    hostname=None,
    file_store_uri=None,
    filename=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    if filename:
        _file = files.upload(
            ctx,
            filename,
            org_id=org_id,
            label=config_type,
            tag=env_name,
            name=os.path.basename(filename),
        )
        file_store_uri = f"/v1/files/{_file['id']}"

    app = apps.get_app(ctx, org_id, application, maintained=True)
    _config = agilicus.EnvironmentConfig(
        maintenance_org_id=org_id,
        config_type=config_type,
        file_store_uri=file_store_uri,
        mount_src_path=mount_src_path,
        mount_username=username,
        mount_password=password,
        mount_share=share,
        mount_domain=domain,
        mount_hostname=hostname,
        **kwargs,
    )
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.application_api.env_config_post(app["id"], env_name, _config)


def update(
    ctx,
    application,
    env_name,
    id,
    org_id=None,
    config_type=None,
    mount_path=None,
    file_store_uri=None,
    **kwargs,
):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = apps.get_app(ctx, org_id, application, maintained=True)

    apiclient = context.get_apiclient(ctx, token)
    _config = apiclient.application_api.env_config_get(
        app["id"], env_name, id, maintenance_org_id=org_id
    )

    _update = agilicus.EnvironmentConfig(
        maintenance_org_id=org_id,
        mount_path=_config.mount_path,
        config_type=_config.config_type,
        file_store_uri=_config.file_store_uri,
    )

    if mount_path:
        _update.mount_path = mount_path

    if config_type:
        _update.config_type = config_type

    if file_store_uri:
        _update.file_store_uri = file_store_uri

    return apiclient.application_api.env_config_put(app["id"], env_name, id, _update)


def delete(ctx, application, env_name, id, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = apps.get_app(ctx, org_id, application, maintained=True)
    apiclient = context.get_apiclient(ctx, token)

    _config = apiclient.application_api.env_config_get(
        app["id"], env_name, id, maintenance_org_id=org_id
    )

    file_id = os.path.basename(_config.file_store_uri)
    try:
        files.delete(ctx, file_id, org_id=org_id, _continue_on_error=True)
    except Exception:
        print(f"Failed to delete the {_config.file_store_uri}")

    return apiclient.application_api.env_config_delete(app["id"], env_name, id, org_id)


def query(ctx, application, env_name, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    app = apps.get_app(ctx, org_id, application, maintained=True)

    apiclient = context.get_apiclient(ctx, token)
    return apiclient.application_api.env_config_get_all(app["id"], env_name, org_id)


class EnvVarConfigObj:
    def __init__(self, ctx, application, env_name, org_id=None, secret=False):
        self.ctx = ctx
        self.application = application
        self.env_name = env_name
        self.org_id = org_id
        if secret:
            self.env_file = "secret-env.yaml"
            self.config_type = "SECRET_ENV"
        else:
            self.env_file = "config-env.yaml"
            self.config_type = "CONFIGMAP_ENV"
        self.env_config = None
        self.data = {}
        self.build_env_list()

    def get_env_list(self):
        return self.data

    def build_env_list(self):
        configs = query(self.ctx, self.application, self.env_name, self.org_id)
        for config in configs:
            if config.config_type == self.config_type:
                with tempfile.TemporaryDirectory() as tempdir:
                    destination = os.path.join(tempdir, self.env_file)
                    files.download(
                        self.ctx,
                        os.path.basename(config.file_store_uri),
                        org_id=self.org_id,
                        destination=destination,
                    )
                    with open(destination) as stream:
                        self.data = yaml.safe_load(stream)
                self.env_config = config
                return

    def write_env_list(self, data):
        self.data.update(data)
        with tempfile.TemporaryDirectory() as tempdir:
            destination = os.path.join(tempdir, self.env_file)
            with open(destination, "w") as outfile:
                yaml.dump(self.data, outfile, default_flow_style=False)

            if self.env_config:
                # delete the old config
                delete(
                    self.ctx,
                    self.application,
                    self.env_name,
                    self.env_config.id,
                    self.org_id,
                )
            self.env_config = add(
                self.ctx,
                self.application,
                self.env_name,
                org_id=self.org_id,
                config_type=self.config_type,
                filename=destination,
            )

    def add_env_var(self, name, value):
        data = {}
        data[name] = value

        self.write_env_list(data)

    def del_env_var(self, name):
        data = self.get_env_list()
        for key in list(data.keys()):
            if key == name:
                del data[key]
        self.data = data
        self.write_env_list(data)
