import anvil
from anvil.tables import app_tables
from kivy.core.window import Window
from kivy.uix.filechooser import platform
from kivy.uix.screenmanager import Screen, ScreenManager
import anvil.server
from kivy.lang import Builder
import anvil.server
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget

if platform == 'android':
    from kivy.uix.button import Button
    from kivy.uix.modalview import ModalView
    from kivy.clock import Clock
    from android import api_version, mActivity
    from android.permissions import (
        request_permissions, check_permission, Permission)

view_transaction_history = '''

<WindowManager>:
    TransactionBH:
    ViewProfileScreenBTH:

<TransactionBH>
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Transaction History"
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back_screen()]]
            right_action_items: [['refresh', lambda x: root.refresh()]]
            md_bg_color: 0.043, 0.145, 0.278, 1
        MDScrollView:

            MDList:
                id: container1


<ViewProfileScreenBTH>:
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "View Profile"
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.on_back_button_press()]]
            md_bg_color: 0.043, 0.145, 0.278, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                BoxLayout:
                    id: box1
                    orientation: 'vertical'
                    size_hint_y: None
                    MDLabel:
                        text: "Transaction details"
                        halign: "center"
                        bold: True
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(20)

                    BoxLayout:
                        id: box1
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(800)

                        padding: [10, 0,0,0]
                        canvas.before:
                            Color:
                                rgba: 0, 0, 0, 1  # Blue color for the box
                            Line:
                                rectangle: self.pos[0], self.pos[1], self.size[0], self.size[1]

                        MDGridLayout:
                            cols: 2
                            spacing: 5
                            MDLabel:
                                text: "Transaction ID"
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id : transaction_id
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "User Email" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: user_email
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "Receiver Email" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: receiver_email
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "Wallet ID" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: wallet_id
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "Transaction Type" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: transaction_type
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "Amount" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: vtamount
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"

                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "Date and Time" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: date_time
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"



                        MDGridLayout:
                            cols: 2
                            spacing: dp(10)
                            padding: dp(10)
                            MDLabel:
                                text: "status" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"
                                bold: True
                            MDLabel:
                                id: status
                                text: "" 
                                size_hint_y:None
                                height:dp(50)
                                halign: "left"

'''

