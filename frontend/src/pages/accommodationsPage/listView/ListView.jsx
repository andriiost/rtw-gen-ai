import { React, useState, useEffect } from 'react'
import ListElement from './ListElement'
import SortWhite from '../../../assets/sortWhite.png'
import SortAlphaUp from '../../../assets/sortAlphaUp.png'
import SortAlphaDown from '../../../assets/sortAlphaDown.png'
import getHeaderKey from '../../../mockData/utils'
export const ListView = ({ listData }) => {
  // headers used for the list view
  const headers = [
    'Accommodation',
    'Part of Body',
    'NAICS Industry',
    'Nature of Injury',
    'Source',
    'Status'
  ]
  // create an object for sort such that each header has a numeric value
  const [sort, setSort] = useState(Object.fromEntries(headers.map(i => [i, 0])))
  const [sortedData, setSortedData] = useState([])
  console.log(listData)

  useEffect(() => {
    const sorted = [...listData].sort((a, b) => {
      const column = Object.keys(sort).find(header => sort[header] !== 0);
      if (column) {
        const convertedHeader = getHeaderKey(column);
        if (sort[column] === 1) {
          return a[convertedHeader] > b[convertedHeader] ? 1 : -1;
        }
        if (sort[column] === 2) {
          return a[convertedHeader] < b[convertedHeader] ? 1 : -1;
        }
      }
      return 0;
    });
    setSortedData(sorted);
  }, [listData, sort]);

  const sortColumn = (header) => {
    if (sort[header] == 2) setSort({ ...sort, [header]: 0 })
      else setSort({ ...sort, [header]: sort[header] + 1 })
  };

  const changeIcon = (state) => {
    if (state == 0) {
      return SortWhite
    } else if (state == 1) {
      return SortAlphaUp
    } else {
      return SortAlphaDown
    }
  }

  return (
    <div className='w-full'>
      <div className='grid grid-cols-6 p-4 bg-blue-950'>
        {headers.map((header, i) => {
          return (
            <>
              {i != 5 ?
                <div key={i} className='flex justify-between p-1' onClick={() => sortColumn(header)}>
                  <h3 className='text-white text-sm'>{header}</h3>
                  <img src={changeIcon(sort[header])} className='mr-4' />
                </div> :
                <div key={i} className='flex justify-between p-1'>
                  <h3 className='text-white text-sm'>{header}</h3>
                </div>}

            </>
          )
        })}
      </div>

      <div className=''>
        {sortedData.map((item, i) => {
          return <ListElement
            key={i}
            id={i}
            accommodation={item.accommodation_name}
            partOfBody={item.injury_location_name}
            naicsIndustry={item.industry_name}
            natureOfInjury={item.activity_name}
            source={item.source}
            status={item.verified}
          />
        })}
      </div>
    </div>
  )
}

