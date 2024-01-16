from sqlmodel import create_engine,Session

class Connection:
    def __init__(self, db_string):
        print(f"THis is db:{db_string}")
        self.engine = create_engine(db_string)
        self.session = Session(self.engine)
    def insert(self,model_instance):
        print(model_instance)
        self.session.add(model_instance)
        self.session.commit()
        self.session.refresh(model_instance)
        return model_instance
    def fetch(self,sql_st):
        return self.session.exec(sql_st)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            pass
        self.session.close()

