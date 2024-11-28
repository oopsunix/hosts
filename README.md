# Hosts

使用 GitHub Actions 每天定时更新hosts解析，解决GitHub、Steam、TMDB、Google Translate、wallhaven访问问题

## 最新hosts解析

- ALL: `https://raw.githubusercontent.com/oopsunix/hosts/main/hosts`
- Github: `https://raw.githubusercontent.com/oopsunix/hosts/main/hosts_github`
- Google Translate: `https://raw.githubusercontent.com/oopsunix/hosts/main/hosts_google_translate`
- Steam: `https://raw.githubusercontent.com/oopsunix/hosts/main/hosts_steam`
- TMDB: `https://raw.githubusercontent.com/oopsunix/hosts/main/hosts_tmdb`
- wallhaven: `https://raw.githubusercontent.com/oopsunix/hosts/main/hosts_wallhaven`


## 修改hosts文件
复制 hosts 文本 -> 将复制的文本粘贴至系统 hosts 文件

- Windows

```
C:\Windows\System32\drivers\etc\hosts
```

- Linux/macOS

```
/etc/hosts
```

## 刷新生效
- Windows

```
ipconfig /flushdns
```

- Linux

```
/etc/init.d/network restart
```

- macOS

```
sudo killall -HUP mDNSResponder
```


