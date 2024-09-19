import React from 'react'

export default function 
({ accommodation, partOfBody, naicsIndustry, natureOfInjury, source, status }) {
  return (
    <div className='grid-col-6 gap-10'>
                    <div> {accommodation}</div>
                    <div>{partOfBody}</div>
                    <div> {naicsIndustry}</div>
                    <div> {natureOfInjury}</div>
                    {/* this will be an actual link */}
                    <div> {source}</div> 
                    {status ? 
                    <div className='flex'> Verified
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#00803E"/>
</svg>
                     </div>  
                    :
                    <div className='flex'> Unverified 
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#D90000"/>
</svg>

                    </div>  
                     }
                                
    </div>
  )
}
