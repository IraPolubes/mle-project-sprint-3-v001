# Мониторинг
Смотрим метрики:
http://flat_predict_app:1702/metrics



После запуска dockr-compose сервисы находятся по следующим адресам после того как добавить в VisualStudio Code перенаправление портов 1702, 8081, 9090, 3000 через Ports в терминале:

Microservice: http://localhost:8081/docs
Prometheus metrics: http://localhost:9090/metrics
Prometheus UI: http://localhost:9090/
Grafana: http://localhost:3000/

## Для мониторинга выбраны метрики нескольких типов:

### Реальное время

### Инрфраструткурные


### Прикладные
