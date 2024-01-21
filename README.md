## Контекст, для которого будем готовить метрики
Начальство требует, чтобы для мониторинга всегда был назначен как минимум один ответственный

## Проектирование exporter
В код была добавлена такая метрика roster_users_cnt, которая отвечает за кол-во пользователей (==дежурных) в списке.

Переменная увеличивается/уменьшается при добавлении/удалении пользователя из ростера.

---
Также я планировал добавить метрику api_response_lapse, но подключить метрику к мне так и не удалось
- все метрики oncall экспортируются из приложения notifier
  - входная точка src/oncall/bin/notifier.py
- ручки на rosters API (/api/v0/teams/{team}/rosters/{roster}/users) находятся в приложении api, которое не экспортирует метрики
- возникли сложности с тем, чтобы внедрить метрики в api 
  - кодовая база достаточно сложна, и времени на ресерч у меня не было

Насколько мне известно, SRE не обязан разбираться в кодовой базе так же хорошо, как и разработчики, ввиду разделения обязанностей.

Как SRE, чтобы внедрить новую метрику api_response_time в приложение, я бы поступил следующим образом
- Собрал бы встречу разработчиков и рассказал бы контекст
- Попросил бы их добавить эту метрику/попросил бы объяснить как это сделать
