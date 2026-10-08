import unittest

from app import create_app


class DatabasePoolConfigurationTest(unittest.TestCase):
    def test_database_pool_configuration_is_expanded_for_mysql(self):
        app = create_app()
        engine_options = app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {})

        self.assertGreaterEqual(engine_options.get("pool_size"), 20)
        self.assertGreaterEqual(engine_options.get("max_overflow"), 30)
        self.assertTrue(engine_options.get("pool_pre_ping"))


if __name__ == "__main__":
    unittest.main()
