import React from 'react'

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number
  max?: number
}

export function Progress({ className = '', value = 0, max = 100, ...props }: ProgressProps) {
  const percentage = Math.min(Math.max(0, value), max)
  
  return (
    <div
      className={`relative h-2 w-full overflow-hidden rounded-full bg-gray-100 ${className}`}
      {...props}
    >
      <div
        className="h-full w-full flex-1 bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 ease-out"
        style={{
          transform: `translateX(-${100 - (percentage / max) * 100}%)`,
        }}
      />
    </div>
  )
}