import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create a table for questions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sn INTEGER,
                has_preamble INTEGER,
                preamble_text TEXT,
                question TEXT,
                has_question_figure INTEGER,
                question_figure_name TEXT,
                has_answer_figure INTEGER,
                answer_figure_name TEXT,
                answer TEXT,
                has_calculations INTEGER,
                subject TEXT,
                year INTEGER,
                content INTEGER,
                UNIQUE(sn, year, content)
            )
        ''')

        # Create a table for answers
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_answers_stt (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                question_id INTEGER,
                answer TEXT,
                is_correct INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (question_id) REFERENCES questions (sn)
            )
        ''')

        # Create a table for app settings
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                selected_voice TEXT,
                selected_year INTEGER,
                selected_contest TEXT,
                roundSelection TEXT,
                selected_rounds TEXT
            )
        ''')

        # Commit the changes
        self.conn.commit()
    

    def insert_question(self, sn, has_preamble, preamble_text, question, has_question_figure, question_figure_name, has_answer_figure, answer_figure_name, answer, has_calculations, subject):
        self.cursor.execute("""
            REPLACE INTO questions (sn, has_preamble, preamble_text, question, has_question_figure, question_figure_name, has_answer_figure, answer_figure_name, answer, has_calculations, subject)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sn, has_preamble, preamble_text, question, has_question_figure, question_figure_name, has_answer_figure, answer_figure_name, answer, has_calculations, subject))
        self.conn.commit()

    def insert_user_answer(self, user_id, question_id, answer, is_correct):
        self.cursor.execute("""
            INSERT INTO user_answers_stt (user_id, question_id, answer, is_correct)
            VALUES (?, ?, ?, ?)
        """, (user_id, question_id, answer, is_correct))
        self.conn.commit()

    def insert_app_setting(self, selected_voice, selected_year, selected_contest, roundSelection, selected_rounds):
        self.cursor.execute("""
            INSERT INTO app_settings (selected_voice, selected_year, selected_contest, roundSelection, selected_rounds)
            VALUES (?, ?, ?, ?, ?)
        """, (selected_voice, selected_year, selected_contest, roundSelection, selected_rounds))
        self.conn.commit()
        
    def get_app_setting(self):
        self.cursor.execute("SELECT * FROM app_settings")
        result = self.cursor.fetchone()
        if result: 
            selected_voice, selected_year, selected_contest, roundSelection, selected_rounds = result
            return {
                "selected_voice": selected_voice,
                "selected_year": selected_year,
                "selected_contest": selected_contest,
                "roundSelection": roundSelection,
                "selected_rounds": selected_rounds
            }
        else:
            return None

    def get_questions(self):
        
        self.cursor.execute("SELECT question FROM questions")
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.conn.close()

#db = Database('my_database.db')

#db.insert_question(1, 1, 'Preamble text', 'Question text', 1, 'Question figure name', 1, 'Answer figure name', 'Answer text', 1, 'Subject text')
#db.insert_user_answer(1, 1, 'User answer text', 1)
#db.insert_app_setting('Setting name', 'Setting value')

#db.close()