Builder.load_string(view_transaction_history)
class TransactionBH(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        email = self.get_table()
        profile = app_tables.fin_user_profile.search()
        transaction = app_tables.fin_wallet_transactions.search()
        s = 0
        transaction_id = []
        wallet_customer_id = []
        for i in transaction:
            transaction_id.append(i['transaction_id'])
            wallet_customer_id.append(i['customer_id'])
        print(transaction_id)

        pro_customer_id = []
        pro_mobile_number = []
        pro_email_id = []
        borrower_name = []

        for i in profile:
            pro_customer_id.append(i['customer_id'])
            pro_mobile_number.append(i['mobile'])
            pro_email_id.append(i['email_user'])
            borrower_name.append(i['full_name'])

        index = -1
        if email in pro_email_id:
            index = pro_email_id.index(email)
        print(pro_customer_id[index])

        index_list = []

        for idx, val in enumerate(wallet_customer_id):
            if val == pro_customer_id[index]:
                index_list.append(idx)
        print(index_list)
        print(wallet_customer_id)

        b = 1
        k = -1
        for i in reversed(index_list):
            b += 1
            k += 1
            if wallet_customer_id[i] in pro_customer_id:
                number = pro_customer_id.index(wallet_customer_id[i])
            else:
                number = 0
            item = ThreeLineAvatarIconListItem(

                IconLeftWidget(
                    icon="card-account-details-outline"
                ),
                text=f"Borrower Name : {borrower_name[number]}",
                secondary_text=f"Borrower Mobile Number : {pro_mobile_number[number]}",
                tertiary_text=f"Transaction Name : {transaction_id[i]}",
                text_color=(0, 0, 0, 1),  # Black color
                theme_text_color='Custom',
                secondary_text_color=(0, 0, 0, 1),
                secondary_theme_text_color='Custom',
                tertiary_text_color=(0, 0, 0, 1),
                tertiary_theme_text_color='Custom'
            )
            item.bind(
                on_release=lambda instance, transactions_id=transaction_id[i]: self.icon_button_clicked(instance,
                                                                                                        transactions_id))
            self.ids.container1.add_widget(item)
        else:
            print("Index out of range!")

    def icon_button_clicked(self, instance, transactions_id):
        value = instance.text.split(':')
        value = value[-1][1:]
        data = app_tables.fin_foreclosure.search()
        sm = self.manager

        # Create a new instance of the LoginScreen
        profile = ViewProfileScreenBTH(name='ViewProfileScreenBTH')

        # Add the LoginScreen to the existing ScreenManager
        sm.add_widget(profile)

        # Switch to the LoginScreen
        sm.current = 'ViewProfileScreenBTH'
        self.manager.get_screen('ViewProfileScreenBTH').initialize_with_value(transactions_id, data)

    def on_pre_enter(self):
        # Bind the back button event to the on_back_button method
        Window.bind(on_keyboard=self.on_back_button)

    def on_pre_leave(self):
        # Unbind the back button event when leaving the screen
        Window.unbind(on_keyboard=self.on_back_button)

    def on_back_button(self, instance, key, scancode, codepoint, modifier):
        # Handle the back button event
        if key == 27:  # 27 is the keycode for the hardware back button on Android
            self.go_back_screen()
            return True  # Consume the event, preventing further handling
        return False  # Continue handling the event

    def go_back_screen(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'DashboardScreen'

    def refresh(self):
        self.ids.container1.clear_widgets()
        self.__init__()

    def get_table(self):
        # Make a call to the Anvil server function
        # Replace 'YourAnvilFunction' with the actual name of your Anvil server function
        return anvil.server.call('another_method')


    def on_back_button_press(self):
        self.manager.current = 'DashboardScreenLF'

class ViewProfileScreenBTH(Screen):
    def initialize_with_value(self, value, data):
        data = app_tables.fin_wallet_transactions.search()
        transaction_id = []
        user_email = []
        receiver_email = []
        wallet_id = []
        transaction_type = []
        amount = []
        date_time = []
        status = []
        for i in data:
            transaction_id.append(i['transaction_id'])
            user_email.append(i['user_email'])
            receiver_email.append(i['receiver_email'])
            wallet_id.append(i['wallet_id'])
            transaction_type.append(i['transaction_type'])
            amount.append(i['amount'])
            date_time.append(i['transaction_time_stamp'])
            status.append(i['status'])

        if value in transaction_id:
            index = transaction_id.index(value)
            self.ids.transaction_id.text = str(transaction_id[index])
            self.ids.user_email.text = str(user_email[index])
            self.ids.receiver_email.text = str(receiver_email[index])
            self.ids.wallet_id.text = str(wallet_id[index])
            self.ids.transaction_type.text = str(transaction_type[index])
            self.ids.vtamount.text = str(amount[index])
            self.ids.date_time.text = str(date_time[index])
            self.ids.status.text = str(status[index])


    def on_pre_enter(self):
        # Bind the back button event to the on_back_button method
        Window.bind(on_keyboard=self.on_back_button)

    def on_pre_leave(self):
        # Unbind the back button event when leaving the screen
        Window.unbind(on_keyboard=self.on_back_button)

    def on_back_button(self, instance, key, scancode, codepoint, modifier):
        # Handle the back button event
        if key == 27:  # 27 is the keycode for the hardware back button on Android
            self.on_back_button_press()
            return True  # Consume the event, preventing further handling
        return False  # Continue handling the event

    def on_back_button_press(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'TransactionBH'

class MyScreenManager(ScreenManager):
    pass





