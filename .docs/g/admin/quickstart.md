Клонируем репозиторий:

```
% git clone https://github.com/ForceFledgling/notilog.git
```

Перемещаем .env-example в .end и меняем переменные.

Запускаем билд (запускается docker-compose.override.yml):

```
notilog % TAG=test ./scripts/build.sh      
[+] Building 2.3s (40/40) FINISHED
...
...
vladimir@MacBook-Pro-Vladimir-2 notilog %
```

Поднимаем контейнеры:

```
notilog % docker-compose up -d               
[+] Running 38/14
...
...
[+] Building 13.4s (40/40) FINISHED
...
...
[+] Running 10/10
 ✔ Network notilog_default          Created                                                                                                                                             
 ✔ Network notilog_traefik-public   Created                                                                                                                                             
 ✔ Volume "notilog_app-db-data"     Created                                                                                                                                             
 ✔ Container notilog-db-1           Healthy                                                                                                                                             
 ✔ Container notilog-mailcatcher-1  Started                                                                                                                                             
 ✔ Container notilog-proxy-1        Started                                                                                                                                             
 ✔ Container notilog-frontend-1     Started                                                                                                                                             
 ✔ Container notilog-prestart-1     Exited                                                                                                                                              
 ✔ Container notilog-adminer-1      Started                                                                                                                                             
 ✔ Container notilog-backend-1      Started                                                                                                                                             
notilog % 
```

Проверяем что все поднялось:

```
notilog % docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS                   PORTS                                            NAMES
de38d1c444ba   backend:latest           "fastapi run --reloa…"   7 minutes ago   Up 7 minutes (healthy)   0.0.0.0:8000->8000/tcp                           notilog-backend-1
72d77cfd0134   adminer                  "entrypoint.sh php -…"   7 minutes ago   Up 7 minutes             0.0.0.0:8080->8080/tcp                           notilog-adminer-1
f5c503a46ac6   postgres:12              "docker-entrypoint.s…"   7 minutes ago   Up 7 minutes (healthy)   0.0.0.0:5432->5432/tcp                           notilog-db-1
5fb54f770944   frontend:latest          "/docker-entrypoint.…"   7 minutes ago   Up 7 minutes             0.0.0.0:5173->80/tcp                             notilog-frontend-1
8ea0fec08d38   schickling/mailcatcher   "sh -c 'mailcatcher …"   7 minutes ago   Up 7 minutes             0.0.0.0:1025->1025/tcp, 0.0.0.0:1080->1080/tcp   notilog-mailcatcher-1
e0e310260714   traefik:3.0              "/entrypoint.sh --pr…"   7 minutes ago   Up 7 minutes             0.0.0.0:80->80/tcp, 0.0.0.0:8090->8080/tcp       notilog-proxy-1
notilog %
```

Проверяем доступность:

*   Фронтенд: http://localhost:5173
*   Бэкенд: http://localhost:8000/docs
*   Traefik: http://localhost:8090, http://localhost:80
*   Adminer: http://localhost:8080
*   MailCatcher: http://localhost:1080