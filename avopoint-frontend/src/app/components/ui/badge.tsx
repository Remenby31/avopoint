import React from 'react'

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'success'
}

const badgeVariants = {
  default: 'border-transparent bg-blue-500 text-white hover:bg-blue-600',
  secondary: 'border-transparent bg-gray-100 text-gray-900 hover:bg-gray-200',
  destructive: 'border-transparent bg-red-500 text-white hover:bg-red-600',
  outline: 'text-gray-950 border-gray-200',
  success: 'border-transparent bg-green-500 text-white hover:bg-green-600'
}

export function Badge({ className = '', variant = 'default', ...props }: BadgeProps) {
  return (
    <div
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-gray-950 focus:ring-offset-2 ${badgeVariants[variant]} ${className}`}
      {...props}
    />
  )
}