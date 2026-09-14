# -*- coding: utf-8 -*-
"""deepskins.proxy —— 自动探测本机代理, 并把它交给 git / pip 子进程。

为什么需要:
    * git 读 **Windows 系统代理**(注册表 Internet Settings), 所以桌面代理软件一开
      (Clash / verge / v2ray …) git 就能用, `deepskins install` 看着像"没问题";
    * pip 与 Python 的 requests **故意不读注册表**, 只看 HTTP_PROXY / HTTPS_PROXY
      环境变量。桌面代理软件默认通常不写这两个变量 —— 于是 pip 直连 pypi.org,
      在受限网络下就报 SSL UNEXPECTED_EOF / Read timed out。
    本模块把"探测到的代理"显式喂给这两条通道, 用户不必自己配环境变量。

探测顺序:
    1. 环境变量 HTTP_PROXY / HTTPS_PROXY / ALL_PROXY(以及小写形式) —— 尊重用户设置;
    2. Windows 注册表 Internet Settings 的 ProxyServer(系统代理);
    3. 本机常见代理端口探测(127.0.0.1:7897/7890/10809/…)。

关闭方式: 设 DEEPSKINS_NO_PROXY=1; 或显式指定 DEEPSKINS_PROXY=http://host:port。
"""
import os
import socket
import subprocess
import sys

# 常见桌面代理软件默认监听端口
COMMON_PORTS = (7897, 7890, 7891, 10809, 10808, 1080, 8888, 2080, 20171)
PROBE_TIMEOUT = 0.35

_cached = None
_cached_source = None
# 记住"用户是否显式指定过", 便于诊断输出
EXPLICIT = ("DEEPSKINS_PROXY",)

ENV_KEYS = ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy")


def _disabled():
    v = os.environ.get("DEEPSKINS_NO_PROXY", "").strip().lower()
    return v not in ("", "0", "false", "no")


def _normalize(value):
    """统一成 http://host:port 形式; 兼容 localhost:7897 / 127.0.0.1:7897。"""
    if not value:
        return None
    v = value.strip().strip('"').strip("'")
    if not v:
        return None
    if "://" not in v:
        v = "http://" + v
    # 去掉可能的结尾斜杠
    return v.rstrip("/")


def _split_bypass():
    raw = os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or ""
    return [p.strip() for p in raw.split(",") if p.strip()]


def _from_env():
    for k in ENV_KEYS:
        v = os.environ.get(k)
        if v:
            return _normalize(v), "环境变量 %s" % k
    return None, None


def _from_override():
    v = os.environ.get("DEEPSKINS_PROXY")
    if v:
        return _normalize(v), "DEEPSKINS_PROXY"
    return None, None


def _from_windows_registry():
    """读 Windows 系统代理(HKCU Internet Settings), 仅在 ProxyEnable=1 时生效。"""
    if sys.platform != "win32":
        return None, None
    try:
        import winreg  # noqa: WPS433 (仅 Windows 可用)
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        try:
            enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            server, _ = winreg.QueryValueEx(key, "ProxyServer")
        finally:
            winreg.CloseKey(key)
        if not enable or not server:
            return None, None
        server = str(server)
        # 形如 "host:port" 或 "http=host:port;https=host:port"
        if "=" in server:
            parts = dict(
                p.split("=", 1) for p in server.split(";") if "=" in p)
            server = parts.get("https") or parts.get("http") or ""
        return (_normalize(server), "Windows 系统代理(注册表)") if server else (None, None)
    except Exception:
        return None, None


def _port_open(port, host="127.0.0.1"):
    try:
        with socket.create_connection((host, port), timeout=PROBE_TIMEOUT):
            return True
    except OSError:
        return False


def _from_local_ports():
    for port in COMMON_PORTS:
        if _port_open(port):
            return "http://127.0.0.1:%d" % port, "本机端口探测(%d 在监听)" % port
    return None, None


def detect(force=False):
    """返回 (proxy_url 或 None, 来源说明 或 None)。结果会缓存。"""
    global _cached, _cached_source
    if _cached is not None and not force:
        return _cached, _cached_source
    if _disabled():
        _cached, _cached_source = None, "已由 DEEPSKINS_NO_PROXY 关闭"
        return _cached, _cached_source

    for finder in (_from_override, _from_env, _from_windows_registry, _from_local_ports):
        url, source = finder()
        if url:
            _cached, _cached_source = url, source
            return _cached, _cached_source

    _cached, _cached_source = None, "未探测到代理"
    return _cached, _cached_source


def env_with_proxy(base=None):
    """返回一份带代理环境变量的副本, 供 pip 等"只认环境变量"的程序使用。"""
    env = dict(base if base is not None else os.environ)
    url, _ = detect()
    if url:
        env["HTTP_PROXY"] = url
        env["HTTPS_PROXY"] = url
        env["http_proxy"] = url
        env["https_proxy"] = url
    return env


def pip_args():
    """给 pip 命令追加的参数(pip 自己也会读环境变量, 这里再显式传一次更稳)。"""
    url, _ = detect()
    return ["--proxy", url] if url else []


def git_config_args():
    """给 git 命令追加的 -c 参数。

    只有"探测到代理、且用户 git 全局没配代理"时才注入 —— 免得覆盖用户自己的配置。
    """
    url, _ = detect()
    if not url:
        return []
    configured = ""
    try:
        configured = subprocess.run(
            ["git", "config", "--global", "--get", "http.proxy"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            timeout=10, text=True).stdout.strip()
    except Exception:
        configured = ""
    if configured:
        return []
    return ["-c", "http.proxy=%s" % url, "-c", "https.proxy=%s" % url]


def describe():
    """给 doctor 用的一行摘要。"""
    url, source = detect(force=True)
    if url:
        return "代理: %s  (来源: %s)" % (url, source)
    return "代理: 未探测到  (%s)" % (source or "无")
