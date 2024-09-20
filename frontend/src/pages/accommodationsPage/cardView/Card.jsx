import React from 'react'
import { NavLink } from 'react-router-dom'
const Card = ({ name, desc, injury, industry, activity, verified, date_created, link }) => {
  const truncDesc = desc.length > 100
    ? desc.slice(0, 150) + "..."
    : desc;
  return (
    <div className='border-slate-200 border-2 rounded-md p-3'>
      <h2 className='text-2xl text-sky-600 font-bold'>{name}</h2>
      <p className='text-slate-500 text-sm mb-4'>{activity}</p>
      <div className="flex mb-4 flex-row">
        <div className="px-3 py-1 me-1 border-2 border-emerald-800/75 text-emerald-800/75 rounded-3xl">
          {injury}
        </div>
        <div className="px-3 py-1 mx-1 border-2 border-gray-500 text-gray-500 rounded-3xl">
          {industry}
        </div>
      </div>
      <p className='text-slate-500 text-base mb-10'>{truncDesc}</p>
      <NavLink to={link} className='flex flex-row text-base mb-2 text-sky-600'>
        <p className='underline'> Visit the original document </p>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g id="external-link-alt-solid">
            <path id="Vector" d="M13.5 3.75V5.25H17.6719L8.46094 14.4609L9.53906 15.5391L18.75 6.32812V10.5H20.25V3.75H13.5ZM3.75 6.75V20.25H17.25V10.5L15.75 12V18.75H5.25V8.25H12L13.5 6.75H3.75Z" fill="#0076BF" />
          </g>
        </svg>
      </NavLink>
      {verified ?
        <div className='flex text-slate-500 text-sm'>
          <div className='my-auto'>
            <svg className='my-auto' width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#00803E" />
            </svg>
          </div>
          <p className='px-2'>
            Verified on {date_created}
          </p>
        </div>
        :
        <div className='flex text-slate-500 content-center text-center text-sm'>
          <div className='my-auto'>
            <svg className='my-auto' width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#D90000" />
            </svg>
          </div>
          <p className="px-2">
            Unverified
          </p>
        </div>
      }
    </div>
  )
}

export default Card