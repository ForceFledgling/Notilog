Если перед запуском билда забыли создать `.env` файл:

```
notilog % TAG=test ./scripts/build.sh 
WARN[0000] The "POSTGRES_USER" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_DB" variable is not set. Defaulting to a blank string. 
parsing docker-compose.yml: error while interpolating services.db.environment.[]: required variable POSTGRES_PASSWORD is missing a value: Variable not set
notilog % 
```