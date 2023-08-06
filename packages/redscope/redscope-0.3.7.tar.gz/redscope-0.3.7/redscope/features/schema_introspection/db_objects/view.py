from redscope.features.schema_introspection.db_objects.ddl import DDL


class View(DDL):

    def __init__(self, schema: str, name: str, ddl: str):
        super().__init__(name)
        self.schema = schema
        self.ddl = ddl

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    @property
    def create(self) -> str:
        return f"CREATE VIEW {self.schema}.{self.name} AS \n {self.ddl};"

    @property
    def create_if_not_exist(self) -> str:
        return f"CREATE OR REPLACE VIEW {self.schema}.{self.name} AS \n {self.ddl};"

    @property
    def drop(self) -> str:
        return f"DROP VIEW {self.schema}.{self.name};"

    @property
    def drop_if_exist(self) -> str:
        return f"DROP VIEW IF EXISTS {self.schema}.{self.name};"
