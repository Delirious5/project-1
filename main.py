import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from datetime import datetime
import csv
import os


class PizzaApp(App):
    def build(self):
        self.pizza_counts = {
            'Cheese': 0,
            'Tuna': 0,
            'Meat': 0,
            'Fantasia': 0
        }
        self.prices = {
            'Cheese': 5000,
            'Tuna': 5000,
            'Meat': 5000,
            'Fantasia': 5000
        }

        self.root = BoxLayout(orientation='vertical')

        self.pizza_labels = {}
        for pizza in self.pizza_counts:
            h_layout = BoxLayout(size_hint_y=None, height=50)
            label = Label(text=f'{pizza} Pizza: 0', font_size='20sp')
            self.pizza_labels[pizza] = label
            h_layout.add_widget(label)
            add_button = Button(text='+', font_size='20sp')
            add_button.bind(on_press=lambda instance, pizza=pizza: self.add_pizza(pizza))
            h_layout.add_widget(add_button)
            subtract_button = Button(text='-', font_size='20sp')
            subtract_button.bind(on_press=lambda instance, pizza=pizza: self.subtract_pizza(pizza))
            h_layout.add_widget(subtract_button)
            self.root.add_widget(h_layout)

        self.total_label = Label(text='Total: 0', font_size='20sp')
        self.root.add_widget(self.total_label)

        self.order_list = ScrollView(size_hint=(1, None), size=(400, 200))
        self.order_list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.order_list_layout.bind(minimum_height=self.order_list_layout.setter('height'))
        self.order_list.add_widget(self.order_list_layout)
        self.root.add_widget(self.order_list)

        self.notification_label = Label(text='', font_size='20sp', size_hint_y=None, height=50, opacity=0)
        self.root.add_widget(self.notification_label)

        self.button_layout = BoxLayout(size_hint_y=None, height=50)

        self.save_button = Button(text='Save', font_size='20sp')
        self.save_button.bind(on_press=self.save_orders)
        self.button_layout.add_widget(self.save_button)

        self.new_order_button = Button(text='New Order', font_size='20sp')
        self.new_order_button.bind(on_press=self.new_order)
        self.button_layout.add_widget(self.new_order_button)

        self.root.add_widget(self.button_layout)

        return self.root

    def add_pizza(self, pizza):
        self.pizza_counts[pizza] += 1
        self.update_labels()
        self.update_order_list()

    def subtract_pizza(self, pizza):
        if self.pizza_counts[pizza] > 0:
            self.pizza_counts[pizza] -= 1
        self.update_labels()
        self.update_order_list()

    def update_labels(self):
        total = 0
        for pizza, count in self.pizza_counts.items():
            self.pizza_labels[pizza].text = f'{pizza} Pizza: {count}'
            total += count * self.prices[pizza]
        self.total_label.text = f'Total: {total}'

    def update_order_list(self):
        self.order_list_layout.clear_widgets()
        for pizza, count in self.pizza_counts.items():
            if count > 0:
                order_label = Label(text=f'{pizza} Pizza: {count}', font_size='18sp', size_hint_y=None, height=30)
                self.order_list_layout.add_widget(order_label)

    def save_orders(self, instance):
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f'orders_{current_date}.csv'

        new_file = not os.path.exists(filename)

        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Date & Time', 'Pizza Type', 'Quantity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if new_file:
                writer.writeheader()

            for pizza, count in self.pizza_counts.items():
                if count > 0:
                    #writer.writerow({'Date & Time': datetime.now().strftime("%Y-%m-%d %H:%M"), 'Pizza Type': pizza,'Quantity': count})
                    writer.writerow({'Date & Time': datetime.now().strftime("%Y-%m-%d %H:%M"), 'Pizza Type': pizza,'Quantity': count, "Total": total})

        self.show_notification("Order Saved")

    def new_order(self, instance):
        for pizza in self.pizza_counts:
            self.pizza_counts[pizza] = 0
        self.update_labels()
        self.update_order_list()
        self.show_notification("New Order")

    def show_notification(self, message):
        self.notification_label.text = message
        anim = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim.start(self.notification_label)


if __name__ == '__main__':
    PizzaApp().run()
