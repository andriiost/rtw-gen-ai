import React from 'react'
import Card from './Card'

const CardView = ({ cards }) => {
  console.log(cards)
  return (
    <div className='grid grid-cols-3 gap-4'>
      {cards.map((obj) => {
        return <Card name={obj.accommodation_name}
          desc={obj.accommodation_description}
          injury={obj.injury_location_name}
          industry={obj.industry_name}
          activity={obj.activity_name}
          verified={obj.verified} 
          date_created={obj.date_created}
          />
      })}
    </div>
  )
}

export default CardView