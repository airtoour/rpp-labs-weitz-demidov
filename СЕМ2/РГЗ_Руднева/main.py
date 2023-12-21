from routes import * # Импорт всех модулей из файла routes для работы приложения

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
