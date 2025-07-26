import React from 'react'

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive'
}

const alertVariants = {
  default: 'bg-white text-gray-950 border-gray-200',
  destructive: 'border-red-500/50 text-red-900 bg-red-50 [&>svg]:text-red-600'
}

export function Alert({ className = '', variant = 'default', ...props }: AlertProps) {
  return (
    <div
      role="alert"
      className={`relative w-full rounded-lg border p-4 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-gray-950 [&>svg~*]:pl-7 ${alertVariants[variant]} ${className}`}
      {...props}
    />
  )
}

export function AlertTitle({ className = '', ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h5
      className={`mb-1 font-medium leading-none tracking-tight ${className}`}
      {...props}
    />
  )
}

export function AlertDescription({ className = '', ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <div
      className={`text-sm [&_p]:leading-relaxed ${className}`}
      {...props}
    />
  )
}