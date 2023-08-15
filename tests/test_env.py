from unittest import TestCase
from unittest.mock import patch
from src.envtool import EnvTool
import os

@patch.dict("os.environ", {"var_name": "var_value"})
class TestEnvTool(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_getting_environment_variable_succeeds(self):
        # Arrange
        env_tool = EnvTool()

        # Act
        result = env_tool.get_env_var("var_name")

        # Assert
        self.assertEqual("var_value", result)

    def test_getting_environment_variable_returns_null(self):
        # Arrange
        env_tool = EnvTool()

        # Act
        result = env_tool.get_env_var("non_existent_var")

        # Assert
        self.assertEqual(None, result)

    def test_getting_environment_variable_raises_exception(self):
        # Arrange
        env_tool = EnvTool()

        # Act
        with self.assertRaises(Exception):
            env_tool.get_env_var("non_existent_var", True)

    def test_setting_environment_variable_succeeds(self):
        # Arrange
        env_tool = EnvTool()

        # Act
        env_tool.set_env_var("var_name", "new_var_value")

        # Assert
        self.assertEqual("new_var_value", os.getenv("var_name"))

    @patch("builtins.open")
    def test_setting_environment_variables_from_file_succeeds(self, mock_open):
        # Arrange
        env_tool = EnvTool()
        mock_open.return_value.__enter__.return_value.readlines.return_value = ["# Var1","var_name=var_value","# Var2", "var_name2=var_value2", "# Var3", "var_name3=var_value3"]

        # Act
        env_tool.set_env_vars_from_file("tests/test_env_vars.txt")

        # Assert
        self.assertEqual("var_value", os.getenv("var_name"))
        self.assertEqual("var_value2", os.getenv("var_name2"))
        self.assertEqual("var_value3", os.getenv("var_name3"))

    @patch("builtins.open")
    def test_setting_environment_variables_from_file_raises_exception_when_file_not_found(self, mock_open):
        # Arrange
        env_tool = EnvTool()
        mock_open.side_effect = FileNotFoundError

        # Act
        with self.assertRaises(Exception):
            env_tool.set_env_vars_from_file("tests/test_env_vars.txt")