"use client";
import React, { useContext, useEffect, useState } from "react";
import { QuizContext } from "@/components/QuizContext";
import katex from 'katex';
import 'katex/dist/katex.min.css'; // Import KaTeX CSS

const Home = () => {
  const { questionText } = useContext(QuizContext);
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    setDisplayedText('');
    let index = 0;
    const intervalId = setInterval(() => {
      if (index < questionText.length) {
        const char = questionText[index];
        setDisplayedText((prevText) => prevText + char);
        index++;
      } else {
        clearInterval(intervalId);
      }
    }, 30);

    return () => clearInterval(intervalId);
  }, [questionText]);

  // Rendering LaTeX expressions using KaTeX
  const question_parts = displayedText.split("$");

  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <div className="flex justify-center items-center w-64 h-64 rounded-full border-2 border-blue-300 bg-gray-100 relative bottom-20">
        <h1 className="text-2xl font-bold">Quizmistress</h1>
      </div>
      <div className="mb-6 w-2/3 h-auto mt-0">
        <p className="text-lg">
          {question_parts.map((question_part, index) => {
            if (index % 2 === 0) {
              // Even indices are regular text
              return (
                <React.Fragment key={index}>{question_part}</React.Fragment>
              );
            } else {
              // Odd indices are LaTeX
              return (
                <span
                  key={index}
                  dangerouslySetInnerHTML={{
                    __html: katex.renderToString(question_part, {
                      throwOnError: false,
                    }),
                  }}
                />
              );
            }
          })}
        </p>
      </div>
    </div>
  );
};

export default Home;



// "use client";
// import React, { useContext, useEffect, useState } from "react";
// import { QuizContext } from "@/components/QuizContext";
// import katex from 'katex';
// import 'katex/dist/katex.min.css'; // Import KaTeX CSS

// const Home = () => {
//   const { questionText } = useContext(QuizContext);
//   const [displayedText, setDisplayedText] = useState("");

//   useEffect(() => {
//     setDisplayedText('');
//     let index = 0;
//     const intervalId = setInterval(() => {
//       if (index < questionText.length) {
//         setDisplayedText((prevText) => prevText + questionText[index]);
//         index++;
//       } else {
//         clearInterval(intervalId);
//       }
//     }, 100);

//     return () => clearInterval(intervalId);
//   }, [questionText]);

//   // Rendering LaTeX expressions using KaTeX
//   const question_parts = displayedText.split("$");

//   return (
//     <div className="flex flex-col justify-center items-center h-screen">
//       <div className="flex justify-center items-center w-64 h-64 rounded-full border-2 border-blue-300 bg-gray-100 relative bottom-20">
//         <h1 className="text-2xl font-bold">Quizmistress</h1>
//       </div>
//       <div className="mt-4 w-2/3 h-auto">
//         <p className="text-lg">
//           {question_parts.map((question_part, index) => {
//             if (index % 2 === 0) {
//               // Even indices are regular text
//               return (
//                 <React.Fragment key={index}>{question_part}</React.Fragment>
//               );
//             } else {
//               // Odd indices are LaTeX
//               return (
//                 <span
//                   key={index}
//                   dangerouslySetInnerHTML={{
//                     __html: katex.renderToString(question_part, {
//                       throwOnError: false,
//                     }),
//                   }}
//                 />
//               );
//             }
//           })}
//         </p>
//       </div>
//     </div>
//   );
// };

// export default Home;
