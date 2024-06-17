"use client";
// components/BottomDock.tsx
import { useState, useEffect } from "react";
import {
  ArrowRightIcon,
  ArrowPathIcon,
  ChartBarIcon,
  CogIcon,
  PlayIcon,
  PauseIcon,
  StopIcon,
} from "@heroicons/react/24/outline";
import { Button } from "../button";
import Link from "next/link";
import { MicrophoneIcon } from "@heroicons/react/24/solid";
import { useContext } from "react";
import { QuizContext } from "@/components/QuizContext";
import GuideOverlay from "./GuideOverlay";

import encode from "audiobuffer-to-wav";

// Here is your ngrok url
const API_BASE_URL = "http://localhost:3001";

const BottomDock = () => {
  // useState for the overlay windows
  const [isGuideOpen, setIsGuideOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // useStates for dynamic functionalities
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const { setQuestionText, setCurrentIndex, setTotalQuestions } =
    useContext(QuizContext);

  // useSTates for recording audio
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  const startQuiz = async () => {
    setIsPlaying(true);
    setCurrentIndex(currentQuestionIndex + 1);
    setTotalQuestions(24);
    try {
      // Fetch the audio URL from the API route
      const response = await fetch(`${API_BASE_URL}/api/play_questions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ index: currentQuestionIndex }),
      });

      // Ensure the response is OK
      if (response.ok) {
        const data_response = await response.json();
        console.log(data_response); // Check the structure of the received JSON data

        // Check for any errors in the response data
        if (data_response.questions_error) {
          console.error(
            "Error fetching questions:",
            data_response.questions_error
          );
        } else {
          // Display the question as text
          const textToDisplay = data_response.questions; // Adjust index based on your requirements
          setQuestionText(textToDisplay);
        }

        // Play the audio if audio_url is provided and valid
        if (data_response.audio_url) {
          const audioUrl = data_response.audio_url;
          console.log("audioUrl:", audioUrl);
          const audioResponse = await fetch(audioUrl);
          if (audioResponse.ok) {
            const blob = await audioResponse.blob();
            const url = window.URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.play();
          } else {
            console.error("Error fetching audio:", audioResponse.statusText);
          }
        } else if (data_response.audio_error) {
          console.error("Error fetching audio:", data_response.audio_error);
        }
      } else {
        console.error("Error fetching data:", response.statusText);
      }
    } catch (error) {
      console.error("Error starting quiz:", error);
    }
  };

  const pauseQuiz = async () => {
    setIsPlaying(false);
  };

  const stopRecording = async () => {
    setIsRecording(false);
  };

  const recordAnswer = async () => {
    if (!isRecording) {
      setIsRecording(true);
      console.log("Recording started ...");
      try {
        // Turn on microphone and record user's answer and send to server.

        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks: Blob[] = [];

        mediaRecorder.addEventListener("dataavailable", (event) => {
          audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", async () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          const audioArrayBuffer = await audioBlob.arrayBuffer();
          const audioContext = new AudioContext();
          const audioBuffer = await audioContext.decodeAudioData(
            audioArrayBuffer
          );
          const wavBlob = encode(audioBuffer);

          const formData = new FormData();
          formData.append(
            "audioFile",
            new File([wavBlob], "audio.wav", { type: "audio/wav" })
          );

          const response = await fetch(
            `${API_BASE_URL}/api/process_user_answer`,
            {
              method: "POST",
              body: formData,
            }
          );

          const data = await response.json();
          if (response.ok) {
            const audioUrl = data.audio_url;
            const audioResponse = await fetch(audioUrl);
            if (audioResponse.ok) {
              const blob = await audioResponse.blob();
              const url = window.URL.createObjectURL(blob);
              const audio = new Audio(url);
              audio.play();
            } else {
              console.error("Error playing response");
            }
          }

          console.log(data.message);
          console.log("is_round_complete:", data.is_round_complete);
          console.log("answer_state:", data.answer_state);
        });

        // Start recording
        mediaRecorder.start();

        // Stop recording after a brief moment (e.g, 5 seconds)
        setTimeout(() => {
          mediaRecorder.stop();
          setIsRecording(false);
        }, 8000);
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      // Stop recording
      //   setIsRecording(true);
      //   if(mediaRecorder) {
      //     mediaRecorder.stop();
      //     setIsRecording(true)
    }
  };

  const handleNextQuestion = () => {
    setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
    startQuiz();
  };

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div className="fixed bottom-8 left-0 right-0 flex justify-center">
      <div className="flex items-center justify-center space-x-16 border border-gray-300 rounded-full bg-gray-200 p-4">
        <Button
          variant="link"
          className="flex flex-col items-center justify-center"
          onClick={handleRefresh}
        >
          <div className="flex flex-col items-center justify-center">
            <ArrowPathIcon className="h-6 w-6 text-gray-500" />
            <span className="text-xs text-gray-500">Refresh</span>
          </div>
        </Button>

        <Button
          variant="link"
          className="flex flex-col items-center justify-center w-12 h-16"
          onClick={isPlaying ? pauseQuiz : startQuiz}
        >
          <div className="flex flex-col items-center justify-center">
            {isPlaying ? (
              <StopIcon className="h-6 w-6 text-red-500" />
            ) : (
              <PlayIcon className="h-6 w-6 text-gray-500" />
            )}

            <span className="text-xs text-gray-500">
              {isPlaying ? "Stop" : "Start"}
            </span>
          </div>
        </Button>

        <Button
          variant="link"
          className={`flex flex-col items-center justify-center rounded-full p-3 ${
            isRecording ? "bg-red-500" : "bg-blue-500"
          }`}
          onClick={isRecording ? stopRecording : recordAnswer}
        >
          <div className="flex flex-col items-center justify-center">
            <MicrophoneIcon className="h-8 w-8 text-white" />
          </div>
        </Button>

        <Button
          variant="link"
          className="flex flex-col items-center justify-center"
          onClick={handleNextQuestion} // Handle next question button click
        >
          <div className="flex flex-col items-center justify-center">
            <ArrowRightIcon className="h-6 w-6 text-gray-500" />
            <span className="text-xs text-gray-500">Next</span>
          </div>
        </Button>

        <Button
          variant="link"
          className="flex flex-col items-center justify-center"
          onClick={() => setIsGuideOpen(true)}
        >
          <div className="flex flex-col items-center justify-center">
            <ChartBarIcon className="h-6 w-6 text-gray-500" />
            <span className="text-xs text-gray-500">Guide</span>
          </div>
        </Button>

        {/* Guide Overlay */}
        <GuideOverlay
          isOpen={isGuideOpen}
          onClose={() => setIsGuideOpen(false)}
        />
      </div>
    </div>
  );
};

export default BottomDock;
