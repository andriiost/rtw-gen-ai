
// THIS PAGE IS A PLACEHOLDER MUST BE CHANGED STILL FROM ALL ACCOMMODATION PAGE

import { React, useState, useEffect } from 'react'
import accommodationsMock from '../../mockData/accommodationsMocks.json'
import CardView from '../accommodationsPage/cardView/CardView'
import { ListView } from '../accommodationsPage/listView/ListView'
import GridIcon from '../../assets/gridIcon.png'
import ListIcon from '../../assets/listIcon.png'
import SortIcon from '../../assets/sort.png'
import FilterIcon from '../../assets/filter.png'
import Dropdown from '../../components/Dropdown'
export default function BacklogView () {
    const [data, setData] = useState([])
    const [view, setView] = useState(true)
    const [categories, setCategories] = useState([])
    const [filters, setFilters] = useState([])
    const [search, setSearch] = useState("")

    //Menu filter options
    const categoryOptions = [
        { value: 'natureOfInjury', label: 'Nature of Injury' },
        { value: 'accommodationName', label: 'Accommodation Name' }
    ]
    const filterOptions = [
        { value: 'forward', label: 'A -> Z' },
        { value: 'reverse', label: 'Z -> A' }
    ]
    // setData(accommodationsMock.accommodations);

    useEffect(() => {
        // if (accommodationsMock) {
            let output = [...accommodationsMock.accommodations];

            output = output.filter((item) => {
                return (search === "") ? item : item.accommodation_name.toLowerCase().includes(search.toLowerCase());
            })

            setData(output);
        // }
        console.log(categories);
        console.log(filters);
        // console.log(output);
    }, [categories, filters, search])

    const handleCategories = (input) => {
        if (!categories.includes(input.value)) {
            setCategories([...categories, input.value])
        }
    }

    const handleFilters = (input) => {
        setFilters([...filters, input.value])
    }

    // const handleSearch = (event) => {
    //     let input = event.target.value
    //     setSearch(input);
    // }

    return (
        <main className='p-16 pl-32 pr-32'>
            <h1 className='text-4xl mb-8'>Verifications Backlog</h1>
            <section className='flex w-full items-center'>
                <div className='flex gap-3 w-full'>
                    <input type='text' placeholder='Search'
                        className='border-slate-400 border-2 rounded-md p-1 grow' onChange={(e) => setSearch(e.target.value)}/>
                    <div className='flex'>
                    <div className='me-2'>
                    <Dropdown
                        icon={SortIcon}
                        title={'Sort'}
                        categoryOptions={categoryOptions}
                        filterOptions={filterOptions}
                        handleCategories={handleCategories}
                        handleFilters={handleFilters} />
                    </div>
                    <div className=''>
                    <Dropdown 
                        icon={FilterIcon}
                        title={'Filter'}
                        categoryOptions={categoryOptions}
                        filterOptions={filterOptions}
                        handleCategories={handleCategories}
                        handleFilters={handleFilters} />
                        </div>
                     </div>
                </div>
                
            </section>
            <section className='pt-8 pb-6'>
                    
                    <ListView listData={data} verificationPage={true} />
                
            </section>
        </main>
    )
}
