import React from 'react'
import wsibLogo from '../assets/wsibLogo.png'
export default function NavBar() {
  const user = 1

  return (
    <div className="flex shadow-2xl py-12 justify-evenly">
        <div className='flex'>
            <img className='px-4' src={wsibLogo} alt="WSIB Logo"/>  
        <h1 className='text-4xl hidden md:block px-4 my-auto'>Internal Services</h1>
        </div>
       
       <div className='flex my-auto'>
       <p className='px-8 py-0 my-auto'> Français</p>
        <p className='px-8 sm:block hidden py-0 my-auto'>Exit</p>

        {
          !user ?
          <button className='flex rounded-3xl bg-sky-600 text-white px-8 py-2'>
            <div className='px-2'>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="user-lock-solid">
<path id="Vector" d="M10 3.125C7.5625 3.125 5.625 5.0625 5.625 7.5C5.625 9.02344 6.38123 10.351 7.54394 11.1328C5.31876 12.0921 3.75 14.3085 3.75 16.875H5C5 14.125 7.25 11.875 10 11.875C10.75 11.875 11.5002 12.063 12.1252 12.3755C12.3127 12.0005 12.5 11.6248 12.8125 11.3123C12.6881 11.2501 12.5598 11.2007 12.4329 11.1462C13.6077 10.3663 14.375 9.03275 14.375 7.5C14.375 5.0625 12.4375 3.125 10 3.125ZM10 4.375C11.75 4.375 13.125 5.75 13.125 7.5C13.125 9.25 11.75 10.625 10 10.625C8.25 10.625 6.875 9.25 6.875 7.5C6.875 5.75 8.25 4.375 10 4.375ZM15.625 11.25C14.25 11.25 13.125 12.375 13.125 13.75V15H11.25V20H20V15H18.125V13.75C18.125 12.375 17 11.25 15.625 11.25ZM15.625 12.5C16.3125 12.5 16.875 13.0625 16.875 13.75V15H14.375V13.75C14.375 13.0625 14.9375 12.5 15.625 12.5ZM12.5 16.25H18.75V18.75H12.5V16.25Z" fill="white"/>
</g>
</svg>
</div>
            Login
        </button>
          :
          <p className='underline px-8 text-sky-600 font-bold'>Logout</p>
        }
        
       </div>
        
    </div>
  )
}
