import React from 'react';
import { Play, Github } from 'lucide-react';

interface HeaderProps {
  onRestart: () => void;
}

const Header: React.FC<HeaderProps> = ({ onRestart }) => {
  return (
    <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <Play className="w-4 h-4 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white">Talk2Diagram</h1>
            <p className="text-sm text-gray-400">Create Animations with Natural Language</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-gray-400">
            <a 
              href="https://github.com/Ayonto"
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center space-x-1 hover:text-white transition-colors duration-200"
              >
              <Github className="w-4 h-4" />
              <span></span>
            </a>
            <span>| made by <b>s.i.ayonto</b> </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;