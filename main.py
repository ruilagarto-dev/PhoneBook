from modules.logger import LogManager
from modules.View.view import PhoneBookView
from modules.Model.model import PhoneBookModel
from modules.controller import PhoneBookController

if __name__ == "__main__":
    logger = LogManager()
    
    model = PhoneBookModel(logger)
    view = PhoneBookView(logger)
    controller = PhoneBookController(logger, view, model)

    try:
        view.start()
    finally:
        model.close_database()

    
