import React from 'react'

export default function
  ({ id, accommodation, partOfBody, naicsIndustry, natureOfInjury, source, status }) {
    const truncateText = (text) => {
      return (text.length > 19) ? text.slice(0, 19) + "..." : text
    }
  return (
    <div className={`grid grid-cols-6 p-4 gap-8 hover:bg-sky-100 transition ease-in hover:ease-out ${id % 2 == 1 && 'bg-slate-50'}`}>
      <p> {truncateText(accommodation)}</p>
      <p> {truncateText(partOfBody)}</p>
      <p> {truncateText(naicsIndustry)}</p>
      <p> {truncateText(natureOfInjury)}</p>
      {/* this will be an actual link */}
      <p> {source}</p>
      {status ?
        <div className='flex items-center gap-3'>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#00803E" />
          </svg>
          Verified
        </div>
        :
        <div className='flex items-center gap-3'>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#D90000" />
          </svg>
          Unverified
        </div>
      }

    </div>
  )
}
