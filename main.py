from typing import Any, Type, Union

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble


class Animal:

    name = None
    weight = None

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class NewAnimalCreator(ModalView):

    def __init__(self, master_grid: GridLayout, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(NewAnimalCreatorRoot(master_grid, self))


class NewAnimalCreatorGrid(GridLayout):

    cols = 2

    def __init__(self, master: GridLayout, modal: ModalView, **kwargs):
        super().__init__(**kwargs)

        self.master, self.modal = master, modal

        self.value_inputs: dict[str, TextInput] = {}

        for fieldname in Animal.__dict__:
            if not fieldname.startswith('__'):
                self.add_widget(label := Label(text=f"{fieldname} = "))
                self.add_widget(text_input := TextInput(multiline=False))
                self.value_inputs[fieldname] = text_input

        self.add_widget(button := Button(text='Save'))
        button.bind(on_press=self.save)
        self.add_widget(button := Button(text='Cancel'))
        button.bind(on_press=modal.dismiss)

    def save(self, arg: Any):
        new_animal: Type[Animal] = type(self.value_inputs['name'].text, (Animal,), {field: textinput.text for field, textinput in self.value_inputs.items()})
        self.master.animal_container.add_widget(AnimalType(new_animal))
        self.modal.dismiss()


class NewAnimalCreatorRoot(GridLayout):

    cols = 1

    def __init__(self, master: GridLayout, modal: ModalView) -> None:
        super().__init__()

        self.add_widget(Label(text='New Animal Creator', font_size=30))

        self.add_widget(NewAnimalCreatorGrid(master, modal, size_hint_y=0.2))


class AnimalContainer(GridLayout):

    cols = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #self.add_widget(button := Button(text='Create New Species'))
        #self.add_widget(button := Button(text='Spawn Animal'))


class AnimalType(GridLayout):

    cols = 1

    def __init__(self, animal: Type[Animal], **kwargs):
        super().__init__(**kwargs)

        self.add_widget(AnimalTypeHeader(animal))
        self.add_widget(AnimalList())


class AnimalTypeHeader(GridLayout):

    cols = 2

    def __init__(self, animal: Type[Animal], **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Label(text=animal.name))

        self.add_widget(Button(text=f"Add new {animal.name}"))


class AnimalList(GridLayout):
    pass


class RootGrid(GridLayout):

    cols = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(label := Label(text='Animal Farm', font_size=30, size_hint_y=0.3))

        self.add_widget(button := Button(text='Create New Species', size_hint_y=0.2))
        button.bind(on_press=lambda arg: NewAnimalCreator(self).open())

        self.animal_container = AnimalContainer()
        self.add_widget(self.animal_container)

        # self.add_widget(button := Button(text='Pause'))
        # #button.bind(on_press=lambda arg:)
        # self.add_widget(button := Button(text='Continue'))
        # #button.bind(on_press=test_func)
        # self.add_widget(button := Button(text='Toggle'))
        # #button.bind(on_press=test_func)
        # self.add_widget(button := Button(text='Stop'))
        # #button.bind(on_press=test_func)


class DemoGUI(App):

    def build(self):
        return RootGrid()


if __name__ == '__main__':
    DemoGUI().run()
