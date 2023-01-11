<h1>Бот для учёта личных расходов</h1>
<p>Установите <code>Docker, Docker-compose</code></p>
<p>Отредактируйте файл <code>db_method.py</code>:</p>
<p>Измените переменные <code>db_name</code> и <code>password</code> на необходимые имя и пароль.</p>
<p>Отредактируйте <code>.yml</code> файл, добавив переменные <code>BOT_TOKEN</code> и <code>TELEGRAM_ACCESS</code>,</p>
<p>так же добавьте переменные из файла <code>db_method</code> в 
<p><code>environment:
      POSTGRES_DB: name_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password</code></p>
<p>Первый запуск <code>docker-compose up -d --build</code></p>
<p>Последующий запуск <code>docker-compose up -d</code></p>
<p>Остановить <code>docker-compose down</code></p>
   
