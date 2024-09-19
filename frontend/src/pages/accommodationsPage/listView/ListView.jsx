import React from 'react'
import ListElement from './ListElement'
export const ListView = ({listData}) => {
  console.log(listData)
  return (
    <>
    <div>
      {/* list view header */}
    </div>

    <div>
      {listData.map((item) => {
        <ListElement 
        accommodation={item.accommodation} 
        partOfBody={item.partOfBody}
        naicsIndustry={item.naicsIndustry}
        natureOfInjury={item.natureOfInjury}
        source={item.source}
        status= {item.status}
          />
      })}
      </div>
    </>
  )
}

