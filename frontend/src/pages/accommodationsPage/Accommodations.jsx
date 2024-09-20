import { React, useState, useEffect } from 'react'
import accommodationsMock from '../../mockData/accommodationsMocks.json'
import CardView from './cardView/CardView'
import { ListView } from './listView/ListView'
import Card from './cardView/Card'
import GridIcon from '../../assets/gridIcon.png'
import ListIcon from '../../assets/listIcon.png'
import SortIcon from '../../assets/sort.png'
import FilterIcon from '../../assets/filter.png'
import Dropdown from '../../components/Dropdown'
// import { ListView } from './listView/listView'
export const Accommodations = () => {
    const [data, setData] = useState([])
    const [view, setView] = useState(true)
    useEffect(() => {
        setData(accommodationsMock.accommodations);
    }, [data])

    //Menu filter options
    const categoryOptions = [
        { value: 'natureOfInjury', label: 'Nature of Injury' },
        { value: 'accommodationName', label: 'Accommodation Name' }
    ]
    const subOptions = [
        { value: 'forward', label: 'A -> Z' },
        { value: 'reverse', label: 'Z -> A' }
    ]
    return (
        <main className='p-16 pl-32 pr-32'>
            <h1 className='text-4xl mb-8'>List of Accommodations</h1>
            <section className='flex w-full items-center'>
                <div className='flex gap-3 w-full'>
                    <input type='text' placeholder='Search'
                        className='border-slate-400 border-2 rounded-md p-1 w-2/6' />
                    <Dropdown
                        icon={SortIcon}
                        title={'Sort'}
                        categoryOptions={categoryOptions}
                        subOptions={subOptions} />
                    <Dropdown
                        icon={FilterIcon}
                        title={'Filter'}
                        categoryOptions={categoryOptions}
                        subOptions={subOptions} />
                </div>
                <div className='flex' onClick={() => setView(!view)}>
                    <div className={`p-3 px-5 flex items-center justify-center border-2 border-r-0 border-slate-400 rounded-tl-md rounded-bl-md ${!view && ' bg-sky-100'}`}>
                        <img src={ListIcon} />
                        <p className='font-semibold pl-1 text-slate-600'>List</p>
                    </div>
                    <div className={`p-3 px-5 flex items-center justify-center border-2 border-l-0 border-slate-400 rounded-tr-md rounded-br-md ${view && ' bg-sky-100'}`}>
                        <img src={GridIcon} />
                        <p className='font-semibold pl-1 text-slate-600'>Grid</p>
                    </div>
                </div>
            </section>
            <form className='grid grid-cols-6'>
                {/* menu at top */}
            </form>
            <section className='pt-8 pb-6'>
                {view ?
                    <CardView cards={data} />
                    :
                    <ListView listData={data}/>
                }
            </section>
        </main>
    )
}

// {view ? (<CardView cardsData={data} />) : <ListView listData={data} />}
