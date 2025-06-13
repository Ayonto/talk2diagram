import React from 'react';
import { Play, Download, Clock, Video } from 'lucide-react';
import { VideoData } from '../types';

interface PreviewPanelProps {
  video: VideoData | null;
  isGenerating: boolean;
}

const PreviewPanel: React.FC<PreviewPanelProps> = ({ video, isGenerating }) => {
  return (
    <div className="h-full flex flex-col">
      {/* Compact Header */}
      <div className="px-6 py-3 border-b border-gray-700 bg-gray-900">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 bg-gradient-to-r from-green-500 to-blue-500 rounded-md flex items-center justify-center">
            <Video className="w-3 h-3 text-white" />
          </div>
          <h2 className="text-sm font-medium text-white">Preview</h2>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 p-6">
        {isGenerating ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4 mx-auto animate-pulse-subtle">
                <Play className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-lg font-medium text-gray-300 mb-2">Creating Animation</h3>
              <p className="text-sm text-gray-500">
                Processing your request with AI and rendering the video...
              </p>
              <div className="mt-4 flex justify-center">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        ) : video ? (
          <div className="h-full flex flex-col animate-fade-in">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                  <Play className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h3 className="font-medium text-gray-200">{video.title}</h3>
                  <div className="flex items-center space-x-2 text-xs text-gray-500">
                    <Clock className="w-3 h-3" />
                    <span>Generated {video.timestamp.toLocaleTimeString()}</span>
                  </div>
                </div>
              </div>

              {/* download button */}
              {/* <button className="p-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors duration-200">
                <Download className="w-4 h-4 text-gray-400" />
              </button> */} 
              
            </div>
            
            <div className="flex-1 bg-black rounded-lg overflow-hidden flex items-center justify-center">
              <video
                src={video.url}
                // controls
                autoPlay
                loop
                className="max-w-full max-h-full object-contain"
                onError={(e) => {
                  console.error('Video error:', e);
                }}
              >
                Your browser does not support the video tag.
              </video>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mb-4 mx-auto">
                <Play className="w-8 h-8 text-gray-500" />
              </div>
              <h3 className="text-lg font-medium text-gray-300 mb-2">Ready for Animation</h3>
              <p className="text-sm text-gray-500 max-w-sm mx-auto">
                Start a conversation to create your first physics or math animation. 
                Describe what you want to see and I'll bring it to life!
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PreviewPanel;