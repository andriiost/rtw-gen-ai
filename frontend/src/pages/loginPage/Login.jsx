import React from 'react'
import wsibLogo from '../../assets/wsibLogo.png'
export default function Login() {
  return (
    <div className="flex min-h-full flex-1 flex-col justify-center mb-6 mt-10 px-6 py-12 lg:px-8">
    <div className="sm:mx-auto sm:w-full sm:max-w-xs">
      <img
        alt="WSIB Logo"
        src={wsibLogo}
        className="mx-auto w-auto"
      />
      <h2 className="mt-10 text-left text-xs leading-9 tracking-tight text-gray-500">
        Sign in with your organizational account
      </h2>
    </div>

    <div className="sm:mx-auto sm:w-full sm:max-w-xs">
      <form className="space-y-2">
        <div>
          <div>
            <input
              id="email"
              name="email"
              type="email"
              placeholder='Firstname_Lastname@wsib.on.ca'
              required
              className="block w-full border-0 py-1.5 text-black placeholder:text-black shadow-sm ps-2 sm:text-sm sm:leading-6 bg-gray-200 "
            />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between">
          </div>
          <div>
            <input
              id="password"
              name="password"
              type="password"
              required
              placeholder='Password'
              className="block w-full border-0 py-1.5 text-black placeholder:text-black shadow-sm ps-2 sm:text-sm sm:leading-6 bg-gray-200"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            className="flex mt-5 w-full justify-center rounded-3xl bg-sky-600 text-white px-3 py-3 text-sm font-semibold leading-6 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
  )
}
