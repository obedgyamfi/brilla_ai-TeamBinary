import pandas as pd
import sqlite3

# Load the excel file and inspect the columns
filepath = ('./updated_excel_file.xlsx')

def load_excel_to_db(filepath, cursor, year,content):
    
    df = pd.read_excel(filepath)
    
    # Map the DataFrame columns to the database columns
    for _, row in df.iterrows():
        sn = row['S/N']
        has_preamble = row['Has Preamble']
        preamble_text = row['Preamble Text']
        question = row['Question']
        has_question_figure = row['Question has figure']
        question_figure_name = row['Question figure name']
        has_answer_figure = row['Answer has figure']
        answer_figure_name = row['Answer figure name']
        answer = row['Answer']
        has_calculations = row['calculations present']
        subject = row['Subject']
        
        cursor.execute('''
        INSERT OR IGNORE INTO questions (sn, has_preamble, preamble_text, question, has_question_figure, question_figure_name,
                                         has_answer_figure, answer_figure_name, answer, has_calculations, subject, year, content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sn, has_preamble, preamble_text, question, has_question_figure, question_figure_name,
              has_answer_figure, answer_figure_name, answer, has_calculations, subject, year, content))
        
def main():
    
    # Add more file paths as needed
    # file_paths = [
    #     ('./ai_models_and_data/models_and_data/nsmq_past_questions/NSMQ QUESTIONS SPREADSHEETS/2009/2009 NSMQ contest 1.xlsx', 2009, 1),
    # ]    
    
    file_paths = [
        ('./updated_excel_file.xlsx', 2021, 1),
    ] 
    
    conn = sqlite3.connect('nsmq.db')
    cur = conn.cursor()
    
    for filepath, year, content in file_paths:
        load_excel_to_db(filepath, cur, year, content)
        
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == '__main__':
    main()
    print("Questions loaded successfully!!")
    
    
    