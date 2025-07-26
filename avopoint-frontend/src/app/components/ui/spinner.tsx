import React from 'react'

export interface SpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg'
}

const spinnerSizes = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6', 
  lg: 'w-8 h-8'
}

export function Spinner({ className = '', size = 'md', ...props }: SpinnerProps) {
  return (
    <div
      className={`${spinnerSizes[size]} animate-spin rounded-full border-2 border-gray-300 border-t-blue-500 ${className}`}
      {...props}
    />
  )
}

export function LoadingDots({ className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`flex space-x-1 ${className}`} {...props}>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
    </div>
  )
}