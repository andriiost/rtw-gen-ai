import React from 'react'
import { Link } from 'react-router-dom'
export default function Error({title, message, buttonText, buttonLink}) {
  return (
    <main className="grid min-h-full place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8">
              <div className="text-center">
                <p className="text-base font-semibold text-sky-600">:(</p>
                <h1 className="mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl">
                  {title}
                </h1>
                <p className="mt-6 text-base leading-7 text-gray-600">
                  {message}
                </p>
                <div className="mt-10 flex items-center justify-center gap-x-6">
                  <Link
                    to={buttonLink}
                    className="rounded-xl bg-sky-600 border-2 border-sky-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-white hover:text-sky-600"
                  >
                    {buttonText}
                  </Link>
                </div>
              </div>
            </main>
  )
}
