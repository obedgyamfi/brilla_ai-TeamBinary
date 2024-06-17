// components/QuizContext.tsx
"use client"
import { createContext, useState } from 'react';

export const QuizContext = createContext({
  questionText: '',
  setQuestionText: (text: string) => {},
  year: '', 
  setYear: (text: string) => {},
  contest: '',
  setContest: (text: string) => {},
  round: '', 
  setRound: (text: string) => {},
  currentIndex: 1,
  setCurrentIndex: (value: number) => {},
  totalQuestions:24,
  setTotalQuestions: (value: number) => {}
});

export const QuizProvider = ({ children }) => {
  const [questionText, setQuestionText] = useState('');
  const [year, setYear] = useState('2021');
  const [contest, setContest] = useState('Contest 1');
  const [round, setRound] = useState('Round 1');
  const [currentIndex, setCurrentIndex] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(24);

  return (
    <QuizContext.Provider value={{ 
      questionText, year, contest, round, 
      currentIndex, totalQuestions, 
      setQuestionText, setYear, setContest, setRound, 
      setCurrentIndex, setTotalQuestions
      }}>
      {children}
    </QuizContext.Provider>
  );
};