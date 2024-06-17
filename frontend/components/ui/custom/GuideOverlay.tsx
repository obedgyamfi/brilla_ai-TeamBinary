import React from "react";
import { Dialog, DialogPanel, DialogTitle } from "@headlessui/react";

interface AnalyticsOverlayProps {
  isOpen: boolean;
  onClose: () => void;
}

const GuideOverlay: React.FC<AnalyticsOverlayProps> = ({ isOpen, onClose }) => {
  return (
    <Dialog open={isOpen} onClose={onClose}>
      <DialogPanel className="fixed inset-0 bg-white/30 p-4 flex items-center justify-center">
        <div className="rounded-lg shadow-md p-6 max-w-4xl w-full bg-white backdrop-blur-md">
          <DialogTitle className="border-b pb-2 font-medium text-gray-900">Guide</DialogTitle>
          <div className="mt-4 text-gray-500 space-y-4">
            <p>Welcome to our AI education website!</p>
            <p>Here's a brief guide on how to navigate our quiz-based assessment page:</p>
            <ol className="list-decimal list-inside space-y-2">
              <li>Check your online status at the top of the page. If connected, it will display "Online."</li>
              <li>Quiz details like the year, contest number, and round number are displayed at the top.</li>
              <li>Keep track of the quiz time with the timer at the top.</li>
              <li>Click the microphone button and speak your answer clearly to respond.</li>
              <li>Click the play button to listen to a question again.</li>
              <li>Click the next button to move to the next question.</li>
              <li>If issues occur, click the refresh button to reload the page.</li>
            </ol>
          </div>

          <div className="absolute bottom-4 right-4 flex items-center justify-end space-x-2">
            <button
              type="button"
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md shadow py-2 px-4"
              onClick={onClose}
            >
              Close
            </button>
            </div>
        </div>
        
      </DialogPanel>
    </Dialog>
  );
};

export default GuideOverlay;
