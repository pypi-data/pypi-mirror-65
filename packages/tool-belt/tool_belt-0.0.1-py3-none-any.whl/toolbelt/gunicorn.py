from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def __init__(self, app, host: str, port: int, number_of_workers: int):
        self._options = {
            "bind": f"{host}:{port}",
            "workers": number_of_workers
        }

        self.application = app

        super().__init__()

    def init(self, parser, opts, args):
        raise NotImplementedError()

    def load_config(self):
        for key, value in self._options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

# Other options
# backlog: int = 2048
# max_requests: int = 0
# timeout: int = 30
# graceful_timeout: int = 30

# Security
# 'limit_request_line'
# 'limit_request_fields'
# 'limit_request_field_size'

# Hooks (function)
# 'on_starting'
# 'on_reload'
# 'when_ready'
# 'pre_fork'
# 'post_fork'
# 'post_worker_init'
# 'worker_int'
# 'worker_abort'
# 'pre_exec'
# 'pre_request'
# 'post_request'
# 'child_exit'
# 'worker_exit'
# 'nworkers_changed'
# 'on_exit'

# Logging
# 'accesslog',
# 'disable_redirect_access_to_syslog'
# 'access_log_format'
# 'errorlog'
# 'loglevel'
# 'capture_output'
# 'logger_class',
# 'logconfig'
# 'logconfig_dict'
# 'syslog_addr'
# 'syslog'
# 'syslog_prefix'
# 'syslog_facility'
# 'enable_stdio_inheritance'
# 'statsd_host'
# 'dogstatsd_tags'
# 'statsd_prefix'

# Debugging
# 'reload'
# 'reload_engine'
# 'reload_extra_files'
# 'spew'
# 'check_config'

# Server Mechanics
# 'preload_app'
# 'sendfile'
# 'reuse_port'
# 'chdir'
# 'daemon'
# 'raw_env'
# 'pidfile'
# 'worker_tmp_dir'
# 'user'
# 'group'
# 'umask'
# 'initgroups'
# 'tmp_upload_dir'
# 'secure_scheme_headers'
# 'forwarded_allow_ips'
# 'pythonpath'
# 'paste'
# 'proxy_protocol'
# 'proxy_allow_ips'
# 'raw_paste_global_conf'
# 'strip_header_spaces'

# Worker Processes
# 'workers'
# 'worker_class'
# 'threads'
# 'worker_connections'
# 'max_requests'
# 'max_requests_jitter'
# 'timeout'
# 'graceful_timeout'
# 'keepalive'
