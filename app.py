from services.facade.app_facade import AppFacade

app_facade = AppFacade()
app = app_facade.create_app()

if __name__ == '__main__':
    app.run(debug = True)
