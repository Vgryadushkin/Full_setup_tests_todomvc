from selene import have, command
from selene.support.shared import browser

completed = have.css_class('completed')

class TodoMVC:
    def __init__(self):
        self.todo_list = browser.all('#todo-list>li')

    def open(self):
        browser.open('https://todomvc4tasj.herokuapp.com/')
        app_loaded = "return $._data($('#clear-completed')[0], 'events')" \
                     ".hasOwnProperty('click')"
        browser.should(have.js_returned(True, app_loaded))
        return self

    def add(self, *todos: str):
        for todo in todos:
            browser.element('#new-todo').type(todo).press_enter()
        return self

    def given_opened(self, *todos: str):
        self.open()
        self.add(*todos)

    def should_be(self, *todos: str):
        self.todo_list.should(have.exact_texts(*todos))
        return self

    def start_editing(self, todo, new_text):
        self.todo_list.element_by(have.exact_text(todo)).double_click()
        return self.todo_list.element_by(have.css_class('editing')).element('.edit').perform(
            command.js.set_value(new_text))

    def edit(self, todo, new_text):
        self.start_editing(todo, new_text).press_enter()
        return self

    def edit_by_focus_change(self, todo, new_text):
        self.start_editing(todo, new_text).press_tab()
        return self

    def cancel_edit(self, todo: str, new_text):
        self.start_editing(todo, new_text).press_escape()

    def toggle(self, todo: str):
        self.todo_list.element_by(have.exact_text(todo)) \
            .element('.toggle').click()
        return self

    def toggle_all(self):
        browser.element('#toggle-all').click()
        return self

    def should_be_completed(self, *todos: str):
        self.todo_list.filtered_by(completed) \
            .should(have.exact_texts(*todos))
        return self

    def should_be_active(self, *todos: str):
        self.todo_list.filtered_by(completed.not_) \
            .should(have.exact_texts(*todos))
        return self

    def clear_completed(self):
        browser.element('#clear-completed').click()
        return self

    def delete(self, todo: str):
        self.todo_list.element_by(have.exact_text(todo)) \
            .hover().element('.destroy').click()
        return self

    def should_be_items_left(self, count: int):
        browser.element('#todo-count strong') \
            .should(have.exact_text(str(count)))
        return self

    def should_be_empty(self):
        self.todo_list.should(have.size(0))
