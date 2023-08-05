# Toggle Admin (BETA 0.1)
> Модуль для выдачи прав администратора в беседах ВК.

С помощью «Toggle Admin» вы можете выдавать права администратора пользователям, не заходя в браузер. 
Это будет полезно для тех, кто большое количество времени сидит в ВК через мобильное устройство.

### Установка
1. Напрямую через GitHub (Архив):
<br>```pip install https://github.com/zpodushkin/toggle-admin/archive/master.zip --upgrade```

2. С помощью установщика pip из PyPi:
<br>```pip install toggle-admin```

### Пример использования
```python
from vkbottle.user import User, types
from vkbottle.rule import VBMLUserRule
from vkbottle import TaskManager
from toggle_admin import ToggleAdmin, ToggleAdminError

user = User(token="токен_от_вк")
admin = ToggleAdmin(login=7943343455, password="Balalaika31")
tm = TaskManager(user.loop)


@user.on.message_new(VBMLUserRule("!admin <uid:int>", lower=True))
async def set_admin(ans: types.Message, uid: int):
    try:
        await admin(ans.peer_id, uid, is_admin=True)
        await ans("Права администратора выданы!")
    except ToggleAdminError:
        await ans("Упс, произошла ошибочка...")


@user.on.message_new(VBMLUserRule("!unadmin <uid:int>", lower=True))
async def unset_admin(ans: types.Message, uid: int):
    try:
        await admin(ans.peer_id, uid, is_admin=False)
        await ans("Права администратора сняты!")
    except ToggleAdminError:
        await ans("Упс, произошла ошибочка...")


if __name__ == '__main__':
    tm.add_task(user.run())
    tm.run()
```

### Contributing
ПР поддерживаются! Мне приятно видеть ваш вклад в развитие модуля.
<br>Задавайте вопросы в блоке Issues и в [VK](https://vk.com/ovh_root)!

### Лицензия
Copyright © 2019-2020 [zpodushkin](https://github.com/zpodushkin).
<br>Этот проект имеет [GPL-3.0](https://github.com/zpodushkin/toggle-admin/blob/master/LICENSE) лицензию.