import json
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from .models import Application, Activity, ActivityReminder

@receiver(post_save, sender=Application)
def notify_application_change(sender, instance, created, **kwargs):
    """
    Отправляет уведомление PostgreSQL при создании или обновлении заявки.
    """
    channel = 'application_updates'  # Имя канала для NOTIFY

    # Формируем полезную нагрузку (payload)
    # Вы можете добавить больше полей, если это необходимо
    payload_data = {
        'id': instance.id,
        'user_id': instance.user_id,
        'status': instance.status,
        'hr_comment': instance.hr_comment,
        'job_id': instance.job_id if instance.job else None,
        'activity_id': instance.activity_id if instance.activity else None,
        'is_created': created  # True если объект был создан, False если обновлен
    }
    payload_json = json.dumps(payload_data, default=str)

    try:
        with connection.cursor() as cursor:
            # Экранируем одинарные кавычки в JSON, если они там могут быть, 
            # хотя json.dumps обычно этого избегает для ключей и стандартных значений.
            # Более надежный способ - использовать параметры SQL, но для NOTIFY это сложнее.
            # Однако, json.dumps должен создавать валидный JSON, который не должен ломать SQL-строку,
            # если только в самих данных нет очень специфических символов.
            # Для большей безопасности можно было бы использовать $$ для обрамления строки в PostgreSQL.
            sql_command = f"NOTIFY {channel}, '{payload_json.replace("'", "''")}';"
            cursor.execute(sql_command)
        print(f"Sent NOTIFY on channel '{channel}' for Application ID {instance.id}")
    except Exception as e:
        # В реальном приложении здесь стоит использовать логирование
        print(f"Error sending NOTIFY for Application ID {instance.id}: {e}") 

@receiver(post_save, sender=Activity)
def notify_activity_change(sender, instance, created, **kwargs):
    """
    Отправляет уведомление PostgreSQL при создании или обновлении активности.
    Также обновляет время отправки напоминаний, если время начала активности изменилось.
    """
    # Часть 1: Обновление напоминаний, если start_time изменилось
    if not created:  # Только при обновлении активности
        update_fields = kwargs.get('update_fields')
        start_time_may_have_changed = False
        if update_fields is None:  # Полное сохранение, предполагаем, что могло измениться
            start_time_may_have_changed = True
        elif 'start_time' in update_fields: # Явно обновлялось
            start_time_may_have_changed = True

        if start_time_may_have_changed and instance.start_time:
            new_target_reminder_sent_at = instance.start_time - timedelta(hours=24)
            
            reminders_for_activity = ActivityReminder.objects.filter(activity=instance)
            for reminder in reminders_for_activity:
                # Проверяем, нужно ли действительно обновлять, чтобы избежать лишних записей в БД,
                # если время уже корректно или это напоминание другого типа (например, за 1 час)
                # Пока что обновляем все напоминания для этой активности, предполагая, что все они должны быть за 24 часа.
                # В будущем можно добавить проверку reminder.reminder_type == '24h_before' или подобное.
                if reminder.sent_at != new_target_reminder_sent_at:
                    reminder.sent_at = new_target_reminder_sent_at
                    reminder.save(update_fields=['sent_at']) # Сохраняем только измененное поле
                    print(f"Updated ActivityReminder ID {reminder.id} sent_at to {new_target_reminder_sent_at} for Activity ID {instance.id}")

    # Часть 2: Отправка NOTIFY (существующая логика)
    channel = 'activity_updates'  # Имя канала для NOTIFY для активностей

    payload_data = {
        'id': instance.id,
        'title': instance.title,
        'start_time': instance.start_time.isoformat() if instance.start_time else None,
        'end_time': instance.end_time.isoformat() if instance.end_time else None,
        'is_active': instance.is_active,
        'is_created': created
    }
    payload_json = json.dumps(payload_data, default=str)

    try:
        with connection.cursor() as cursor:
            sql_command = f"NOTIFY {channel}, '{payload_json.replace("'", "''")}';"
            cursor.execute(sql_command)
        print(f"Sent NOTIFY on channel '{channel}' for Activity ID {instance.id}")
    except Exception as e:
        print(f"Error sending NOTIFY for Activity ID {instance.id}: {e}") 
