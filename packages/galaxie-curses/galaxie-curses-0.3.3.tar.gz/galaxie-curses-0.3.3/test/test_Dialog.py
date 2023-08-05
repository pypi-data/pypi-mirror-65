import unittest

import GLXCurses

class TestDialog(unittest.TestCase):
    def test__buttons_list(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(type(dialog._action_area), list)
        dialog._action_area = None
        self.assertEqual([], dialog._action_area)
        list_of_test = [
            'Hello',
            42
        ]
        dialog._action_area = list_of_test
        self.assertEqual(dialog._action_area, list_of_test)
        self.assertRaises(TypeError, setattr, dialog, '_action_area', 42)

    # Style Property
    def test_action_aera_border(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(0, dialog.action_aera_border)
        dialog.action_aera_border = 42
        self.assertEqual(42, dialog.action_aera_border)
        dialog.action_aera_border = 5
        self.assertEqual(5, dialog.action_aera_border)
        self.assertRaises(TypeError, setattr, dialog, 'action_aera_border', 'Hello.42')
        self.assertRaises(ValueError, setattr, dialog, 'action_aera_border', -42)

    def test_button_spacing(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(6, dialog.button_spacing)
        dialog.button_spacing = 42
        self.assertEqual(42, dialog.button_spacing)
        dialog.button_spacing = 5
        self.assertEqual(5, dialog.button_spacing)
        self.assertRaises(TypeError, setattr, dialog, 'button_spacing', 'Hello.42')
        self.assertRaises(ValueError, setattr, dialog, 'button_spacing', -42)

    def test_content_area_border(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(2, dialog.content_area_border)
        dialog.content_area_border = 42
        self.assertEqual(42, dialog.content_area_border)
        dialog.content_area_border = 5
        self.assertEqual(5, dialog.content_area_border)
        self.assertRaises(TypeError, setattr, dialog, 'content_area_border', 'Hello.42')
        self.assertRaises(ValueError, setattr, dialog, 'content_area_border', -42)

    def test_content_area_spacing(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(0, dialog.content_area_spacing)
        dialog.content_area_spacing = 42
        self.assertEqual(42, dialog.content_area_spacing)
        dialog.content_area_spacing = 5
        self.assertEqual(5, dialog.content_area_spacing)
        self.assertRaises(TypeError, setattr, dialog, 'content_area_spacing', 'Hello.42')
        self.assertRaises(ValueError, setattr, dialog, 'content_area_spacing', -42)

    # Function
    def test_new(self):
        dialog1 = GLXCurses.Dialog().new()
        dialog2 = GLXCurses.Dialog()
        self.assertNotEqual(dialog1, dialog2)

    def test_new_with_buttons(self):
        dialog = GLXCurses.Dialog()
        dialog2 = GLXCurses.Dialog()
        dialog.new_with_buttons(
            'Message',
            dialog2,
            'Hello.42', '42',
            'Hello.43', '43'
        )

        self.assertEqual('Hello.42', dialog.get_action_area()[0].widget.text)
        self.assertEqual('42', dialog.get_action_area()[0].id)

        self.assertEqual('Hello.43', dialog.get_action_area()[1].widget.text)
        self.assertEqual('43', dialog.get_action_area()[1].id)

        self.assertEqual('Message', dialog.title)
        self.assertEqual(dialog2, dialog.parent)

    def test_response(self):
        dialog = GLXCurses.Dialog()
        GLXCurses.Application().add_window(dialog)
        dialog.response(response_id='42')

    def test_add_button(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(GLXCurses.Button, type(dialog.add_button(button_text='Hello', response_id='42')))
        dialog._action_area = None
        dialog.add_button(button_text='Hello.42', response_id='42')
        dialog.add_button(button_text='Hello.43', response_id='43')
        dialog.add_button(button_text='Hello.44', response_id='44')
        self.assertEqual(3, len(dialog.get_action_area()))

        self.assertEqual('Hello.42', dialog.get_action_area()[0].widget.text)
        self.assertEqual('42', dialog.get_action_area()[0].id)

        self.assertEqual('Hello.43', dialog.get_action_area()[1].widget.text)
        self.assertEqual('43', dialog.get_action_area()[1].id)

        self.assertEqual('Hello.44', dialog.get_action_area()[2].widget.text)
        self.assertEqual('44', dialog.get_action_area()[2].id)

    def test_add_buttons(self):
        dialog = GLXCurses.Dialog()
        self.assertEqual(GLXCurses.Button, type(dialog.add_button(button_text='Hello', response_id='42')))
        dialog._action_area = None
        dialog.add_buttons('Hello.42', '42', 'Hello.43', '43', 'Hello.44', '44')
        self.assertEqual(3, len(dialog.get_action_area()))

        self.assertEqual('Hello.42', dialog.get_action_area()[0].widget.text)
        self.assertEqual('42', dialog.get_action_area()[0].id)

        self.assertEqual('Hello.43', dialog.get_action_area()[1].widget.text)
        self.assertEqual('43', dialog.get_action_area()[1].id)

        self.assertEqual('Hello.44', dialog.get_action_area()[2].widget.text)
        self.assertEqual('44', dialog.get_action_area()[2].id)

    def test_add_action_widget(self):
        dialog = GLXCurses.Dialog()
        button1 = GLXCurses.Button()
        button1.text = 'Hello.42'
        dialog.add_action_widget(child=button1, response_id='42')
        self.assertEqual('Hello.42', dialog.get_action_area()[0].widget.text)
        self.assertEqual('42', dialog.get_action_area()[0].id)

        self.assertRaises(TypeError, setattr, dialog, 'add_action_widget', child=42, response_id=42)
        self.assertRaises(TypeError, setattr, dialog, 'add_action_widget', child=button1, response_id=button1)

    def test_set_default_response(self):
        dialog = GLXCurses.Dialog()
        dialog.add_buttons('Hello.42', '42', 'Hello.43', '43', 'Hello.44', '42', 'Hello.45', '45' )
        dialog.set_default_response('42')
        self.assertEqual(True, dialog.get_action_area()[-2].widget.has_default)
        self.assertEqual(dialog.get_action_area()[-2].widget, GLXCurses.Application().has_default.widget)

    def test_set_response_sensitive(self):
        dialog = GLXCurses.Dialog()
        dialog.add_buttons('Hello.42', '42', 'Hello.43', '43', 'Hello.44', '42')
        for button in dialog.get_action_area():
            if button.id == '42':
                self.assertEqual(True, button.widget.sensitive)

        dialog.set_response_sensitive(response_id='42', setting=False)
        for button in dialog.get_action_area():
            if button.id == '42':
                self.assertEqual(False, button.widget.sensitive)

        dialog.set_response_sensitive(response_id='42', setting=True)
        for button in dialog.get_action_area():
            if button.id == '42':
                self.assertEqual(True, button.widget.sensitive)

        self.assertRaises(TypeError, setattr, dialog, 'set_response_sensitive', response_id='Hello.42', setting=True)
        self.assertRaises(TypeError, setattr, dialog, 'set_response_sensitive', response_id=42, setting='Hello.42')

    def test_get_response_for_widget(self):
        dialog = GLXCurses.Dialog()
        dialog.add_buttons('Hello.42', '42', 'Hello.43', '43', 'Hello.44', '42')
        button = GLXCurses.Button()
        dialog.add_action_widget(child=button, response_id='45')
        self.assertEqual('45', button.id)
        self.assertEqual('45', dialog.get_response_for_widget(widget=button))

        dialog.get_action_area()[-1].id = GLXCurses.GLXC.RESPONSE_NONE
        self.assertEqual(GLXCurses.GLXC.RESPONSE_NONE, dialog.get_response_for_widget(widget=button))

        button2 = GLXCurses.Button()
        self.assertEqual(GLXCurses.GLXC.RESPONSE_NONE, dialog.get_response_for_widget(widget=button2))

        self.assertRaises(TypeError, dialog.get_response_for_widget, widget=42)

    def test_get_widget_for_response(self):
        app = GLXCurses.Application()
        dialog = GLXCurses.Dialog()
        button1 = GLXCurses.Button()
        button2 = GLXCurses.Button()
        dialog.add_action_widget(child=button1, response_id='42')
        dialog.add_action_widget(child=button2, response_id='43')
        self.assertEqual(button1, dialog.get_widget_for_response(response_id='42'))

        self.assertEqual(GLXCurses.GLXC.RESPONSE_NONE, dialog.get_widget_for_response(response_id='4242'))

        self.assertRaises(TypeError, dialog.get_response_for_widget, response_id=42)

    def test_get_action_area(self):
        dialog = GLXCurses.Dialog()
        dialog._action_area = ['42', '42']
        self.assertEqual(dialog._action_area, dialog.get_action_area())

    def test_get_content_area(self):

        dialog = GLXCurses.Dialog()

        self.assertEqual(GLXCurses.VBox, type(dialog.get_content_area()))


if __name__ == '__main__':
    unittest.main()
