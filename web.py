from flask import Flask, render_template, request
from learning_controller import LearningController
from admin_controller import AdminController

app = Flask(__name__)


@app.route('/')
def home():
    """
    Creates a home page.
    """
    return render_template('index.html')


@app.route('/administration/')
def administration():
    """
    Manages administration of MY VOCABULARY.
    :return: render_template
    """

    admin_controller = AdminController(request)
    admin_controller.handle_admin_controller()

    return admin_controller.prepare_render_template()


@app.route('/learning')
def learning():
    """
    Manages the process of learning.
    :return: render_template
    """

    learning_controller = LearningController(request)
    learning_controller.handle_learning_controller()

    return learning_controller.prepare_render_template()


# Run the application if executed as main package
if __name__ == '__main__':
    # Run in debug mode
    app.run(debug=True, host='0.0.0.0')
