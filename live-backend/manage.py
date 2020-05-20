from app import create_app
from app import db

# from app import blueprint

app = create_app('dev')
# region.init_app(app)


# app.register_blueprint(blueprint)
# app.app_context().push()
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)


# @manager.command
# def run():
#     app.run(host='0.0.0.0')


if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host='0.0.0.0', port=5001)

    # from app.supplier_apis.emsai import search
    # import json
    #
    # supplier_number = "70330"
    # supplier_article_number = "P5555-ND"
    # search_data = search(supplier_number=supplier_number, supplier_article_number=supplier_article_number)
    # print(search_data)
    # search_data = json.loads(search_data)
