import React from 'react'

const Card = ({name, desc, injury, industry, activity, verified, date_created}) => {
  const truncDesc = desc.length > 100
    ? desc.slice(0, 100) + "..."
    : desc;
  return (
    <div className='border-slate-200 border-2 rounded-md p-3'>
        <h2 className='text-2xl text-blue-700 font-bold'>{name}</h2>
        <p className='text-slate-600'>{truncDesc}</p>
    </div>
  )
}

export default Card