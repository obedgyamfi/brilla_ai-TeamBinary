// components/TopNavbar.tsx
"use client";
import React, { useState, useEffect, useContext } from "react";
import { Button } from "../button"; // Adjust the import path based on your project structure
import { QuizContext } from "@/components/QuizContext";

const API_BASE_URL = 'http://localhost:3001'



const TopNavbar = () => {
  // Online/Offline state indicator
  const [isOnline, setIsOnline] = useState(true);

  const [showDropdown, setShowDropdown] = useState({
    year: false,
    contest: false,
    round: false,
    timer: false,
  });

  const [selectedYear, setSelectedYear] = useState<number>(2021);
  const [selectedContest, setSelectedContest] = useState<number>(1);
  const [selectedRound, setSelectedRound] = useState<number>(1);
  const [selectedTimer, setSelectedTimer] = useState<number>(10);
  // const [currentIndex, setCurrentIndex] = useState<number>(1);
  // const [totalQuestions, setTotalQuestions] = useState<number>(24);

  const { currentIndex, totalQuestions } =
  useContext(QuizContext);

  const [error, setError] = useState<string>("");

  useEffect(() => {
    const handleOnlineStatusChange = () => {
      setIsOnline(navigator.onLine);
    };
    window.addEventListener("online", handleOnlineStatusChange);
    window.addEventListener("offline", handleOnlineStatusChange);

    return () => {
      window.removeEventListener("online", handleOnlineStatusChange);
      window.removeEventListener("offline", handleOnlineStatusChange);
    };
  }, []);

  // Function to toggle online/offline status
  const toggleOnlineStatus = () => {
    setIsOnline((prevIsOnline) => !prevIsOnline);
  };

  // Mock data for answered questions and timer
  const seconds = 0; // Change this to the actual number of seconds
  const timer = `${seconds}s`; // Timer displayed in seconds

  const toggleDropdown = (menu) => {
    setShowDropdown((prevState) => ({
      ...prevState,
      [menu]: !prevState[menu],
    }));
  };

  const handleSave = async (selectedValue, parentMenu) => {
    try {
      // Update the selected value based on the parent menu
      switch (parentMenu) {
        case "selectedYear":
          setSelectedYear(selectedValue);
          break;

        case "selectedContest":
          setSelectedContest(selectedValue);
          break;

        case "selectedRound":
          setSelectedRound(selectedValue);
          break;
        case "selectedTimer":
          setSelectedTimer(selectedValue);
          break;
        default:
          break;
      }

      // Send the parameters or contents for settings to the Python server API
      const response = await fetch(
        `${API_BASE_URL}/api/save_app_settings`,
        {
          method: "POST",
          body: new URLSearchParams({
            [parentMenu]: selectedValue,
          }),
        }
      );

      const data = await response.json();
      console.log(data.message);
      setError("");
    } catch (error) {
      console.error("Error:", error);
      setError("Failed to save settings. Please try again.");
    }
  };

  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 flex justify-center">
      <div className="flex items-center justify-between w-144 space-x-4 rounded-sm bg-white p-2 shadow-md">
        {/* Online/Offline state indicator */}
        <Button variant="link" onClick={toggleOnlineStatus}>
          {isOnline ? (
            <>
              <svg
                className="w-4 h-4 fill-current text-green-500"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M10 0C4.477 0 0 4.477 0 10c0 5.523 4.477 10 10 10 5.523 0 10-4.477 10-10C20 4.477 15.523 0 10 0zm0 18.75c-4.566 0-8.25-3.684-8.25-8.25S5.434 2.25 10 2.25c4.566 0 8.25 3.684 8.25 8.25S14.566 18.75 10 18.75zM10 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm2.224 8.07a.75.75 0 0 1-1.06 1.06l-2.5-2.5a.75.75 0 0 1 1.06-1.06l2.5 2.5z" />
              </svg>
              <span className="text-green-500">Online</span>
            </>
          ) : (
            <>
              <svg
                className="w-4 h-4 fill-current text-red-500"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M10 0C4.477 0 0 4.477 0 10c0 5.523 4.477 10 10 10 5.523 0 10-4.477 10-10C20 4.477 15.523 0 10 0zm0 18.75c-4.566 0-8.25-3.684-8.25-8.25S5.434 2.25 10 2.25c4.566 0 8.25 3.684 8.25 8.25S14.566 18.75 10 18.75zM10 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm1.06 11.224a.75.75 0 0 1-1.06 1.06l-2.5-2.5a.75.75 0 0 1 1.06-1.06l2.5 2.5zM10.5 5.5a.5.5 0 1 0-1 0v6a.5.5 0 0 0 1 0v-6z" />
              </svg>
              <span className="text-red-500">Offline</span>
            </>
          )}
        </Button>

        {/* Dropdown Menu for Year */}
        <div className="relative">
          <Button
            variant="link"
            className="text-gray=900"
            onClick={() => toggleDropdown("year")}
          >
            {selectedYear}
          </Button>
          {showDropdown.year && (
            <div className="absolute top-full mt-4 bg-white shadow-md rounded-sm">
              {/* Add your year options here */}
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(2021, "selectedYear");
                  toggleDropdown("year");
                }}
              >
                2021
              </Button>
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(2020, "selectedYear")
                  toggleDropdown("year");
                }}
              >
                2020
              </Button>
            </div>
          )}
        </div>

        {/* Dropdown Menu for Contest */}
        <div className="relative">
          <Button
            variant="link"
            className="text-gray=900"
            onClick={() => toggleDropdown("contest")}
          >
            {"Contest" + " " + selectedContest}
          </Button>
          {showDropdown.contest && (
            <div className="absolute top-full mt-4 bg-white shadow-md rounded-sm">
              {/* Add your year options here */}
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(1, "selectedContest");
                  toggleDropdown("contest");
                }}
              >
                Contest 1
              </Button>
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(2, "selectedContest" )
                  toggleDropdown("contest");
                }}
              >
                Contest 2
              </Button>
            </div>
          )}
        </div>

        {/* Dropdown Menu for Round */}
        <div className="relative">
          <Button
            variant="link"
            className="text-gray=900"
            onClick={() => toggleDropdown("round")}
          >
            {"Round" + " " + selectedRound}
          </Button>
          {showDropdown.round && (
            <div className="absolute top-full mt-4 bg-white shadow-md rounded-sm">
              {/* Add your year options here */}
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(1, "selectedRound");
                  toggleDropdown("round");
                }}
              >
                Round 1
              </Button>
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(2, "selectedRound");
                  toggleDropdown("round");
                }}
              >
                Round 2
              </Button>
            </div>
          )}
        </div>

        {/* Indicator for question index */}
        <Button variant="link" className="text-gray-900">
          {currentIndex}/{totalQuestions}
        </Button>

        {/* Dropdown menu for timer */}
        <div className="relative">
          <Button
            variant="link"
            className="text-gray=900"
            onClick={() => toggleDropdown("timer")}
          >
            {selectedTimer + "s"}
          </Button>
          {showDropdown.timer && (
            <div className="absolute top-full mt-4 bg-white shadow-md rounded-sm">
              {/* Add your year options here */}
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(10, "selectedTimer");
                  toggleDropdown("timer");
                }}
              >
                10s
              </Button>
              <Button
                className="text-gray=900 bg-white hover:bg-blue-400 hover:text-white"
                onClick={() => {
                  handleSave(15, "selectedTimer");
                  toggleDropdown("timer");
                }}
              >
                15s
              </Button>
            </div>
          )}
        </div>
      </div>
      {/* Dropdown Menus */}
    </div>
  );
};
export default TopNavbar;
