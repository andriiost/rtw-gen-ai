import React from 'react'
import Card from './Card'

const CardView = ({ cards }) => {
  return (
    <div className='grid grid-cols-3 gap-4'>
      {cards.map((obj, i) => {
        return <Card key={i}
          name={obj.accommodation_name}
          desc={obj.accommodation_description}
          injury={obj.injury_location_name}
          industry={obj.industry_name}
          activity={obj.activity_name}
          verified={obj.verified} 
          date_created={obj.date_created}
          link={obj.link}
          />
      })}
    </div>
  )
}

export default CardView