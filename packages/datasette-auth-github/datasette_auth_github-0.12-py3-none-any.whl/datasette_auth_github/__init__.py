from datasette import hookimpl

from .github_auth import GitHubAuth


@hookimpl
def asgi_wrapper(datasette):
    config = datasette.plugin_config("datasette-auth-github") or {}
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")
    disable_auto_login = bool(config.get("disable_auto_login"))
    allow_users = config.get("allow_users")
    allow_orgs = config.get("allow_orgs")
    allow_teams = config.get("allow_teams")
    cookie_ttl = config.get("cookie_ttl") or 60 * 60
    cookie_version = config.get("cookie_version")

    # require_auth defaults to True unless set otherwise
    require_auth = True
    if "require_auth" in config:
        require_auth = config["require_auth"]

    def wrap_with_asgi_auth(app):
        if not (client_id and client_secret):
            return app

        return GitHubAuth(
            app,
            client_id=client_id,
            client_secret=client_secret,
            require_auth=require_auth,
            cookie_version=cookie_version,
            cookie_ttl=cookie_ttl,
            disable_auto_login=disable_auto_login,
            allow_users=allow_users,
            allow_orgs=allow_orgs,
            allow_teams=allow_teams,
            cacheable_prefixes=["/-/static/", "/-/static-plugins/"],
        )

    return wrap_with_asgi_auth


@hookimpl
def extra_template_vars(request):
    return {"auth": request.scope.get("auth") if request else None}
