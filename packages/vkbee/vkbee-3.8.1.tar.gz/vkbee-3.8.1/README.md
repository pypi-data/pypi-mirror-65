<head>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
</head>

![vkbee](https://github.com/asyncvk/vkbee/blob/master/vkbee/bgtio.png?raw=true)

[Documentation](https://asyncvk.github.io)

[Example Bot](https://pastebin.com/raw/hxhXPyb9)

[VK](https://vk.me/join/AJQ1d0zSjRa17i3RkVt3m5KH)

<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-%23FFD242?logo=python&logoColor=white">
    <img alt="Downloads" src="https://pepy.tech/badge/vkbee">
</p>




# vkbee

## Ultra-Fast speed by uvloop

<p>You need add definer in your code</p>

```python
uvspeed = True
import vkbee
```

## Установка
```bash
pip3 install vkbee
```
## Установка стабилного лонгпула
```bash
pip3 install vkbee==1.6
```


Simple Async VKLibrary faster than vk_api
# Пример работы
```python
import asyncio
import vkbee

async def main(loop):
    token = "сюдатокен"
    vk_s = vkbee.VkApi(token, loop=loop)
    vk = vk_s.get_api()
    await vk_s.messages.send(
        chat_id=1,
        message='VKBEE',
        random_id=0
    )
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```



