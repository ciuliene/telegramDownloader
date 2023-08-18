from unittest import TestCase
from unittest.mock import patch
from src.menu import Menu

@patch("sys.stdin.fileno")
@patch('tty.setraw')
@patch('termios.tcsetattr')
@patch('termios.tcgetattr')
class TestMenu(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

    @patch("sys.stdout.write")
    @patch("sys.stdin.read")
    def test_getting_menu_selection_returns_first_option(self, mock_read, mock_write, *_):
        # Arrange
        options = ["Option 1", "Option 2", "Exit"]
        menu = Menu(options)
        commands = []
        mock_read.side_effect = commands + [chr(13)]

        # Act
        selection, index = menu.start_menu()

        # Assert
        self.assertEqual(selection, options[0])
        self.assertEqual(index, 0)
        self.assertEqual(mock_write.call_count, (((len(options)*2) * (len(commands)+1)) + 3))

    @patch("sys.stdout.write")
    @patch("sys.stdin.read")
    def test_getting_menu_selection_returns_second_choice(self, mock_read, mock_write, *_):
        # Arrange
        options = ["Option 1", "Option 2", "Exit"]
        menu = Menu(options)
        commands = [chr(66)]
        mock_read.side_effect = commands + [chr(13)]

        # Act
        selection, index = menu.start_menu()

        # Assert
        self.assertEqual(selection, options[1])
        self.assertEqual(index, 1)
        self.assertEqual(mock_write.call_count, (((len(options)*2) * (len(commands)+1)) + 3))


    @patch("sys.stdout.write")
    @patch("sys.stdin.read")
    def test_getting_menu_selection_returns_first_choice_after_some_movements(self, mock_read, mock_write, *_):
        # Arrange
        options = ["Option 1", "Option 2", "Exit"]
        menu = Menu(options)
        commands = [chr(66), chr(65)]
        mock_read.side_effect = commands + [chr(13)]

        # Act
        selection, index = menu.start_menu()

        # Assert
        self.assertEqual(selection, options[0])
        self.assertEqual(index, 0)
        self.assertEqual(mock_write.call_count, (((len(options)*2) * (len(commands)+1)) + 3))

    @patch("sys.stdout.write")
    @patch("sys.stdin.read")
    def test_exiting_menu_ends_execution(self, mock_read, *_):
        # Arrange
        options = ["Option 1", "Exit"]
        menu = Menu(options)
        commands = [chr(66)]
        mock_read.side_effect = commands + [chr(13)]

        # Arrange
        with self.assertRaises(SystemExit):
            menu.start_menu()
